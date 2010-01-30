%define	lib_name_orig	libxfs
%define	lib_major	1
%define	lib_name	%mklibname xfs %{lib_major}
%define	lib_name_devel	%mklibname xfs -d
%define	lib_name_static_devel	%mklibname xfs -d -s

Name:		xfsprogs
Version:	3.1.1
Release:	%manbo_mkrel 1
Summary:	Utilities for managing the XFS filesystem
Source0:	ftp://oss.sgi.com/projects/xfs/cmd_tars//%{name}-%{version}.tar.gz
Patch1:		xfsprogs-2.9.8-fix-underlinking.patch
Patch2:		xfsprogs-2.10.2-format_not_a_string_literal_and_no_format_arguments.diff
License:	GPLv2 and LGPLv2
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libext2fs-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
URL:		http://oss.sgi.com/projects/xfs/
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

%package -n	%{lib_name}
Summary:	Main library for %{lib_name_orig}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{lib_name_orig}.

%package -n	%{lib_name_devel}
Summary:	XFS filesystem-specific libraries and headers
Group:		Development/C
Requires:	%{lib_name} = %{version}
# For uuid/uuid.h included in /usr/include/xfs/linux.h
Requires:	libuuid-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	xfs-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	xfs-devel < %{version}-%{release}
Obsoletes:      %{lib_name}-devel < %{version}-%{release}

%description -n	%{lib_name_devel}
%{lib_name_devel} contains the libraries and header files needed to
develop XFS filesystem-specific programs.

You should install %{lib_name_devel} if you want to develop XFS
filesystem-specific programs, If you install %{lib_name_devel}, you'll
also want to install xfsprogs.

%package -n	%{lib_name_static_devel}
Summary:	XFS filesystem-specific static libraries
Group:		Development/C
Requires:	%{lib_name_devel} = %{version}
Provides:	%{lib_name_orig}-static-devel = %{version}-%{release}
Provides:	xfs-static-devel = %{version}-%{release}

%description -n	%{lib_name_static_devel}
%{lib_name_devel} contains the static libraries needed to
develop XFS filesystem-specific programs.

You should install %{lib_name_static_devel} if you want to develop XFS
filesystem-specific programs, If you install %{lib_name_static_devel}, you'll
also want to install xfsprogs.

%prep
%setup -q
#patch0 -p1 -b .enable-lazy-count
%patch1 -p1 -b .underlinking
%patch2 -p0 -b .format_not_a_string_literal_and_no_format_arguments

%build
export DEBUG="-DNDEBUG"
export OPTIMIZER="%{optflags}"

%configure2_5x \
		--libdir=/%{_lib} \
		--libexecdir=%{_libdir} \
		--sbindir=/sbin \
		--bindir=/usr/sbin \
		--enable-gettext=yes \
		--enable-editline=no \
		--enable-shared=yes

make DEBUG=-DNDEBUG OPTIMIZER="%{optflags}"

%install
rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/

# nuke files already packaged as %doc
rm -r %{buildroot}%{_datadir}/doc/xfsprogs/
%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING doc/CREDITS README
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

%files -n %{lib_name}
%defattr(-,root,root)
%doc README
/%{_lib}/*.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%doc README
/%{_lib}/*.so
/%{_lib}/*.la
%{_includedir}/xfs
%{_mandir}/man3/*

%files -n %{lib_name_static_devel}
%defattr(-,root,root)
/%{_lib}/*.a
