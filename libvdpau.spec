# vdpau is used by mesa, mesa is used by wine and steam
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 1
%define libname %mklibname vdpau %{major}
%define devname %mklibname vdpau -d
%define libtrace %mklibname vdpau_trace %{major}
%define lib32name %mklib32name vdpau %{major}
%define dev32name %mklib32name vdpau -d
%define lib32trace %mklib32name vdpau_trace %{major}
%global optflags %{optflags} -O3

%ifarch %armx %riscv
%bcond_without bootstrap
%else
%bcond_with bootstrap
%endif

Summary:	Video Decode and Presentation API for Unix
Name:		libvdpau
Version:	1.5
Release:	1
License:	MIT
Group:		System/Libraries
Url:		http://cgit.freedesktop.org/~aplattner/libvdpau
Source0:	https://gitlab.freedesktop.org/vdpau/libvdpau/-/archive/%{version}/libvdpau-%{version}.tar.bz2

%if %{without bootstrap}
# for apidoc:
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	texlive
%endif
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	meson
%if %{with compat32}
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
%endif

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	VDPAU shared library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
The Video Decode and Presentation API for Unix (VDPAU) wrapper shared
library. This library is responsible for loading the hardware-specific
VDPAU driver.

%package -n %{lib32trace}
Summary:	VDPAU tracing module for debugging (32-bit)
Group:		Development/X11

%description -n %{lib32trace}
VDPAU tracing module libvdpau_trace.so for debugging VDPAU.

%package -n %{dev32name}
Summary:	VDPAU development headers (32-bit)
Group:		Development/X11
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32trace} = %{version}-%{release}

%description -n %{dev32name}
This package contains the VDPAU headers for developing software that
uses VDPAU.
%endif

%prep
%autosetup -p1
%if %{with compat32}
%meson32
%endif
%meson

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
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

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libvdpau.so.%{major}*

%files -n %{lib32trace}
%dir %{_prefix}/lib/vdpau
%{_prefix}/lib/vdpau/libvdpau_trace.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libvdpau.so
%{_prefix}/lib/vdpau/libvdpau_trace.so
%{_prefix}/lib/pkgconfig/vdpau.pc
%endif
