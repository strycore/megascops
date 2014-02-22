QUVI_PREFIX=/usr/local
CELERY_LOGGING_LEVEL="debug"


run:
	DJANGO_SETTINGS_MODULE=megascops.settings.local ./manage.py runserver 0.0.0.0:8000

initvenv:
	virtualenv venv

worker:
	./manage.py celery worker --loglevel=${CELERY_LOGGING_LEVEL} -E -Q quvi

db:
	DJANGO_SETTINGS_MODULE=megascops.settings.local ./manage.py syncdb --noinput
	DJANGO_SETTINGS_MODULE=megascops.settings.local ./manage.py migrate

clean:
	rm -rf ./build
	find . -name "*.pyc" -delete

deps:
	pip install -r config/requirements.pip

deps-system:
	sudo apt-get install rabbitmq-server liblua5.1-socket2 lua-expat \
		postgresql libpq-dev

deps-build:
	sudo apt-get install libtool libcurl4-gnutls-dev liblua5.1-0-dev \
		             autoconf gengetopt autopoint asciidoc \
			     libproxy-dev libjson-glib-dev libglib2.0-dev \
			     libxml2-dev

test:  clean
	DJANGO_SETTINGS_MODULE=megascops.settings.testing ./manage.py test video


shell:
	DJANGO_SETTINGS_MODULE=megascops.settings.local ./manage.py shell

fixtures:
	./manage.py dumpdata --indent=2 > video/fixtures/initial_data.json

migration:
	./manage.py schemamigration $(app) --auto

migrate:
	./manage.py migrate

fetch-quvi-0.4:
	mkdir -p build
	git clone -b maint-0.4 git://repo.or.cz/libquvi-scripts.git build/libquvi-scripts
	git clone -b maint-0.4 git://repo.or.cz/libquvi.git build/libquvi
	git clone -b maint-0.4 git://repo.or.cz/quvi-tool.git build/quvi-tool

fetch-quvi:
	mkdir -p build
	git clone git://repo.or.cz/libquvi-scripts.git build/libquvi-scripts
	git clone git://repo.or.cz/libquvi.git build/libquvi
	git clone git://repo.or.cz/quvi-tool.git build/quvi-tool

quvi-scripts:
	cd build/libquvi-scripts && \
	./bootstrap.sh && \
	./configure --with-nsfw && \
	make && \
	sudo make uninstall && \
	sudo make install

libquvi:
	cd build/libquvi && \
	./bootstrap.sh && \
	./configure && \
	make && \
	sudo make uninstall && \
	sudo make install


quvi-tool:
	cd build/quvi-tool && \
	./bootstrap.sh && \
	./configure && \
	make && \
	sudo make uninstall && \
	sudo make install

quvi-python:
	cd ${VIRTUAL_ENV}/src/python-quvi; ls; \
		python setup.py build_ext; \
		python setup.py install

quvi:	quvi-scripts libquvi quvi-tool

npmdeps:
	sudo npm install coffee-script -g
	sudo npm install less -g
