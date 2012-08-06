from os.path import join
from fabric import utils
from fabric.api import run, env, local, sudo, put, require, cd
from fabric.contrib.project import rsync_project

from fabsettings import REMOTE_PATH, REMOTE_HOST, PROJECT_NAME

RSYNC_EXCLUDE = (
    '.git',
    '.gitignore',
    '.bzr',
    '.bzrignore',
    '*.pyc',
    '*.db',
    'fabfile.py',
    'bootstrap.py',
    'reload',
    'save-fixtures',
    'media/*',
    'static',
)

# Structure of the project on the server
# /root/path                     <- Home directory of project owner
#           |
#           +->staging/             <- Virtualenv specific to staging env
#                   |
#                   +->project_name/      <- Root of Django project


env.home = REMOTE_PATH
env.project = PROJECT_NAME


def _setup_path():
    env.root = join(env.home, env.environment)
    env.code_root = join(env.root, env.project)


def staging():
    env.user = 'django'
    env.environment = 'staging'
    env.hosts = [REMOTE_HOST]
    env.host = REMOTE_HOST
    _setup_path()


def production():
    utils.abort("No production server defined")


def touch():
    """Touch wsgi file to trigger reload."""
    require('code_root', provided_by=('staging', 'production'))
    conf_dir = join(env.code_root, 'config')
    with cd(conf_dir):
        run('touch %s.wsgi' % env.project)


def apache_reload():
    sudo('service apache2 reload', shell=False)


def test():
    local("python manage.py test")


def initial_setup():
    """Setup virtualenv"""
    sudo('pip install virtualenv', shell=False)
    run('mkdir -p %(home)s' % env)
    run('cd %(home)s; virtualenv --no-site-packages %(environment)s' % env)
    put('requirements.txt', env.root)
    run('cd %(root)s ; ' % env + \
        'source ./bin/activate ; ' + \
        'pip install -E %(root)s --requirement requirements.txt' % env)


def update_vhost():
    local('cp config/%(project)s.conf /tmp' % env)
    local('sed -i s#%%ROOT%%#%(home)s#g /tmp/%(project)s.conf' % env)
    local('sed -i s/%%PROJECT%%/%(project)s/g /tmp/%(project)s.conf' % env)
    local('sed -i s/%%ENV%%/%(environment)s/g /tmp/%(project)s.conf' % env)
    local('sed -i s/%%DOMAIN%%/%(host)s/g /tmp/%(project)s.conf' % env)
    put('/tmp/%(project)s.conf' % env, '%(root)s' % env)
    sudo('cp %(root)s/%(project)s.conf ' % env +\
         '/etc/apache2/sites-available/%(project)s' % env, shell=False)
    sudo('a2ensite %(project)s' % env, shell=False)


def rsync():
    require('root', provided_by=('staging', 'production'))
    extra_opts = '--omit-dir-times'
    rsync_project(
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts
    )


def reload_data():
    require('code_root', provided_by=('staging', 'production'))
    if env.environment == "staging":
        with cd(env.code_root):
            run("mkdir -p db")
            run("rm -f db/*.db")
            run("source ../bin/activate; python manage.py syncdb --noinput")
            run("chmod 777 db -R")


def copy_local_settings():
    require('code_root', provided_by=('staging', 'production'))
    put('config/local_settings_%(environment)s.py' % env, env.code_root)
    with cd(env.code_root):
        run('mv local_settings_%(environment)s.py local_settings.py' % env)


def collectstatic():
    with cd(env.code_root):
        run('source ../bin/activate; python manage.py collectstatic --noinput')


def configtest():
    run("apache2ctl configtest")


def deploy():
    #initial_setup()
    rsync()
    copy_local_settings()
    reload_data()
    collectstatic()
    update_vhost()
    configtest()
    apache_reload()
