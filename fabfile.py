#!/usr/bin/python

from fabric.api import *
from fabric.contrib import *
import os

def packages():
    sudo('apt-get -y update')
    sudo('apt-get -y -f upgrade')
    sudo('apt-get -y install gdebi')
    sudo('apt-get -y install nginx')
    sudo('apt-get -y install supervisor')
    sudo('apt-get -y install htop')
    sudo('apt-get -y install htop python-setuptools nginx python-pip language-pack-pt-base language-pack-pt python-pychart-doc python-dateutil python-docutils python-feedparser python-gdata python-jinja2 python-ldap python-libxslt1 python-lxml python-mako python-mock python-openid python-psycopg2 python-psutil python-pybabel python-pychart python-pydot python-pyparsing python-reportlab python-simplejson python-tz python-unittest2 python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi')

def postgres():
    put('files/locale','/etc/default/locale',use_sudo=True)
    sudo('apt-get -y install language-pack-pt-base language-pack-pt')
    sudo('apt-get -y install postgresql')
    sudo('su - postgres -c "createuser -s openerp"')

def openerp():
    sudo('wget http://nightly.openerp.com/7.0/nightly/deb/openerp_7.0-latest-1.tar.gz')
    sudo('mkdir /opt/openerp') 
    sudo('mkdir /etc/openerp')
    sudo('tar zvxf openerp_7.0-latest-1.tar.gz -C /opt/openerp  --strip-components 1') 

def instance(instance='openerp'):
    env.instance = instance

    sudo('useradd -m -d /home/%(instance)s -s /bin/true %(instance)s' % env)
    sudo('su -  postgres -c "createuser -s %(instance)s"' % env)
    sudo('mkdir -p  /home/%(instance)s/addons' % env)
    #
    source_file = 'files/openerp/template.conf'
    destination_file = '/etc/openerp/%(instance)s.conf' % env
    files.upload_template(source_file, destination_file, context=env,mode=0755,use_sudo=True)
    #
    source_file = 'files/supervisor/template.conf'
    destination_file = os.path.join('/etc/supervisor/conf.d/',env.instance + '.conf')
    files.upload_template(  'files/supervisor/template.conf',
                            '/etc/supervisor/conf.d/%(instance)s.conf' % env,
                            context=env,use_sudo=True)
    #
    source_file = 'files/nginx/template.conf'
    destination_file = os.path.join('/etc/nginx/conf.d/',env.instance + '.conf')
    files.upload_template(source_file, destination_file, context=env,use_sudo=True)
    #
    sudo('supervisorctl update')
    sudo('supervisorctl restart %(instance)s' % env)
    sudo('/etc/init.d/nginx restart')


@task
def deploy():
    packages()
    postgres()
    openerp()
    instance('openerp')
