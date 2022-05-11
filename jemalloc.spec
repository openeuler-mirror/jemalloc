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
Version:        5.2.1
Release:        6
Summary:        General-purpose scalable concurrent malloc implementation
License:        BSD-2-Clause
URL:            http://www.canonware.com/jemalloc/
Source0:        https://github.com/jemalloc/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

Patch1:         backport-Jemalloc-5.2.1-patch-1-fix-large-bin-index-accessed-through-cache-bin-descriptor.patch
Patch2:         backport-Jemalloc-5.2.1-patch-2-fix-undefined-behavior-in-hash.patch
Patch3:         backport-Jemalloc-5.2.1-patch-3-fix-tcaches-mutex-pre-post-fork-handling.patch
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
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test %{?_smp_mflags}
make check

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
* Tue May 10 2022 Ge Wang <wangge@h-partner.com> - 5.2.1-6
- License compliance rectification

* Thu Dec 2 2021 guominghong <guominghong@huawei.com> - 5.2.1-5
- Fix spec check

* Tue Nov 16 2021 guominghong <guominghong@huawei.com> - 5.2.1-4
- Fix tcaches mutex pre-post fork handling

* Tue Nov 16 2021 guominghong <guominghong@huawei.com> - 5.2.1-3
- Fix Undefined Behavior in hash.h 

* Wed Nov 3 2021 guominghong <guominghong@huawei.com> - 5.2.1-2
- Fix large bin index accessed through cache bin descriptor

* Tue Jul 20 2021 weidong <weidong@uniontech.com> - 5.2.1-1
- Update jemlloc

* Wed Jun 02 2021 wulei <wulei80@huawei.com> - 5.1.0-4
- fixes failed: no acceptable C compiler found in $PATH

* Thu Nov 14 2019 wangye<wangye54@huawei.com> - 5.1.0-3
- Package init
