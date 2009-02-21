
%define name	vdpau
%define version	0
%define docsnap	3032807
%define	inclver	180.16
%define rel	1

%define major	1
%define libname	%mklibname vdpau %major
%define devname	%mklibname vdpau -d

Summary:	Video Decode and Presentation API for Unix
Name:		%{name}
Version:	%{version}
Release:	%mkrel 0.%inclver.%rel
License:	MIT
Group:		System/Libraries
URL:		http://www.nvnews.net/vbulletin/showthread.php?t=123091
Source0:	ftp://download.nvidia.com/XFree86/vdpau/vdpau-docs-%{docsnap}.tar.bz2
# Newer than the one in vdpau-docs:
Source1:	vdpau-includes-nvidia-180.16.tar.bz2
# Generic version of VDPAU, only reports "no implementation" error:
Source2:	vdpau-stub.c
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	doxygen
BuildRequires:	libx11-devel

%description
The Video Decode and Presentation API for Unix (VDPAU) provides a
complete solution for decoding, post-processing, compositing, and
displaying compressed or uncompressed video streams. These video
streams may be combined (composited) with bitmap content, to
implement OSDs and other application user interfaces.

Only the proprietary NVIDIA driver supports this interface so far.

%package -n %libname
Summary:	VDPAU wrapper shared library
Group:		System/Libraries

%description -n %libname
The Video Decode and Presentation API for Unix (VDPAU) wrapper shared
library. This generic version does not support any hardware.

%package -n %devname
Summary:	VDPAU development headers and documentation
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Provides:	vdpau-devel = %{version}-%{release}

%description -n %devname
The Video Decode and Presentation API for Unix (VDPAU) provides a
complete solution for decoding, post-processing, compositing, and
displaying compressed or uncompressed video streams. These video
streams may be combined (composited) with bitmap content, to
implement OSDs and other application user interfaces.

Only the proprietary NVIDIA driver supports this interface so far.

This package contains the VDPAU headers and documentation for
developing software that uses VDPAU.

%prep
%setup -q -c -a 1
cp %{SOURCE2} .
cp -afv vdpau include

%build
gcc -shared -fPIC %{optflags} %{?ldflags} -Iinclude \
  -o libvdpau.so.1 -Wl,-soname=libvdpau.so.1 vdpau-stub.c
doxygen/doxygen.sh

%install
rm -rf %{buildroot}
install -d -m755 %{buildroot}%{_includedir}/vdpau
install -m644 include/vdpau/*.h %{buildroot}%{_includedir}/vdpau

install -d -m755 %{buildroot}%{_libdir}
install -m755 libvdpau.so.1 %{buildroot}%{_libdir}
ln -s libvdpau.so.1 %{buildroot}%{_libdir}/libvdpau.so

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libvdpau.so.%{major}*

%files -n %{devname}
%defattr(-,root,root)
%doc doxygen/html/*
%{_includedir}/vdpau
%{_libdir}/libvdpau.so
