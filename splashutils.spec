%define		pre	pre10
Summary:	Utilities for setting fbsplash
Summary(pl):	Narzêdzia do ustawiania fbsplash
Name:		splashutils
Version:	0.9
Release:	%{pre}.1
Epoch:		0
License:	GPL
Group:		-
Source0:	http://dev.gentoo.org/~spock/projects/gensplash/current/%{name}-%{version}-%{pre}.tar.bz2
URL:		http://dev.gentoo.org/~spock/projects/gensplash/
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
%setup -q -n %{name}-%{version}-%{pre}

%build
install -d linux/include
ln -sf %{_kernelsrcdir}/include/linux linux/include/linux
ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} linux/include/asm
ln -sf %{_kernelsrcdir}/include/asm-generic linux/include/asm-generic
%{__make} splash_kern splash_user

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /sbin/*
