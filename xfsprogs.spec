%define _disable_ld_no_undefined 1

%define	major	1

%define	oldlib	%mklibname xfs %{major}
%define	olddev	%mklibname xfs -d
%define	oldstat	%mklibname xfs -d -s

%define	xcmd	%mklibname xcmd  %{major}

%define	libname	%mklibname handle %{major}
%define	devname	%mklibname handle -d
%define	statname %mklibname handle -d -s

Summary:	Utilities for managing the XFS filesystem
Name:		xfsprogs
Version:	4.14.0
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	https://www.kernel.org/pub/linux/utils/fs/xfs/xfsprogs/xfsprogs-%{version}.tar.xz
Patch0:		xfsprogs-4.7.0-libxcmd-link.patch

BuildRequires:	libtool
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(blkid)
Requires:	common-licenses
Conflicts:	xfsdump < 3.0.0

%description
A set of commands to use the XFS filesystem, including mkfs.xfs.

XFS is a high performance journaling filesystem which originated
on the SGI IRIX platform.  It is completely multi-threaded, can
support large files and large filesystems, extended attributes,
variable block sizes, is extent based, and makes extensive use of
Btrees (directories, extents, free space) to aid both performance
and scalability.

Refer to the documentation at http://oss.sgi.com/projects/xfs/
for complete details.  This implementation is on-disk compatible
with the IRIX version of XFS.

%package -n	%{libname}
Summary:	Main library for xfsprogs
Group:		System/Libraries
License:	LGPLv2.1+
%rename		%{oldlib}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libhandle.

%package -n	%{devname}
Summary:	XFS filesystem-specific libraries and headers
Group:		Development/C
License:	LGPLv2.1+
Requires:	%{libname} = %{EVRD}
# For uuid/uuid.h included in /usr/include/xfs/linux.h
Requires:	libuuid-devel
%rename		%{olddev}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
%{devname} contains the libraries and header files needed to
develop XFS filesystem-specific programs.

You should install %{devname} if you want to develop XFS
filesystem-specific programs, If you install %{devname}, you'll
also want to install xfsprogs.

%package -n	%{statname}
Summary:	XFS filesystem-specific static libraries
Group:		Development/C
License:	LGPLv2.1+
Requires:	%{devname} = %{version}
%rename		%{oldstat}
Provides:	%{name}-static-devel = %{EVRD}

%description -n	%{statname}
%{devname} contains the static libraries needed to
develop XFS filesystem-specific programs.

You should install %{statname} if you want to develop XFS
filesystem-specific programs, If you install %{statname}, you'll
also want to install xfsprogs.

%prep
%setup -q
%apply_patches
aclocal -I m4
autoconf

%build
export DEBUG="-DNDEBUG"
export OPTIMIZER="%{optflags}"

%configure	--libdir=/%{_lib} \
		--libexecdir=%{_libdir} \
		--sbindir=/sbin \
		--bindir=/usr/sbin \
		--enable-gettext=yes \
		--enable-static \
		--enable-editline=no \
		--enable-shared=yes \
		--enable-readine=yes

%make DEBUG=-DNDEBUG OPTIMIZER="%{optflags}"

%install
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/

install -d %{buildroot}%{_libdir}
rm %{buildroot}/%{_lib}/libhandle.so
ln -sr %{buildroot}/%{_lib}/libhandle.so.%{major}.* %{buildroot}%{_libdir}/libhandle.so
mv %{buildroot}/%{_lib}/libhandle.a %{buildroot}%{_libdir}/libhandle.a
chmod +x %{buildroot}/%{_lib}/libhandle.so.%{major}*

# nuke files already packaged as %doc
rm -r %{buildroot}%{_datadir}/doc/xfsprogs/
%find_lang %{name}

%files -f %{name}.lang
%doc doc/CREDITS README
/sbin/xfs_admin
/sbin/xfs_bmap
# /sbin/xfs_check
/sbin/xfs_copy
/sbin/xfs_db
/sbin/xfs_freeze
/sbin/xfs_growfs
/sbin/xfs_info
/sbin/xfs_io
/sbin/xfs_logprint
/sbin/xfs_mkfile
/sbin/xfs_ncheck
/sbin/xfs_quota
/sbin/xfs_rtcp
/sbin/xfs_mdrestore
/sbin/xfs_metadump
/sbin/xfs_estimate
/sbin/xfs_fsr
/sbin/fsck.xfs
/sbin/mkfs.xfs
/sbin/xfs_repair
/sbin/xfs_spaceman
%{_mandir}/man[85]/*

%files -n %{libname}
/%{_lib}/libhandle.so.%{major}*

%files -n %{devname}
%{_libdir}/libhandle.so
%{_includedir}/xfs
%{_mandir}/man3/*

%files -n %{statname}
%{_libdir}/libhandle.a
