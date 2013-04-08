QUVI_PREFIX=/usr/local


run:
	./manage.py runserver

clean:
	rm -rf ./build
	find . -name "*.pyc" -delete

build-deps:
	sudo apt-get install libtool libcurl4-gnutls-dev liblua5.1-0-dev \
		             gengetopt

test:
	./manage.py test video

fetch-quvi:
	mkdir -p build
	git clone git://repo.or.cz/libquvi-scripts.git build/libquvi-scripts
	git clone git://repo.or.cz/libquvi.git build/libquvi
	git clone git://repo.or.cz/quvi-tool.git build/quvi-tool

quvi-scripts:
	cd build/libquvi-scripts; ./autogen.sh
	cd build/libquvi-scripts; ./configure
	cd build/libquvi-scripts; make
	cd build/libquvi-scripts; sudo make install

libquvi:
	cd build/libquvi; ./autogen.sh
	cd build/libquvi; ./configure
	cd build/libquvi; make
	cd build/libquvi; sudo make install
	

quvi-tool:
	cd build/quvi-tool; ./autogen.sh
	cd build/quvi-tool; ./configure
	cd build/quvi-tool; make
	cd build/quvi-tool; sudo make install

quvi:	libquvi quvi-scripts quvi-tool
