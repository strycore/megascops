Megascops
=========

Dependencies
------------

Install python dependencies in a virtualenv using the bootstrap.py script

There are some other non-python dependencies which are required,
these must be installed before running the bootstrap script.

 * gearman
   sudo apt-get install gearman

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
