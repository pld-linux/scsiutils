%define	sg_utils_ver	0.97
%define	scsidev_ver	2.10
%define	scsiinfo_ver	1.7
Summary:	SCSI utilities
Summary(pl):	Narzêdzia do SCSI
Name:		scsiutils
Version:	%{scsiinfo_ver}.%{scsidev_ver}.%{sg_utils_ver}
Release:	1
Epoch:		1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://tsx-11.mit.edu/pub/linux/ALPHA/scsi/scsiinfo-%{scsiinfo_ver}.tar.gz
Source1:	http://www.torque.net/sg/p/sg_utils-%{sg_utils_ver}.tgz
Source2:	http://www.garloff.de/kurt/linux/scsidev/scsidev-%{scsidev_ver}.tar.gz
Source3:	http://www.garloff.de/kurt/linux/rescan-scsi-bus.sh
Patch0:		scsiinfo-glibc.patch
Patch1:		scsiinfo-makefile.patch
Patch2:		scsiinfo-misc.patch
Patch3:		scsiinfo-tmpdir.patch
Patch4:		sg_utils-makefile.patch
Patch5:		scsidev-makefile.patch
BuildRequires:	autoconf
BuildRequires:	automake
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
- sg_utils: A colection of small useful tools, that are based on the
  sg interface and give info on the SCSI bus, copy data... Warning: Some
  of these tools access the internals of your system and a wrong usage
  of them may render your system inoperational.

Note: scsiinfo comes with a graphical user interface which can be
found in the scsiutils-tk package.

%description -l pl
Zestaw u¿ytecznych narzêdzi dla u¿ytkowników systemów SCSI:
- scsiinfo: pozwala na dostêp do niektórych informacji wewnêtrznych
  SCSI, takich jak listy defektów, strony trybów (kontroluj±cych
  zachowanie cache urz±dzenia i obs³ugê b³êdów).
- scsiformat: narzêdzie do niskopoziomowego formatowania dysków SCSI.
- scsidev: je¿eli Twoja konfiguracja SCSI zmienia siê, np. poniewa¿
  masz urz±dzenia zewnêtrzne nie zawsze pod³±czone lub w³±czone,
  mapowania j±dra dotycz±ce urz±dzeñ SCSI nie s± takie same. Ten program
  tworzy mapowanie nie zmieniaj±ce siê w wiêkszo¶ci przypadków.
- rescan-scsi-bus.sh: skrypt skanuj±cy szynê SCSI i dynamicznie
  dodaj±cy (opcjonalnie tak¿e usuwaj±cy) urz±dzenia.
- sg_utils: zestaw ma³ych narzêdzi bazuj±cych na interfejsie sg
  udostêpniaj±cych informacje o szynie SCSI, kopiuj±cych dane... Uwaga:
  czê¶æ z nich u¿ywa dostêpu do wnêtrzno¶ci systemu i z³e ich u¿ycie
  mo¿e uczyniæ system niedzia³aj±cym.

Dostêpny jest interfejs graficzny do scsiinfo - znajduje siê w
pakiecie scsiutils-tk.

%package tk
Summary:	Tk graphical frontend for scsiinfo
Summary(pl):	Graficzny frontend do scsiinfo oparty o Tk
Group:		X11/Applications
Requires:	%{name} = %{version}
Requires:	tk

%description tk
For visualization and manipulation of SCSI mode pages, scsiinfo comes
with graphical interface.

%description tk -l pl
Graficzny interfejs do scsiinfo - do wizualizacji i manipulowania
stronami trybów SCSI.

%prep
%setup -q -c -a1 -a2
cd scsiinfo-%{scsiinfo_ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd ../sg_utils-%{sg_utils_ver}
%patch4 -p1
cd ../scsidev-%{scsidev_ver}
%patch5 -p1

%build
cd scsiinfo-%{scsiinfo_ver}
%{__make} clean
%{__make} OPT="%{rpmcflags}"

cd ../scsidev-%{scsidev_ver}
%{__aclocal}
%{__autoconf}
%configure
%{__make}

cd ../sg_utils-%{sg_utils_ver}
mv -f README README.sg
%{__make} OPT="%{rpmcflags}" PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_bindir},%{_libdir}/scsi,%{_mandir}/man8}

