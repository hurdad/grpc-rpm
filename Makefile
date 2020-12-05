# grpc-rpm
version = 1.34.0
release = 1
name = grpc
full_name = $(name)-$(version)
download_url = "https://github.com/grpc/$(name)/archive/v$(version).tar.gz"

all: rpm

clean:
	rm -rf rpmbuild
	rm -rf grpc
	rm -rf $(full_name)
	rm -rf $(full_name).tar.gz

mkdir: clean
	mkdir -p rpmbuild
	mkdir -p rpmbuild/BUILD
	mkdir -p rpmbuild/BUILDROOT
	mkdir -p rpmbuild/RPMS
	mkdir -p rpmbuild/SOURCES
	mkdir -p rpmbuild/SRPMS

download: mkdir
	git clone --recursive https://github.com/grpc/grpc.git
	mv grpc $(full_name)
	cd $(full_name) && git checkout v$(version)
	tar -czvf $(full_name).tar.gz $(full_name)
	cp $(full_name).tar.gz rpmbuild/SOURCES/$(full_name).tar.gz

rpm: download
	rpmbuild $(RPM_OPTS) \
	  --define "_topdir %(pwd)" \
	  --define "_builddir %{_topdir}/rpmbuild/BUILD" \
	  --define "_buildrootdir %{_topdir}/rpmbuild/BUILDROOT" \
	  --define "_rpmdir %{_topdir}/rpmbuild/RPMS" \
	  --define "_srcrpmdir %{_topdir}/rpmbuild/SRPMS" \
	  --define "_specdir %{_topdir}" \
	  --define "_sourcedir %{_topdir}/rpmbuild/SOURCES" \
	  --define "VERSION $(version)" \
 	  --define "RELEASE $(release)" \
	  -ba $(name).spec
