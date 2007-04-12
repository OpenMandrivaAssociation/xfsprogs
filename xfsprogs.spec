%define	name	xfsprogs
%define	version	2.8.18
%define	release	%mkrel 1

%define	lib_name_orig	libxfs
%define	lib_major	1
%define	lib_name	%mklibname xfs %{lib_major}

Summary:	Utilities for managing the XFS filesystem
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.bz2
License:	GPL
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libext2fs-devel
BuildRequires:	libreadline-devel
BuildRequires:	libtermcap-devel
BuildRequires:	libtool
Prereq:		/sbin/ldconfig
URL:		http://oss.sgi.com/projects/xfs/
Requires:	common-licenses

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

%package -n	%{lib_name}-devel
Summary:	XFS filesystem-specific static libraries and headers
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	xfs-devel = %{version}-%{release}
Obsoletes:	xfs-devel


%description -n	%{lib_name}-devel
%{lib_name}-devel contains the libraries and header files needed to
develop XFS filesystem-specific programs.

You should install %{lib_name}-devel if you want to develop XFS
filesystem-specific programs, If you install %{lib_name}-devel, you'll
also want to install xfsprogs.

%prep
%setup -q

# make it lib64 aware, better make a patch?
perl -pi -e "/(libuuid|pkg_s?lib_dir)=/ and s|/lib\b|/%{_lib}|;" configure

%build
aclocal && autoconf
%configure2_5x \
		--libdir=/%{_lib} \
		--libexecdir=%{_libdir} \
		--sbindir=/sbin \
		--bindir=/usr/sbin \
		--enable-gettext=yes \
		--enable-readline=yes \
		--enable-editline=no \
		--enable-termcap=yes \
		--enable-shared=yes \
		--enable-shared-uuid=yes
%make DEBUG=-DNDEBUG OPTIMIZER="${RPM_OPT_FLAGS}"

%install
rm -rf $RPM_BUILD_ROOT
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/

# nuke files already packaged as %doc
rm -rf %{buildroot}%{_datadir}/doc/xfsprogs/
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING doc/CREDITS README
%{_sbindir}/xfs_admin
%{_sbindir}/xfs_bmap
%{_sbindir}/xfs_check
%{_sbindir}/xfs_copy
%{_sbindir}/xfs_db
%{_sbindir}/xfs_freeze
%{_sbindir}/xfs_growfs
%{_sbindir}/xfs_info
%{_sbindir}/xfs_io
%{_sbindir}/xfs_logprint
%{_sbindir}/xfs_mkfile
%{_sbindir}/xfs_ncheck
%{_sbindir}/xfs_quota
%{_sbindir}/xfs_rtcp
/sbin/fsck.xfs
/sbin/mkfs.xfs
/sbin/xfs_repair
%{_mandir}/man[85]/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc README
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc/PORTING README
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*so
%{_libdir}/*a
%{_includedir}/xfs
%{_includedir}/disk
%{_mandir}/man3/*


