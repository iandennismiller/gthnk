# greenthink-library (c) 2013 Ian Dennis Miller

import sys, os, platform
from fabric.api import env, run, put, get, open_shell, local, hosts
from fabric.contrib.project import rsync_project

env.user = 'greenthink-library'
env.key_filename = ['/Users/idm/.ssh/keys/secure']

if not env.hosts:
    print "need to call with -H [host.saperea.com]"
    sys.exit(1)

def rsync():
    "rsync project to remote system"

    if not os.path.exists("fabfile.py"):
        print "need to run in root of project"
        sys.exit(1)

    excluded = [
        "*.egg-info",
        ".build",
        ".git*",
        "*.pyc",
        "dist",
        "build",
    ]
    rsync_project(remote_dir=env.user, local_dir="./", exclude=excluded, delete=True)

def pull():
    "pull on the remote system"
    run('cd ~/{app} && git pull'.format(app=env.user))

def setup():
    "run make install, which installs this module"
    cmd = 'source ~/.virtualenvs/{app}/bin/activate && cd {app} && make install'
    run(cmd.format(app=env.user))

def ipython():
    "open ipython environment on remote host"
    open_shell("~/.virtualenvs/{app}/bin/manage.py shell && exit".format(app=env.user))

def ssh():
    "open a shell on the remote host"
    open_shell("source ~/.virtualenvs/{app}/bin/activate".format(app=env.user))

def restart():
    "restart app server"
    run("pkill -HUP runserver.py")

def logs():
    "watch logs on remote server"
    open_shell("tail -f /var/log/{app}/*log /var/log/nginx/{app}*log && exit".format(app=env.user))

def help():
    "get help on testing and deploying"
    print helpfile

helpfile = """
# fabric is used to manage remote deployments of this application

# quickly copy some changes over
fab rsync setup restart
"""