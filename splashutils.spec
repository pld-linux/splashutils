# TODO
# - finish static linking
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

%define		misc_ver	0.1.5
Summary:	Utilities for setting splash
Summary(pl.UTF-8):	Narzędzia do ustawiania splash
Name:		splashutils
Version:	1.5.4
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://dev.gentoo.org/~spock/projects/splashutils/archive/%{name}-%{version}.tar.bz2
# Source0-md5:	325e11440bb040c72b71556ece17a7dd
Source1:	http://dev.gentoo.org/~spock/projects/gensplash/archive/misc%{name}-%{misc_ver}.tar.bz2
# Source1-md5:	20fc3ed2407edc8cd97623bf7f1c5c7b
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-libs.patch
#Patch0: %{name}-makefile.patch # in -libs now
#Patch1: %{name}-compile.patch
#Patch2: %{name}-pld-paths.patch
URL:		http://dev.gentoo.org/~spock/projects/splashutils/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freetype-static
BuildRequires:	glibc-static
BuildRequires:	gpm-static
BuildRequires:	klibc-static >= 1.1.1-1
BuildRequires:	lcms-static
BuildRequires:	libjpeg-static
BuildRequires:	libmng-static
BuildRequires:	libpng-static
BuildRequires:	linux-libc-headers >= 7:2.6.9.1-1.5
BuildRequires:	zlib-static
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Suggests:	splash-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for setting splash.

%description -l pl.UTF-8
Narzędzia do ustawiania splash.

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
	%{__aclocal}
	%{__autoconf}
	%{__autoheader}
	%{__automake}
fi
%configure \
	--with-themedir=%{_sysconfdir}/splash \
	--with-gpm \
	--with-mng \
	--with-png \
	--with-png \
	--with-ttf \
	--with-ttf-kernel \

%{__make} %{?with_verbose:QUIET=false}

%if 0
%{__make} objdir

%{__make} splash_kern \
	CC="%{__cc}"

%{__make} splash_user \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Os"

%{__make} -C miscsplashutils-%{misc_ver} \
	CFLAGS="%{rpmcflags} -Os -I/usr/include/freetype2" \
	LIBDIR="%{_libdir}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/splash,/etc/rc.d/init.d,/etc/sysconfig} \
	    $RPM_BUILD_ROOT/var/run/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%if 0
install miscsplashutils-%{misc_ver}/{fbres,fbtruetype/{fbtruetype,fbtruetype.static}} $RPM_BUILD_ROOT%{_bindir}
%endif
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/splash
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/splash

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add splash

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del splash
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README docs/*
%dir %{_sysconfdir}/splash
%dir /var/run/splashutils
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /sbin/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/splash
%attr(754,root,root) /etc/rc.d/init.d/splash
