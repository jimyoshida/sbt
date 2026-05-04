# omitting .PHONY
PKG_NAME    := $(shell grep '^Package:' DEBIAN/control | awk '{print $$2}')
PKG_VERSION := $(shell grep '^Version:' DEBIAN/control | awk '{print $$2}')
PKG_FILE    := out/$(PKG_NAME)_$(PKG_VERSION)_all.deb

$(PKG_FILE): sbt.py sbt.1 DEBIAN/control build-deb.sh Makefile
	bash -x build-deb.sh $(PKG_FILE)

install:
	dpkg -i $(PKG_FILE)

uninstall:
	dpkg -r $(PKG_NAME)

clean:
	rm -fr out/ tmp/
