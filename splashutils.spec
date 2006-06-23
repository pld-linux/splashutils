#
Summary:	Utilities for setting fbsplash
Summary(pl):	Narzêdzia do ustawiania fbsplash
Name:		splashutils
Version:	1.1.9.10
Release:	1
License:	GPL
Group:		System
Source0:	http://dev.gentoo.org/~spock/projects/gensplash/current/%{name}-%{version}.tar.bz2
# Source0-md5:	af1230e0f1bda32b519a6accf6ade734
Patch0:		%{name}-jpeg_scale.patch
URL:		http://dev.gentoo.org/~spock/projects/gensplash/
BuildRequires:	libjpeg-devel
BuildRequires:	linux-libc-headers >= 7:2.6.9.1-1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities for setting fbsplash.

%description -l pl
Narzêdzia do ustawiania fbsplash.

%prep
%setup -q
%patch0 -p1
cat > Makefile << 'EOF'
PKG_VERSION = %{version}

CFLAGS	= -Os
LDLIBS	= -ljpeg

all:	splash_helper splash_util

K_OBJS	= $(addprefix kernel/,kernel.o dev.o parse.o render.o image.o \
		cmd.o common.o list.o effects.o)

splash_helper:	$(K_OBJS)
	$(CC) $(LDFLAGS) $(LDLIBS) -o $@ $^

kernel/%.o:	%.c config.h splash.h
	$(CC) $(CFLAGS) -DTARGET_KERNEL -c -o $@ $<

OBJS	= splash.o parse.o render.o image.o cmd.o common.o daemon.o list.o \
	effects.o

splash_util:	$(OBJS)
	$(CC) $(LDFLAGS) $(LDLIBS) -o $@ $+

%.o:	%.c config.h splash.h
	$(CC) $(CFLAGS) -DPKG_VERSION=\"$(PKG_VERSION)\" -c -o $@ $<
EOF

cat > config.h << 'EOF'
#define CONFIG_FBSPLASH
#define THEME_DIR 	"%{_sysconfdir}/splash"
#define SPLASH_FIFO	"%{_sysconfdir}/splash/.fifo"
EOF

sed -i 's@"libs/jpeg-6b/jpeglib.h"@<jpeglib.h>@' \
	image.c

rm -rf libs

%build
mkdir kernel
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/splash,/sbin}

install splash_helper $RPM_BUILD_ROOT/sbin
install splash_util $RPM_BUILD_ROOT/sbin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README docs/*
%dir %{_sysconfdir}/splash
%attr(755,root,root) /sbin/*
