
%define name	libvdpau
%define version	0.4.1
%define snap	0
%define rel	1

%define major	1
%define libname	%mklibname vdpau %major
%define devname	%mklibname vdpau -d
%define tracename %mklibname vdpau-trace

Summary:	Video Decode and Presentation API for Unix
Name:		%{name}
Version:	%{version}
%if %snap
Release:	%mkrel 0.%snap.%rel
%else
Release:	%mkrel %rel
%endif
License:	MIT
Group:		System/Libraries
URL:		http://www.nvnews.net/vbulletin/showthread.php?t=123091
%if %snap
# rm -rf libvdpau && git clone git://anongit.freedesktop.org/~aplattner/libvdpau && cd libvdpau/
# git archive --prefix=libvdpau-$(date +%Y%m%d)/ --format=tar HEAD | xz > ../libvdpau-$(date +%Y%m%d).tar.xz
Source0:	libvdpau-%{snap}.tar.xz
%else
Source0:	http://people.freedesktop.org/~aplattner/vdpau/libvdpau-%{version}.tar.gz
%endif
BuildRoot:	%{_tmppath}/%{name}-root
Patch0:		libvdpau-0.4.1-fix-X11-underlinking.patch
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
# for apidoc:
BuildRequires:	tetex graphviz doxygen

%description
The Video Decode and Presentation API for Unix (VDPAU) provides a
complete solution for decoding, post-processing, compositing, and
displaying compressed or uncompressed video streams. These video
streams may be combined (composited) with bitmap content, to
implement OSDs and other application user interfaces.

Only the proprietary NVIDIA driver supports this interface so far.

%package -n %libname
Summary:	VDPAU shared library
Group:		System/Libraries

%description -n %libname
The Video Decode and Presentation API for Unix (VDPAU) wrapper shared
library. This library is responsible for loading the hardware-specific
VDPAU driver.

%package -n %tracename
Summary:	VDPAU tracing module for debugging
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}

%description -n %tracename
VDPAU tracing module libvdpau_trace.so for debugging VDPAU.

%package -n %devname
Summary:	VDPAU development headers
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Provides:	vdpau-devel = %{version}-%{release}

%description -n %devname
This package contains the VDPAU headers for developing software that
uses VDPAU.

%prep
%if %snap
%setup -q -n %name-%snap
%else
%setup -q
%endif

%patch0 -p1

%build
%if %snap
autoreconf -if
%endif
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# (anssi) unneeded files
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/vdpau/*.{la,so}
mv %{buildroot}%{_docdir}/libvdpau/html api-html

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libvdpau.so.%{major}*
%dir %{_libdir}/vdpau

%files -n %tracename
%defattr(-,root,root)
# major is the plugin interface version, not %major
%{_libdir}/vdpau/libvdpau_trace.so.*

%files -n %{devname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog api-html
%{_includedir}/vdpau
%{_libdir}/libvdpau.so
%{_libdir}/pkgconfig/vdpau.pc

