QUVI_PREFIX=/usr/local
CELERY_LOGGING_LEVEL="debug"


run:
	./manage.py runserver

initvenv:
	virtualenv venv

worker:
	./manage.py celery worker --loglevel=${CELERY_LOGGING_LEVEL} -E -Q quvi

db:
	./manage.py syncdb --noinput
	./manage.py migrate

clean:
	rm -rf ./build
	find . -name "*.pyc" -delete

deps:
	pip install Django
	pip install Cython
	cd ${VIRTUAL_ENV}/src/python-quvi && python setup.py build_ext
	cd ${VIRTUAL_ENV}/src/python-quvi && python setup.py install
	pip install -r config/requirements.pip

deps-system:
	sudo apt-get install rabbitmq-server

build-deps:
	sudo apt-get install libtool libcurl4-gnutls-dev liblua5.1-0-dev \
		             gengetopt

test:  clean
	./manage.py test video

fixtures:
	./manage.py dumpdata --indent=2 > video/fixtures/initial_data.json

migration:
	./manage.py schemamigration $(app) --auto

migrate:
	./manage.py migrate

fetch-quvi:
	mkdir -p build
	git clone -b maint-0.4 git://repo.or.cz/libquvi-scripts.git build/libquvi-scripts
	git clone -b maint-0.4 git://repo.or.cz/libquvi.git build/libquvi
	git clone -b maint-0.4 git://repo.or.cz/quvi-tool.git build/quvi-tool

quvi-scripts:
	cd build/libquvi-scripts; ./autogen.sh
	cd build/libquvi-scripts; ./configure --with-nsfw
	cd build/libquvi-scripts; make
	cd build/libquvi-scripts; sudo make install

libquvi:
	cd build/libquvi; ./autogen.sh
	cd build/libquvi; ./configure
	cd build/libquvi; make
	cd build/libquvi; sudo make install


quvi-tool:
	cd build/quvi-tool; \
		./autogen.sh; \
		./configure; \
		make; \
		sudo make install

quvi-python:
	cd ${VIRTUAL_ENV}/src/python-quvi; ls; \
		python setup.py build_ext; \
		python setup.py install

quvi:	libquvi quvi-scripts quvi-tool
