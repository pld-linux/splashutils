#
# TODO
#	- use static packages from distro, not included ones
#	- find a way to make it work on startup (not initrd imo, at kernel
#		time - initramfs) + maybe some init.d
#	- check initramfs (upgrade geninitrd maybe), cause splashutils can
#		make use of it
#	- better way to use kernel-headers (maybe patch glibc-kernel-headers
#		and use them instead)
#
%define		_pre		pre10
%define		_misc_ver	0.1.2
Summary:	Utilities for setting fbsplash
Summary(pl):	Narzêdzia do ustawiania fbsplash
Name:		splashutils
Version:	0.9
Release:	0.%{_pre}.2
License:	GPL
Group:		System
Source0:	http://dev.gentoo.org/~spock/projects/gensplash/current/%{name}-%{version}-%{_pre}.tar.bz2
# Source0-md5:	20ab27ea8e02dc2efb6789cf53663ec8
Source1:	http://dev.gentoo.org/~spock/projects/gensplash/current/miscsplashutils-%{_misc_ver}.tar.bz2
# Source1-md5:	71f85c661c144665ff5d4a8bbef1936e
Patch0:		%{name}-makefile.patch
URL:		http://dev.gentoo.org/~spock/projects/gensplash/
BuildRequires:	freetype-static
BuildRequires:	libjpeg-static
BuildRequires:	libpng-static
BuildRequires:	zlib-static
BuildRequires:	glibc-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for setting fbsplash.

%description -l pl
Narzêdzia do ustawiania fbsplash.

%prep
%setup -q -n %{name}-%{version}-%{_pre} -a1
find . -name CVS | xargs rm -rf 
%patch0 -p1

rm -rf lib/jpeg*
rm -rf lib/libpng*
rm -rf lib/zlib*

%build
install -d linux/include
ln -sf %{_kernelsrcdir}/include/linux linux/include/linux
ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} linux/include/asm
ln -sf %{_kernelsrcdir}/include/asm-generic linux/include/asm-generic
%{__make} splash_kern splash_user
%{__make} -C miscsplashutils-%{_misc_ver} \
        CFLAGS="%{rpmcflags} -I/usr/include/freetype2"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/splash
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install miscsplashutils-%{_misc_ver}/{fbres,fbtruetype/{fbtruetype,fbtruetype.static}} $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README docs/*
%dir %{_sysconfdir}/splash
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /sbin/*
