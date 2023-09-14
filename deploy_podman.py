from pyinfra import host
from pyinfra.operations import apt, server, files

server.shell(
    name="add gpg key for podman",
    commands=[
        'curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_20.04/Release.key" | sudo apt-key add -'
    ],
)

server.shell(
    name="add podman repo",
    commands=[
        'echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_20.04/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list'
    ],
)

apt.update(name="Update package cache", sudo=True)


apt.packages(
    name="Install Podman",
    packages=["podman"],
    sudo=True,
)

files.directory(
    name="create project directory",
    path=f"/home/{host.data.ssh_user}/{host.data.project_path}/",
)

files.template(
    name="Create service file",
    src="templates/kube_deploy.j2",
    dest=f"/home/{host.data.ssh_user}/{host.data.project_path}/kube.yml",
    google_maps_api_key=host.data.google_maps_api_key,
    app_image=host.data.app_image,
    mode="755",
)

server.shell(
    name="login in github registry",
    commands=[
        f"podman login ghcr.io -u {host.data.github_user} -p {host.data.github_token}"
    ],
)

server.shell(
    name="pull route-planner image", commands=[f"podman pull {host.data.app_image}"]
)

server.shell(name="pull mongo image", commands=["podman pull docker.io/library/mongo"])

server.shell(
    name="run podman command to start app",
    commands=[
        f"podman play kube /home/{host.data.ssh_user}/{host.data.project_path}/kube.yml"
    ],
)
