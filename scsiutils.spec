Summary:	SCSI utilities
Summary(pl):	Narzêdzia do SCSI
Name:		scsiutils
Version:	1.7.2.10.000207
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	scsiinfo-1.7.tar.gz
Source1:	http://www.torque.net/sg/p/sg_utils000207.tgz
Source2:	http://www.garloff.de/kurt/linux/scsidev/scsidev-2.10.tar.gz
Source3:	http://www.garloff.de/kurt/linux/rescan-scsi-bus.sh
Patch0:		scsiinfo-glibc.patch
Patch1:		scsiinfo-makefile.patch
Patch2:		scsiinfo-misc.patch
Patch3:		scsiinfo-tmpdir.patch
Patch4:		sg_utils-makefile.patch
Patch5:		sg_utils-misc.patch
Patch6:		scsidev-makefile.patch
BuildRequires:	tk-devel
Provides:	scsiinfo sg_utils scsidev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A collection of useful tools for users of SCSI systems:
- scsiinfo: Allows to access some internals of SCSI devices, such as
  defect lists or the so-called mode pages, which control e.g. the
  behaviour of the device's cache or error management.
- scsiformat: A low-level formatting tool for SCSI disks.
- scsidev: If your SCSI config changes from time to time, e.g. because
  you have external devices which are not always switched on or
  connected then the kernel's mapping to the device nodes is not always
  the way you would expect it. This program creates a mapping which
  remains unchanged in most of these cases.
- rescan-scsi-bus.sh: Script that scans the SCSI bus and dynamicaaly
  adds (and optionally removes) devices.
- sg_utils: A colection of small useful tools, that are baysed on the
  sg interface and give info on the SCSI bus, copy data, ... Warning:
  Some of these tools access the internals of your system and a wrong
  usage of them may render your system inoperational. Note: scsiinfo
  comes with a graphical user interface which can be found in the xscsi
  package.

%package tk
Summary:	Tk graphical frontend for scsiinfo
Summary(pl):	Graficzny frontend do scsiinfo oparty o Tk
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje
Requires:	%{name} = %{version}
Requires:	tk

%description tk
For visualization and manipulation of SCSI mode pages, scsiinfo comes
with graphical interface.

%prep
%setup -q -c -a1 -a2
cd scsiinfo-1.7
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd ../sg_utils
%patch4 -p1
%patch5 -p1
cd ../scsidev-2.10
%patch6 -p1

%build
cd scsiinfo-1.7
%{__make} clean
%{__make} OPT="%{rpmcflags}"

cd ../scsidev-2.10
%configure
%{__make}

cd ../sg_utils
mv -f README README.sg
%{__make} OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_bindir},%{_libdir}/scsi,%{_mandir}/man8}

cd scsiinfo-1.7
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ../scsidev-2.10
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bindir=/sbin

install %{SOURCE3} $RPM_BUILD_ROOT/sbin/rescan-scsi-bus

cd ../sg_utils
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

gunzip $RPM_BUILD_ROOT%{_mandir}/man8/*.gz
gzip -9nf scsiinfo-1.7/{0-CHANGES,0-README.first,0-TODO} \
	scsidev-2.10/{boot.diff,CHANGES,README,TODO} \
	sg_utils/README.sg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc scsiinfo-1.7/{0-CHANGES,0-README.first,0-TODO}.gz
%doc scsidev-2.10/{boot.diff,CHANGES,README,TODO}.gz
%doc sg_utils/README.sg.gz
%attr(755,root,root) /sbin/scsidev
%attr(755,root,root) /sbin/rescan-scsi-bus
%attr(755,root,root) %{_sbindir}/sgcheck
%attr(755,root,root) %{_bindir}/scsiinfo
%attr(755,root,root) %{_bindir}/scsiformat
%attr(755,root,root) %{_bindir}/sg_poll
%attr(755,root,root) %{_bindir}/sg_dd512
%attr(755,root,root) %{_bindir}/sgq_dd512
%attr(755,root,root) %{_bindir}/sgp_dd 
%attr(755,root,root) %{_bindir}/sg_dd2048
%attr(755,root,root) %{_bindir}/sg_whoami
%attr(755,root,root) %{_bindir}/sg_inquiry
%attr(755,root,root) %{_bindir}/sg_tst_med
%attr(755,root,root) %{_bindir}/sg_debug
%attr(755,root,root) %{_bindir}/sg_scan 
%attr(755,root,root) %{_bindir}/sg_rbuf
%attr(755,root,root) %{_bindir}/sg_runt_ex
%attr(755,root,root) %{_bindir}/sg_simple1 
%attr(755,root,root) %{_bindir}/sg_simple2
%attr(755,root,root) %{_bindir}/sg_readcap
%attr(755,root,root) %{_bindir}/sg_map 
%attr(755,root,root) %{_bindir}/sg_test_rwbuf
%attr(755,root,root) %{_bindir}/scsi_inquiry 
%attr(755,root,root) %{_bindir}/sginfo
%{_mandir}/man8/scsiinfo.8*
%{_mandir}/man8/scsiformat.8*
%{_mandir}/man8/scsidev.8*

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scsi-config
%attr(755,root,root) %{_bindir}/tk_scsiformat
%dir %{_libdir}/scsi
%{_libdir}/scsi/generic
%attr(755,root,root) %{_libdir}/scsi/cache
%attr(755,root,root) %{_libdir}/scsi/control
%attr(755,root,root) %{_libdir}/scsi/disconnect
%attr(755,root,root) %{_libdir}/scsi/error
%attr(755,root,root) %{_libdir}/scsi/format
%attr(755,root,root) %{_libdir}/scsi/inquiry
%attr(755,root,root) %{_libdir}/scsi/notch
%attr(755,root,root) %{_libdir}/scsi/overview
%attr(755,root,root) %{_libdir}/scsi/peripheral
%attr(755,root,root) %{_libdir}/scsi/rigid
%attr(755,root,root) %{_libdir}/scsi/save-changes
%attr(755,root,root) %{_libdir}/scsi/save-file
%attr(755,root,root) %{_libdir}/scsi/tworands
%attr(755,root,root) %{_libdir}/scsi/verify
%{_mandir}/man8/tk_scsiformat.8*
%{_mandir}/man8/scsi-config.8*
