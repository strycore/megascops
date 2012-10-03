from os.path import join
from fabric import utils
from fabric.api import run, env, local, sudo, put, require, cd
from fabric.contrib.project import rsync_project

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
    'static/CACHE',
    'megascops.log'
)

env.home = "/srv/django"
env.project = "megascops"


def _setup_path():
    env.root = join(env.home, env.domain)
    env.code_root = join(env.root, env.project)


def staging():
    env.user = 'django'
    env.environment = 'staging'
    env.domain = "megascops.strycore.com"
    env.hosts = [env.domain]
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


def setup():
    """Setup virtualenv"""
    run('mkdir -p %(root)s' % env)
    with cd(env.root):
        run('virtualenv --no-site-packages .')


def requirements():
    put('requirements.txt', env.root)
    with cd(env.root):
        run('source ./bin/activate && '
            'pip install Cython && '
            'pip install --requirement requirements.txt')


def update_vhost():
    local('cp config/%(project)s.vhost /tmp' % env)
    local('sed -i s#%%ROOT%%#%(root)s#g /tmp/%(project)s.vhost' % env)
    local('sed -i s/%%PROJECT%%/%(project)s/g /tmp/%(project)s.vhost' % env)
    local('sed -i s/%%ENV%%/%(environment)s/g /tmp/%(project)s.vhost' % env)
    local('sed -i s/%%DOMAIN%%/%(domain)s/g /tmp/%(project)s.vhost' % env)
    put('/tmp/%(project)s.vhost' % env, '%(root)s' % env)
    sudo('cp %(root)s/%(project)s.vhost ' % env +
         '/etc/apache2/sites-available/%(domain)s' % env, shell=False)
    sudo('a2ensite %(domain)s' % env, shell=False)


def rsync():
    require('root', provided_by=('staging', 'production'))
    extra_opts = '--omit-dir-times'
    rsync_project(
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts
    )


def copy_local_settings():
    require('code_root', provided_by=('staging', 'production'))
    put('config/local_settings_%(environment)s.py' % env, env.code_root)
    with cd(env.code_root):
        run('mv local_settings_%(environment)s.py megascops/local_settings.py'
            % env)


def syncdb():
    require('code_root', provided_by=('stating', 'production'))
    with cd(env.code_root):
        run("source ../bin/activate; "
            "python manage.py syncdb --noinput")


def migrate():
    require('code_root', provided_by=('stating', 'production'))
    with cd(env.code_root):
        run("source ../bin/activate; "
            "python manage.py migrate")


def collectstatic():
    with cd(env.code_root):
        run('source ../bin/activate; python manage.py collectstatic --noinput')


def fix_perms(user="www-data"):
    with cd(env.code_root):
        run("mkdir -p media")
        run("mkdir -p static")
        sudo("chown -R %s.%s media" % (user, user))
        sudo("chown -R %s.%s static" % (user, user))
        sudo("chown %s.%s megascops.log" % (user, user))


def configtest():
    sudo("apache2ctl configtest")


def deploy():
    fix_perms(env.user)
    requirements()
    rsync()
    copy_local_settings()
    collectstatic()
    update_vhost()
    configtest()
    fix_perms()
    apache_reload()
