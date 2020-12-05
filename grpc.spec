%global debug_package %{nil}
Name: grpc
Version:	%{VERSION}
Release:        %{RELEASE}%{?dist}
Summary: Modern, open source, high-performance remote procedure call (RPC) framework
License: ASL 2.0
URL: https://www.grpc.io
Source:         %{name}-%{version}.tar.gz

BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: protobuf-devel
BuildRequires: protobuf-compiler
BuildRequires: openssl-devel
BuildRequires: re2-devel
BuildRequires: abseil-cpp-devel
BuildRequires: google-benchmark-devel
BuildRequires: zlib-devel

%description
gRPC is a modern open source high performance RPC framework that can run in any
environment. It can efficiently connect services in and across data centers
with pluggable support for load balancing, tracing, health checking and
authentication. It is also applicable in last mile of distributed computing to
connect devices, mobile applications and browsers to backend services.

The main usage scenarios:

* Efficiently connecting polyglot services in microservices style architecture
* Connecting mobile devices, browser clients to backend services
* Generating efficient client libraries

Core Features that make it awesome:

* Idiomatic client libraries in 10 languages
* Highly efficient on wire and with a simple service definition framework
* Bi-directional streaming with http/2 based transport
* Pluggable auth, tracing, load balancing and health checking


%package plugins
Summary: gRPC protocol buffers compiler plugins
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: protobuf-compiler

%description plugins
Plugins to the protocol buffers compiler to generate gRPC sources.

%package cli
Summary: gRPC protocol buffers cli
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cli
Plugins to the protocol buffers compiler to generate gRPC sources.

%package devel
Summary: gRPC library development files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and files for gRPC libraries.

%prep
%autosetup -N

#fix pkgconfig path
sed -i 's:lib/pkgconfig:lib64/pkgconfig:' CMakeLists.txt

%build
mkdir -p cmake/build
pushd cmake/build
cmake ../.. -DCMAKE_INSTALL_PREFIX=/usr  \
	-DBUILD_SHARED_LIBS=ON 		 \
	-DCMAKE_BUILD_TYPE=Release       \
	-DgRPC_INSTALL=ON           	 \
	-DgRPC_BUILD_TESTS=ON		 \
	-DgRPC_INSTALL_LIBDIR=lib64	 \
	-DgRPC_ABSL_PROVIDER=package     \
	-DgRPC_CARES_PROVIDER=package    \
	-DgRPC_PROTOBUF_PROVIDER=package \
	-DgRPC_RE2_PROVIDER=package      \
	-DgRPC_SSL_PROVIDER=package      \
	-DgRPC_ZLIB_PROVIDER=package	 \
	-DgRPC_BENCHMARK_PROVIDER=package \
	-DgRPC_INSTALL_CMAKEDIR=lib64/cmake/grpc
make %{?_smp_mflags}
popd

%install
pushd cmake/build
make install DESTDIR=%{buildroot}
cp grpc_cli %{buildroot}%{_bindir}

%post 
ldconfig

%postun
ldconfig

%files
%doc README.md
%license LICENSE
%{_libdir}/libaddress_sorting.so.14*
%{_libdir}/libgpr.so.14*
%{_libdir}/libgrpc++.so.1*
%{_libdir}/libgrpc++_error_details.so.1*
%{_libdir}/libgrpc++_reflection.so.1*
%{_libdir}/libgrpc++_unsecure.so.1*
%{_libdir}/libgrpc++_alts.so.1*
%{_libdir}/libgrpc.so.14*
%{_libdir}/libgrpc_unsecure.so.14*
%{_libdir}/libgrpc_plugin_support.so.1*
%{_libdir}/libgrpcpp_channelz.so.1*
%{_libdir}/libup*.so.14*
%{_datadir}/grpc

%files cli
%{_bindir}/grpc_cli

%files plugins
%doc README.md
%license LICENSE
%{_bindir}/grpc_*_plugin

%files devel
%{_libdir}/libaddress_sorting.so
%{_libdir}/libgpr.so
%{_libdir}/libgrpc++.so
%{_libdir}/libgrpc++_error_details.so
%{_libdir}/libgrpc++_reflection.so
%{_libdir}/libgrpc++_unsecure.so
%{_libdir}/libgrpc++_alts.so
%{_libdir}/libgrpc.so
%{_libdir}/libgrpc_unsecure.so
%{_libdir}/libgrpc_plugin_support.so
%{_libdir}/libgrpcpp_channelz.so
%{_libdir}/libupb.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/grpc/
%{_includedir}/grpc
%{_includedir}/grpc++
%{_includedir}/grpcpp

%changelog
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.26.0-1
- Update to 1.26.0

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 1.20.1-5
- Rebuild for protobuf 3.11

* Thu Oct 03 2019 Miro Hron?ok <mhroncok@redhat.com> - 1.20.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hron?ok <mhroncok@redhat.com> - 1.20.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.20.1-1
- Update to 1.20.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.18.0-1
- Update to 1.18.0

* Mon Dec 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.17.1-3
- Properly store patch in SRPM

* Mon Dec 17 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.1-2
- Build without ruby plugin for Fedora < 30 (Thanks to Mathieu Bridon)

* Fri Dec 14 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.1-1
- Update to 1.17.1 and package python bindings

* Fri Dec 07 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.0-1
- Initial revision
