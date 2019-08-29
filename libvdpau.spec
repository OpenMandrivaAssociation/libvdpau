%define major 1
%define libname %mklibname vdpau %{major}
%define devname %mklibname vdpau -d
%define libtrace %mklibname vdpau_trace %{major}
%global optflags %{optflags} -O3

%ifarch %armx %riscv
%bcond_without bootstrap
%else
%bcond_with bootstrap
%endif

Summary:	Video Decode and Presentation API for Unix
Name:		libvdpau
Version:	1.3
Release:	1
License:	MIT
Group:		System/Libraries
Url:		http://cgit.freedesktop.org/~aplattner/libvdpau
#Source0:	http://people.freedesktop.org/~aplattner/vdpau/libvdpau-%{version}.tar.bz2
Source0:  https://gitlab.freedesktop.org/vdpau/libvdpau/-/archive/%{version}/libvdpau-%{version}.tar.bz2

%if %{without bootstrap}
# for apidoc:
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	texlive
%endif
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:  meson

%description
The Video Decode and Presentation API for Unix (VDPAU) provides a
complete solution for decoding, post-processing, compositing, and
displaying compressed or uncompressed video streams. These video
streams may be combined (composited) with bitmap content, to
implement OSDs and other application user interfaces.

%package -n %{libname}
Summary:	VDPAU shared library
Group:		System/Libraries

%description -n %{libname}
The Video Decode and Presentation API for Unix (VDPAU) wrapper shared
library. This library is responsible for loading the hardware-specific
VDPAU driver.

%package -n %{libtrace}
Summary:	VDPAU tracing module for debugging
Group:		Development/X11
Obsoletes:	%{_lib}vdpau-trace < 0.6-2

%description -n %{libtrace}
VDPAU tracing module libvdpau_trace.so for debugging VDPAU.

%package -n %{devname}
Summary:	VDPAU development headers
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libtrace} = %{version}-%{release}
Provides:	vdpau-devel = %{version}-%{release}

%description -n %{devname}
This package contains the VDPAU headers for developing software that
uses VDPAU.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%if ! %{with bootstrap}
# (anssi) unneeded files
mv %{buildroot}%{_docdir}/libvdpau/html api-html
%endif

%files -n %{libname}
%config(noreplace) %{_sysconfdir}/vdpau_wrapper.cfg
%{_libdir}/libvdpau.so.%{major}*

%files -n %{libtrace}
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau_trace.so.%{major}*

%files -n %{devname}
%doc AUTHORS
%if ! %{with bootstrap}
%doc api-html
%endif
%{_includedir}/vdpau
%{_libdir}/libvdpau.so
%{_libdir}/vdpau/libvdpau_trace.so
%{_libdir}/pkgconfig/vdpau.pc
