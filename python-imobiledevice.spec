#
# Conditional build:
%bcond_without	openssl		# OpenSSL for SSL support
%bcond_with	gnutls		# GnuTLS for SSL support

%if %{with gnutls}
%undefine	with_openssl
%endif
Summary:	libimobiledevice Python 2 bindings
Summary(pl.UTF-8):	Wiązania libimobiledevice dla Pythona 2
Name:		python-imobiledevice
Version:	1.3.0
Release:	11
License:	LGPL v2+
Group:		Development/Languages/Python
#Source0Download: https://www.libimobiledevice.org/
Source0:	https://github.com/libimobiledevice/libimobiledevice/releases/download/%{version}/libimobiledevice-%{version}.tar.bz2
# Source0-md5:	c50a3a32acf33dc8c9ec88137ad12ec4
Patch0:		libimobiledevice-cython.patch
Patch1:		libimobiledevice-system-library.patch
URL:		https://libimobiledevice.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
%{?with_gnutls:BuildRequires:	gnutls-devel >= 2.2.0}
BuildRequires:	libgcrypt-devel
BuildRequires:	libimobiledevice-devel >= 1.3.0
BuildRequires:	libplist-devel >= 2.3.0
BuildRequires:	libplist-c++-devel >= 2.3.0
BuildRequires:	libstdc++-devel
%{?with_gnutls:BuildRequires:	libtasn1-devel >= 1.1}
BuildRequires:	libtool
BuildRequires:	libusbmuxd-devel >= 2.0.2
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.8}
BuildRequires:	pkgconfig
BuildRequires:	python-Cython >= 0.17.0
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-modules >= 1:2.3
BuildRequires:	python-plist-devel >= 2.2.0
BuildRequires:	rpmbuild(macros) >= 2.043
BuildRequires:	rpm-pythonprov
Requires:	libimobiledevice >= 1.3.0
Requires:	python-plist >= 2.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libimobiledevice Python 2 bindings.

%description -l pl.UTF-8
Wiązania libimobiledevice dla Pythona 2.

%prep
%setup -q -n libimobiledevice-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CYTHON=/usr/bin/cython2 \
	PYTHON=%{__python} \
	%{!?with_openssl:--disable-openssl} \
	--disable-silent-rules \
	--disable-static

%{__make} -C cython

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C cython install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%{py_sitedir}/imobiledevice.so
