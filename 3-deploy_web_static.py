#!/usr/bin/python3
# Fabfile to deploy an archive to web servers.

from fabric.api import task, env, run
from fabric.tasks import execute
from os.path import exists

env.hosts = ['54.236.194.249', '100.25.179.160']
env.user = 'ubuntu'


@task
def deploy():
    """Deploys the web_static content to the web servers."""

    # Execute do_pack() to create an archive
    archive_path = execute(do_pack)

    # Check if archive was created successfully
    if not archive_path:
        return False

    # Deploy the archive to the web servers
    result = execute(do_deploy, archive_path['localhost'])

    return result['localhost']  # Return the result of deployment


@task
def do_pack():
    """Create a tar gzipped archive of the directory web_static."""

    from datetime import datetime
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))
    mkdir_command = "mkdir -p versions"
    tar_command = "tar -cvzf {} web_static".format(path)

    # Execute the commands locally to create the archive
    if run("{} && {}".format(mkdir_command, tar_command)).succeeded:
        if exists(path):
            print("web_static packed: {}".format(path))
            return path
    return None


@task
def do_deploy(archive_path):
    """Distributes an archive to a web server."""

    if not exists(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if run("mkdir -p /tmp/").failed:
        return False

    # Upload the archive to the server
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    # Extract the archive
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False

    # Remove the archive
    if run("rm /tmp/{}".format(file)).failed:
        return False

    # Move the content
    if run(f"mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/").failed:
        return False

    # Delete the symbolic link
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False

    # Delete the old folder
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a new symbolic link
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False

    print("New version deployed!")
    return True
