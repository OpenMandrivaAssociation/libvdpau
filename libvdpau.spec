
%define name	libvdpau
%define version	0.1
%define snap	20090221
%define rel	1

%define major	1
%define libname	%mklibname vdpau %major
%define devname	%mklibname vdpau -d
%define tracename %mklibname vdpau-trace

Summary:	Video Decode and Presentation API for Unix
Name:		%{name}
Version:	%{version}
Release:	%mkrel 0.%snap.%rel
License:	MIT
Group:		System/Libraries
URL:		http://www.nvnews.net/vbulletin/showthread.php?t=123091
# rm -rf libvdpau && git clone git://anongit.freedesktop.org/~aplattner/libvdpau && cd libvdpau/
# git archive --prefix=libvdpau-$(date +%Y%m%d)/ --format=tar HEAD | lzma > ../libvdpau-$(date +%Y%m%d).tar.lzma
Source0:	libvdpau-%{snap}.tar.lzma
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	libx11-devel

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
%setup -q -n %name-%snap

%build
autoreconf -if
export LIBS=-ldl
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libvdpau.so.%{major}*

%files -n %tracename
%defattr(-,root,root)
%{_libdir}/libvdpau_trace.so

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/vdpau
%{_libdir}/libvdpau.so
%{_libdir}/pkgconfig/vdpau.pc