cd scsiinfo-%{scsiinfo_ver}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ../scsidev-%{scsidev_ver}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bindir=/sbin

install %{SOURCE3} $RPM_BUILD_ROOT/sbin/rescan-scsi-bus

cd ../sg_utils-%{sg_utils_ver}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix}
cd ..

gunzip $RPM_BUILD_ROOT%{_mandir}/man8/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc scsiinfo-%{scsiinfo_ver}/{0-CHANGES,0-README.first,0-TODO}
%doc scsidev-%{scsidev_ver}/{boot.diff,CHANGES,README,TODO}
%doc sg_utils-%{sg_utils_ver}/{README.sg,README.sg_start,CHANGELOG}
%attr(755,root,root) /sbin/scsidev
%attr(755,root,root) /sbin/rescan-scsi-bus
%attr(755,root,root) %{_sbindir}/sgcheck
%attr(755,root,root) %{_bindir}/scsiformat
%attr(755,root,root) %{_bindir}/scsiinfo
%attr(755,root,root) %{_bindir}/scsi_inquiry
%attr(755,root,root) %{_bindir}/sginfo
%attr(755,root,root) %{_bindir}/sgp_dd
%attr(755,root,root) %{_bindir}/sg_dd
%attr(755,root,root) %{_bindir}/sg_debug
%attr(755,root,root) %{_bindir}/sg_inq
%attr(755,root,root) %{_bindir}/sg_map
%attr(755,root,root) %{_bindir}/sg_rbuf
%attr(755,root,root) %{_bindir}/sg_read
%attr(755,root,root) %{_bindir}/sg_readcap
%attr(755,root,root) %{_bindir}/sg_runt_ex
%attr(755,root,root) %{_bindir}/sg_scan
%attr(755,root,root) %{_bindir}/sg_simple1
%attr(755,root,root) %{_bindir}/sg_simple2
%attr(755,root,root) %{_bindir}/sg_start
%attr(755,root,root) %{_bindir}/sg_test_rwbuf
%attr(755,root,root) %{_bindir}/sg_turs
%attr(755,root,root) %{_bindir}/sg_whoami
%{_mandir}/man8/scsidev.8*
%{_mandir}/man8/scsiformat.8*
%{_mandir}/man8/scsiinfo.8*
%{_mandir}/man8/sg_dd.8*
%{_mandir}/man8/sg_map.8*
%{_mandir}/man8/sg_rbuf.8*
%{_mandir}/man8/sgp_dd.8*
#%attr(755,root,root) %{_bindir}/sg_poll
#%attr(755,root,root) %{_bindir}/sg_dd512
#%attr(755,root,root) %{_bindir}/sgq_dd512
#%attr(755,root,root) %{_bindir}/sg_dd2048
#%attr(755,root,root) %{_bindir}/sg_tst_med

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scsi-config
%attr(755,root,root) %{_bindir}/tk_scsiformat
%dir %{_libdir}/scsi
%attr(755,root,root) %{_libdir}/scsi/cache
%attr(755,root,root) %{_libdir}/scsi/control
%attr(755,root,root) %{_libdir}/scsi/disconnect
%attr(755,root,root) %{_libdir}/scsi/error
%attr(755,root,root) %{_libdir}/scsi/format
%attr(644,root,root) %{_libdir}/scsi/generic
%attr(755,root,root) %{_libdir}/scsi/inquiry
%attr(755,root,root) %{_libdir}/scsi/notch
%attr(755,root,root) %{_libdir}/scsi/overview
%attr(755,root,root) %{_libdir}/scsi/peripheral
%attr(755,root,root) %{_libdir}/scsi/rigid
%attr(755,root,root) %{_libdir}/scsi/save-changes
%attr(755,root,root) %{_libdir}/scsi/save-file
%attr(755,root,root) %{_libdir}/scsi/tworands
%attr(755,root,root) %{_libdir}/scsi/verify
%{_mandir}/man8/scsi-config.8*
%{_mandir}/man8/tk_scsiformat.8*
