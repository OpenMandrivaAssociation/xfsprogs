%define _disable_ld_no_undefined 1

%define	major	1

%define	oldlib	%mklibname xfs %{major}
%define	olddev	%mklibname xfs -d
%define	oldstat	%mklibname xfs -d -s

%define	libname	%mklibname handle %{major}
%define	devname	%mklibname handle -d
%define	statname %mklibname handle -d -s

%bcond_without	uclibc

Summary:	Utilities for managing the XFS filesystem
Name:		xfsprogs
Version:	3.2.0
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/cmd_tars/%{name}-%{version}.tar.gz
Patch1:		xfsprogs-2.9.8-fix-underlinking.patch
Patch2:		xfsprogs-3.2.0-uclibc.patch
Patch4:		xfsprogs-use-posix-signal-api.patch

BuildRequires:	libtool
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(uuid)
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-16
%endif
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

%package -n	uclibc-%{name}
Summary:	Utilities for managing the XFS filesystem (uClibc build)
Group:		System/Kernel and hardware

%description -n	uclibc-%{name}
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

%package -n	uclibc-%{libname}
Summary:	Main library for xfsprogs (uClibc build)
Group:		System/Libraries
License:	LGPLv2.1+

%description -n	uclibc-%{libname}
This package contains the library needed to run programs dynamically
linked with libhandle.

%package -n	%{devname}
Summary:	XFS filesystem-specific libraries and headers
Group:		Development/C
License:	LGPLv2.1+
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}
%endif
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

%if %{with uclibc}
mkdir .uclibc
pushd .uclibc
cp -a ../* .
popd
%endif

%build
%if %{with uclibc}
pushd .uclibc
export DEBUG="-DNDEBUG"

%uclibc_configure \
		OPTIMIZER="%{uclibc_cflags}" \
		--libdir=%{uclibc_root}/%{_lib} \
		--prefix=%{uclibc_root} \
		--exec-prefix=%{uclibc_root} \
		--libexecdir=%{uclibc_root}%{_libdir} \
		--sbindir=%{uclibc_root}/sbin \
		--enable-gettext=yes \
		--enable-static \
		--enable-editline=no \
		--enable-shared=yes \
		--enable-readline=yes

%make DEBUG=-DNDEBUG || make DEBUG=-DNDEBUG 
popd
%endif

export DEBUG="-DNDEBUG"
export OPTIMIZER="%{optflags}"

%configure2_5x	--libdir=/%{_lib} \
		--libexecdir=%{_libdir} \
		--sbindir=/sbin \
		--bindir=/usr/sbin \
		--enable-gettext=yes \
		--enable-static \
		--enable-editline=no \
		--enable-shared=yes \
		--enable-readine=yes

make DEBUG=-DNDEBUG OPTIMIZER="%{optflags}"

%install
%if %{with uclibc}
make -C .uclibc install DIST_ROOT=%{buildroot}
make -C .uclibc install-dev DIST_ROOT=%{buildroot}
install -d %{buildroot}%{uclibc_root}%{_libdir}
rm %{buildroot}%{uclibc_root}/%{_lib}/libhandle.so
ln -sr %{buildroot}/%{uclibc_root}/%{_lib}/libhandle.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libhandle.so
mv %{buildroot}%{uclibc_root}/%{_lib}/libhandle.a %{buildroot}%{uclibc_root}%{_libdir}/libhandle.a
chmod +x %{buildroot}/%{uclibc_root}/%{_lib}/libhandle.so.%{major}*
%endif

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
%doc doc/CHANGES.gz doc/CREDITS README
/sbin/xfs_admin
/sbin/xfs_bmap
/sbin/xfs_check
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
%{_mandir}/man[85]/*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/sbin/xfs_admin
%{uclibc_root}/sbin/xfs_bmap
%{uclibc_root}/sbin/xfs_check
%{uclibc_root}/sbin/xfs_copy
%{uclibc_root}/sbin/xfs_db
%{uclibc_root}/sbin/xfs_freeze
%{uclibc_root}/sbin/xfs_growfs
%{uclibc_root}/sbin/xfs_info
%{uclibc_root}/sbin/xfs_io
%{uclibc_root}/sbin/xfs_logprint
%{uclibc_root}/sbin/xfs_mkfile
%{uclibc_root}/sbin/xfs_ncheck
%{uclibc_root}/sbin/xfs_quota
%{uclibc_root}/sbin/xfs_rtcp
%{uclibc_root}/sbin/xfs_mdrestore
%{uclibc_root}/sbin/xfs_metadump
%{uclibc_root}/sbin/xfs_estimate
%{uclibc_root}/sbin/xfs_fsr

%{uclibc_root}/sbin/fsck.xfs
%{uclibc_root}/sbin/mkfs.xfs
%{uclibc_root}/sbin/xfs_repair
%endif

%files -n %{libname}
%doc README
/%{_lib}/libhandle.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libhandle.so.%{major}*
%endif

%files -n %{devname}
%doc README
%{_libdir}/libhandle.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libhandle.so
%endif
%{_includedir}/xfs
%{_mandir}/man3/*

%files -n %{statname}
%{_libdir}/libhandle.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libhandle.a
%endif
