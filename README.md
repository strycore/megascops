Megascops
=========

Dependencies
------------

Install python dependencies in a virtualenv using the bootstrap.py script

There are some other non-python dependencies which are required,
these must be installed before running the bootstrap script.

 * quvi
   sudo apt-get build-dep libquvi
   sudo apt-get install libtool gengetopt lua5.1 liblua5.1-0-dev
   git clone git://repo.or.cz/quvi.git
   cd quvi
   chmod +x autogen.sh
   ./autogen.sh
   ./configure [--enable-nsfw]
   make
   sudo make install

 * quvi python bindings
   the python bindings can't be installed directly using pip requirements
   because the install process in done in several steps.

    apt-get install cython
    pip -e git://github.com/metal3d/python-libquvi.git#egg=quvi
    # ignore build errors, you build it manually
    cd $VIRTUAL_ENV/src/quvi
    python setup.py build_ext --inplace
    python setup.py install

   You can test if you have successfully installed the python bindings by
   typing "import quvi" from the python interactive console.


PostgreSQL configuriguration
----------------------------

Create a user:

    sudo -u postgres psql
    create user megascops;

Note that the user will need to be able to create databases in order to run
tests. If you have created an user without this permission, run:

    sudo -u postgres psql
    ALTER USER megascops CREATEDB;

Creating a database:

    sudo -u postgres psql
    create database megascops with owner megascops;

or (in shell)

    createdb megascops -O megascops

Modify database's owner:

    sudo -u postgres psql
    alter database megascops owner to megascops;

Change user's password:

    sudo -u postgres psql
    alter user megascops with password 'admin';

Dropping all tables from the database

    drop schema public cascade;
    create schema public;

Quick setup:

    sudo -u postgres psql
    create user megascops with password 'admin';
    create database megascops with owner megascops;
    
