%define	scsiinfo_ver	1.7
Summary:	SCSI utilities
Summary(pl.UTF-8):	Narzędzia do SCSI
Name:		scsiutils
Version:	%{scsiinfo_ver}
Release:	2
Epoch:		1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://tsx-11.mit.edu/pub/linux/ALPHA/scsi/scsiinfo-%{scsiinfo_ver}.tar.gz
# Source0-md5:	1d7a9a42e84430d14b2fbfee342a950c
Source3:	http://www.garloff.de/kurt/linux/rescan-scsi-bus.sh
# Source3-md5:	794f4c8f35a6036b8ae1e1310f46353b
Patch0:		scsiinfo-glibc.patch
Patch1:		scsiinfo-makefile.patch
Patch2:		scsiinfo-misc.patch
Patch3:		scsiinfo-tmpdir.patch
BuildRequires:	tk-devel
# sg_turs and sg_inq commands used by rescan-scsi-bus.sh
Requires:	sg3_utils
Suggests:	scsidev
Provides:	scsiinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	%{_prefix}/lib

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
- rescan-scsi-bus.sh: Script that scans the SCSI bus and dynamically
  adds (and optionally removes) devices.

Note: scsiinfo comes with a graphical user interface which can be
found in the scsiutils-tk package.

%description -l pl.UTF-8
Zestaw użytecznych narzędzi dla użytkowników systemów SCSI:
- scsiinfo: pozwala na dostęp do niektórych informacji wewnętrznych
  SCSI, takich jak listy defektów, strony trybów (kontrolujących
  zachowanie cache urządzenia i obsługę błędów).
- scsiformat: narzędzie do niskopoziomowego formatowania dysków SCSI.
- scsidev: jeżeli Twoja konfiguracja SCSI zmienia się, np. ponieważ
  masz urządzenia zewnętrzne nie zawsze podłączone lub włączone,
  mapowania jądra dotyczące urządzeń SCSI nie są takie same. Ten program
  tworzy mapowanie nie zmieniające się w większości przypadków.
- rescan-scsi-bus.sh: skrypt skanujący szynę SCSI i dynamicznie
  dodający (opcjonalnie także usuwający) urządzenia.

Dostępny jest interfejs graficzny do scsiinfo - znajduje się w
pakiecie scsiutils-tk.

%package tk
Summary:	Tk graphical frontend for scsiinfo
Summary(pl.UTF-8):	Graficzny frontend do scsiinfo oparty o Tk
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	tk

%description tk
For visualization and manipulation of SCSI mode pages, scsiinfo comes
with graphical interface.

%description tk -l pl.UTF-8
Graficzny interfejs do scsiinfo - do wizualizacji i manipulowania
stronami trybów SCSI.

%prep
%setup -q -c -a2
cd scsiinfo-%{scsiinfo_ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd scsiinfo-%{scsiinfo_ver}
%{__make} clean
%{__make} \
	CC="%{__cc} -DCONFIG_BLOCK=1" \
	LDFLAGS="%{rpmldflags}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_bindir},%{_ulibdir}/scsi,%{_mandir}/man8}

%{__make} -C scsiinfo-%{scsiinfo_ver} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE3} $RPM_BUILD_ROOT/sbin/rescan-scsi-bus

gunzip $RPM_BUILD_ROOT%{_mandir}/man8/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc scsiinfo-%{scsiinfo_ver}/{0-CHANGES,0-README.first,0-TODO}
%attr(755,root,root) /sbin/rescan-scsi-bus
%attr(755,root,root) %{_sbindir}/sgcheck
%attr(755,root,root) %{_bindir}/scsiformat
%attr(755,root,root) %{_bindir}/scsiinfo
%attr(755,root,root) %{_bindir}/scsi_inquiry
%attr(755,root,root) %{_bindir}/sginfo
%attr(755,root,root) %{_bindir}/sgp_dd
%{_mandir}/man8/scsiformat.8*
%{_mandir}/man8/scsiinfo.8*

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scsi-config
%attr(755,root,root) %{_bindir}/tk_scsiformat
%dir %{_ulibdir}/scsi
%attr(755,root,root) %{_ulibdir}/scsi/cache
%attr(755,root,root) %{_ulibdir}/scsi/control
%attr(755,root,root) %{_ulibdir}/scsi/disconnect
%attr(755,root,root) %{_ulibdir}/scsi/error
%attr(755,root,root) %{_ulibdir}/scsi/format
%{_ulibdir}/scsi/generic
%attr(755,root,root) %{_ulibdir}/scsi/inquiry
%attr(755,root,root) %{_ulibdir}/scsi/notch
%attr(755,root,root) %{_ulibdir}/scsi/overview
%attr(755,root,root) %{_ulibdir}/scsi/peripheral
%attr(755,root,root) %{_ulibdir}/scsi/rigid
%attr(755,root,root) %{_ulibdir}/scsi/save-changes
%attr(755,root,root) %{_ulibdir}/scsi/save-file
%attr(755,root,root) %{_ulibdir}/scsi/tworands
%attr(755,root,root) %{_ulibdir}/scsi/verify
%{_mandir}/man8/scsi-config.8*
%{_mandir}/man8/tk_scsiformat.8*
