%ifarch x86_64
%define lg_page --with-lg-page=12
%endif

%ifarch aarch64
%define lg_page --with-lg-page=16
%endif

%ifarch aarch64
%define disable_thp --disable-thp
%endif

Name:           jemalloc
Version:        5.1.0
Release:        4
Summary:        General-purpose scalable concurrent malloc implementation
License:        BSD
URL:            http://www.canonware.com/jemalloc/
Source0:        https://github.com/jemalloc/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  libxslt perl-generators gcc

%description
Implemented by malloc (3), is an independent implementation of jemalloc.

%package devel
Summary:        Devel files for jemalloc
Requires:       %{name} = %{version}-%{release}

%description devel
The devel contains libraries and header files for use in jemalloc applications.

%package help
Summary:        help for jemalloc.

%description help
The help package contains manual pages and other related files for jemalloc.

%prep
%autosetup -p1

%build
export LDFLAGS="%{?__global_ldflags} -lrt"
getconf PAGESIZE
uname -a
%configure %{?disable_thp} %{?lg_page}
%make_build

%check
%if %{?_with_check:1}%{!?_with_check:0}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test %{?_smp_mflags}
make check
%endif

%install
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%{_bindir}/jemalloc-config
%{_libdir}/pkgconfig/jemalloc.pc

%files devel
%{_includedir}/jemalloc
%{_bindir}/jeprof
%{_libdir}/libjemalloc.so
%exclude %{_libdir}/libjemalloc.a
%exclude %{_libdir}/libjemalloc_pic.a
%exclude %{_datadir}/doc/%{name}/jemalloc.html

%files help
%doc README VERSION doc/jemalloc.html
%{_mandir}/man3/jemalloc.3*

%changelog
* Wed Jun 02 2021 wulei <wulei80@huawei.com> - 5.1.0-4
- fixes failed: no acceptable C compiler found in $PATH

* Thu Nov 14 2019 wangye<wangye54@huawei.com> - 5.1.0-3
- Package init
