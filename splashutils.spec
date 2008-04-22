# TODO
# - static linking for initrd
# Conditional build:
%bcond_without	verbose		# verbose build (V=1)
%bcond_without	initrd	# build klibc static initrd binaries
Summary:	Utilities for setting splash
Summary(pl.UTF-8):	Narzędzia do ustawiania splash
Name:		splashutils
Version:	1.5.4
Release:	0.2
License:	GPL
Group:		Applications/System
Source0:	http://dev.gentoo.org/~spock/projects/splashutils/archive/%{name}-%{version}.tar.bz2
# Source0-md5:	325e11440bb040c72b71556ece17a7dd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-libs.patch
#Patch0: %{name}-makefile.patch # in -libs now
#Patch1: %{name}-compile.patch
#Patch2: %{name}-pld-paths.patch
URL:		http://dev.gentoo.org/~spock/projects/splashutils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	freetype-devel
BuildRequires:	gpm-devel
BuildRequires:	klibc-devel >= 1.1.1-1
BuildRequires:	lcms-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel
BuildRequires:	libpng-devel
BuildRequires:	linux-libc-headers >= 7:2.6.9.1-1.5
BuildRequires:	zlib-devel
%if %{with initrd}
BuildRequires:	freetype-static
BuildRequires:	glibc-static
BuildRequires:	gpm-static
BuildRequires:	klibc-static >= 1.1.1-1
BuildRequires:	lcms-static
BuildRequires:	libjpeg-static
BuildRequires:	libmng-static
BuildRequires:	libpng-static
BuildRequires:	zlib-static
%endif
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Suggests:	splash-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for setting splash.

%description -l pl.UTF-8
Narzędzia do ustawiania splash.

%package devel
Summary:	Header files for splashutils
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for splashutils libraries

%package static
Summary:	Static splashutils libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static splashutils libraries

%prep
%setup -q %{?notyet:-a1}
%patch0 -p1
#%patch0 -p0
#%patch1 -p0
#%patch2 -p1

mkdir -p nobuild
mv libs/freetype-* nobuild
mv libs/jpeg-* nobuild
mv libs/libpng-* nobuild
mv libs/zlib-* nobuild
mv configure{,.dist}

%build
if [ ! -f configure -o configure.ac -nt configure ]; then
	%{__libtoolize}
	%{__aclocal}
	%{__autoconf}
	%{__autoheader}
	%{__automake}
fi

%if %{with initrd}
# build klibc static for initrd
%configure \
	--with-themedir=%{_sysconfdir}/splash \
	--with-gpm \
	--with-mng \
	--with-png \
	--with-png \
	--with-ttf \
	--with-ttf-kernel

%{__make} -j1 %{?with_verbose:QUIET=false}

%{__make} install DESTDIR=`pwd`/klibc
%{__make} clean
%endif

# build shared for system
%configure \
	--enable-klibc-shared \
	--with-klibc-compiler="%{__cc}" \
	--with-themedir=%{_sysconfdir}/splash \
	--with-gpm \
	--with-mng \
	--with-png \
	--with-png \
	--with-ttf \
	--with-ttf-kernel

%{__make} -j1 %{?with_verbose:QUIET=false}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/splash,/etc/rc.d/init.d,/etc/sysconfig} \
	    $RPM_BUILD_ROOT/var/run/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/splash
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/splash
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add splash

%postun	-p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del splash
fi

%triggerpostun -- %{name} < 1.5.4-0.2
# migrate from apache-config macros
if [ -f /etc/sysconfig/fbsplash.rpmsave ]; then
	cp -f /etc/sysconfig/splash,{.rpmnew}
	mv -f /etc/sysconfig/{fbsplash.rpmsave,splash}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README docs/[!M]*
%attr(755,root,root) /sbin/fbcondecor_ctl.static
%attr(755,root,root) /sbin/fbcondecor_helper
%attr(755,root,root) /sbin/fbsplashctl
%attr(755,root,root) /sbin/fbsplashd.static
%attr(755,root,root) /sbin/splash-functions.sh
%attr(755,root,root) /sbin/splash_util.static
%attr(755,root,root) %{_bindir}/bootsplash2fbsplash
%attr(755,root,root) %{_bindir}/splash_manager
%attr(755,root,root) %{_bindir}/splash_resize
%attr(755,root,root) %{_bindir}/splash_util
%attr(755,root,root) %{_bindir}/splashy2fbsplash.py
%attr(755,root,root) %{_sbindir}/fbcondecor_ctl
%attr(755,root,root) %{_sbindir}/fbsplashd
%attr(755,root,root) %{_sbindir}/splash_geninitramfs
%attr(755,root,root) %{_libdir}/libfbsplash.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfbsplash.so.1
%attr(755,root,root) %{_libdir}/libfbsplashrender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfbsplashrender.so.1
%attr(754,root,root) /etc/rc.d/init.d/splash
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/splash
%dir %{_sysconfdir}/splash
%dir /var/run/splashutils

%files devel
%defattr(644,root,root,755)
%{_libdir}/libfbsplash.so
%{_libdir}/libfbsplashrender.so
%{_libdir}/libfbsplash.la
%{_libdir}/libfbsplashrender.la
%{_includedir}/fbsplash.h
%{_pkgconfigdir}/libfbsplash.pc
%{_pkgconfigdir}/libfbsplashrender.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfbsplash.a
%{_libdir}/libfbsplashrender.a
