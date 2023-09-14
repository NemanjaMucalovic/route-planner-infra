import os

from pyinfra import host
from pyinfra.facts.files import File
from pyinfra.operations import apt, server, files, git, python, pip


gpg_key = host.get_fact(File, host.data.gpg_path)
ssh_key = host.get_fact(File, f"/home/{host.data.ssh_user}/.ssh/id_rsa")
ssh_config = host.get_fact(File, f"/home/{host.data.ssh_user}/.ssh/config")


if ssh_key is None:
    server.shell(
        commands=[f'ssh-keygen -t rsa -N "" -f /home/{host.data.ssh_user}/.ssh/id_rsa']
    )

if ssh_config is None:
    files.template(
        name="Create ssh config.j2 file",
        src="templates/config.j2",
        dest=f"/home/{host.data.ssh_user}/.ssh/config",
    )


if gpg_key is None:
    server.shell(
        name="add gpg key for mongodb",
        commands=[
            "curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg    --dearmor"
        ],
    )

    server.shell(
        name="create list file for mongodb",
        commands=[
            'echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list'
       ],
    )


apt.update(name="Update package cache", sudo=True)

apt.packages(
    name="Install MongoDB packages and python3-pip",
    packages=["mongodb-org", "python3-pip", "python3.8-venv"],
    sudo=True,
)

server.service(
    name="Start MongoDB service",
    service="mongod",
    running=True,
    enabled=True,
    sudo=True,
)


git.repo(
    name="Clone repo",
    src="https://github.com/NemanjaMucalovic/route-planner.git",
    dest=f"/home/{host.data.ssh_user}/{host.data.project_path}",
)

pip.packages(
    name="Install virtualenv",
    pip="pip3",
    packages=["virtualenv"],
)

pip.venv(
    name="Create a virtualenv",
    python="/usr/bin/python3",
    path=f"/home/{host.data.ssh_user}/{host.data.project_path}/venv",
    _shell_executable="/bin/bash",
)
pip.packages(
    name="Install pyinfra into a virtualenv",
    requirements=f"/home/{host.data.ssh_user}/{host.data.project_path}/requirements.txt",
    virtualenv=f"/home/{host.data.ssh_user}/{host.data.project_path}/venv",
    _shell_executable="/bin/bash",
)


files.template(
    name="Create service file",
    src="templates/backend_service.j2",
    dest="/etc/systemd/system/backend.service",
    google_maps_api_key=host.data.google_maps_api_key,
    project_path=host.data.project_path,
    app_user=host.data.ssh_user,
    mode="755",
    user="root",
    group="root",
    sudo=True,
)

server.service(
    name="Start FastAPI service",
    service="backend",
    running=True,
    enabled=True,
    sudo=True,
)
