import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task


PROJECT_NAME = 'dacom'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.env')

env.hosts = []


@task
def production():
    env.hosts = ['root@5.196.225.197']
    env.environment = 'production'


@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield


def chown():
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)


def restart():
    sudo('systemctl restart nginx')
    sudo('systemctl restart dacom')


@task
def fetch(blockchain):
    with cd(PROJECT_ROOT):
        with source_virtualenv():
            run('./manage fetch %s' % blockchain)


@task
def deploy():
    """
    Deploys the latest tag to the production server
    """
    # sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master --no-edit')
        with source_virtualenv():
            run('pip install -r requirements.txt')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')

    restart()
