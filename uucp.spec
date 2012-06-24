Summary:	GNU uucp
Summary(de):	GNU-uucp
Summary(es):	Uucp de la GNU
Summary(fr):	uucp de GNU
Summary(pl):	GNU uucp
Summary(pt_BR):	Uucp da GNU
Summary(ru):	GNU uucp
Summary(tr):	GNU uucp sistemi
Summary(uk):	GNU uucp
Name:		uucp
Version:	1.06.2
Release:	4
License:	GPL
Group:		Networking
URL:		http://lists.cirr.com/cgi-bin/wilma/taylor-uucp/
Source0:	ftp://prep.ai.mit.edu/pub/gnu/uucp/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.inetd
Source3:	%{name}.crontab
Source4:	%{name}-non-english-man-pages.tar.bz2
Patch0:		%{name}-misc.patch
Patch1:		%{name}-debian.patch
Patch2:		%{name}-buggy_autoconf.patch
Patch3:		%{name}-ac.patch
Patch4:		%{name}-security.patch
Patch5:		%{name}-lock.patch
Patch6:		%{name}-pipe.patch
Patch7:		%{name}-no_libnsl.patch
BuildRequires:	autoconf
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UUCP is a Unix to Unix transfer mechanism. It is used primarily for
remote sites to download and upload email and news files to local
machines. If you didn't already know that, you probably don't need
this package installed. :-)

%description -l de
UUCP ist ein Unix-nach-Unix-�bertragungsprotokoll. Es wird vor allem
verwendet, um E-Mail- und News-Dateien von entfernten auf lokale
Rechner herunter- bzw. umgekehrt hochzuladen. Wie Sie wahrscheinlich
wissen, m�ssen Sie das Paket wahrscheinlich nicht installieren. :-)

%description -l es
UUCP es un mecanismo de transferencia de Unix para Unix. Se usa
primeramente en sitios remotos para hacer download y upload de
archivos de mail y news para m�quinas locales. Si no lo sabias,
probablemente no necesitas de este paquete instalado. :-)

%description -l fr
UUCP est un m�canisme de transfert d'UNIX � UNIX. Il est
principalement utilis�s par les sites de connexion pour t�l�charger ou
envoyer des courriers �l�ctroniques et des nouvelles sur les machines
locales. Si vous ne saviez pas d�ja cela, vous n'avez probablement pas
besoin d'insatller ce package.

%description -l pl
UUCP (Unix to Unix Copy Protocol) jest jednym z podstawowych
protoko��w systemu Linux. U�ywany jest przede wszystkim do wysy�ania i
pobierania przesy�ek news�w oraz poczty elektronicznej m�dzy maszynami
po��czonymi np. przez modem.

%description -l pt_BR
UUCP � um mecanismo de transfer�ncia de Unix para Unix. Ele � usado
primeiramente em sites remotos para fazer download e upload de
arquivos de mail e news para m�quinas locais. Se voc� n�o sabia disso,
voc� provavelmente n�o precisa deste pacote instalado. :-)

%description -l ru
UUCP - ��� �������� �������� ������ ����� UNIX-���������. � ��������
������������ ��� ������ ������ � ����������������� ����� ��������.
���� �� ����� �� �����, ��� ���� ����� �� ����� :-))

%description -l tr
UUCP bir Unix'ten Unix'e iletim mekanizmas�d�r. Uzak sitelerden yerel
sisteme e-posta ve haber �bekleri aktar�m� i�in kullan�l�r. Bunun ne
oldu�unu bilmiyorsan�z, b�y�k olas�l�kla i�inize de yaramayacakt�r.
:-)

%description -l uk
UUCP - �� ����Φ�� ������ަ ���̦� ͦ� UNIX-���������. ���¦������
����������դ���� ��� ��ͦ�� ������ �� ������������æ��� ͦ� ��������.
���� �� ����� �� �����, ��� ��� ����� �� ���Ҧ��� :-))

%package server
Summary:	GNU uucp server
Summary(de):	GNU-uucp
Summary(fr):	uucp de GNU
Summary(pl):	Serwer GNU uucp
Group:		Networking
Requires:	%{name} = %{version}

%description server
GNU uucp server.

%description server -l pl
Serwer GNU uucp.

%prep
%setup -q -n uucp-1.06.1
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

find . -name "*.perlpath" | xargs rm -f

%build
%{__autoconf}
%configure

%{__make} clean; make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8},%{_infodir}} \
	$RPM_BUILD_ROOT{%{_libdir}/uucp,/var/{lock/uucp,spool/{uucp,uucppublic}}} \
	$RPM_BUILD_ROOT/var/log/{uucp,archiv/uucp} \
$RPM_BUILD_ROOT%{_sysconfdir}/{uucp/oldconfig,sysconfig/rc-inetd,cron.d,logrotate.d}

%{__make} install install-info \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	man1dir=$RPM_BUILD_ROOT%{_mandir}/man1 \
	man8dir=$RPM_BUILD_ROOT%{_mandir}/man8 \
	owner=`id -u`

gzip -9nf sample/*

ln -sf ../../sbin/uucico $RPM_BUILD_ROOT%{_libdir}/uucp/uucico

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/uucp
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/uucp
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/uucp
bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

# Create empty files
for n in Log Stats Debug; do
	touch $RPM_BUILD_ROOT/var/log/uucp/$n
done

for i in dial passwd port dialcode sys call ; do
cat > $RPM_BUILD_ROOT%{_sysconfdir}/uucp/$i <<EOF
# This is an example of a $i file. This file have the syntax compatible
# with Taylor UUCP (not HDB, not anything else). Please check uucp
# documentation if you are not sure how Taylor config files are supposed to
# look like. Edit it as appropriate for your system.

# Everything after a '#' character is a comment.
EOF
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post server
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun server
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog MANIFEST NEWS sample contrib

%attr(750,uucp,root) %dir %{_sysconfdir}/uucp
%attr(755,uucp,root) %dir %{_sysconfdir}/uucp/oldconfig

%attr(640,uucp,root) %config %verify(not size mtime md5) %{_sysconfdir}/uucp/ca*
%attr(640,uucp,root) %config %verify(not size mtime md5) %{_sysconfdir}/uucp/di*
%attr(640,uucp,root) %config %verify(not size mtime md5) %{_sysconfdir}/uucp/p*
%attr(640,uucp,root) %config %verify(not size mtime md5) %{_sysconfdir}/uucp/sys

%attr(640,root,root) %config /etc/logrotate.d/uucp

%attr(4554,uucp,uucp) %{_bindir}/cu
%attr(4554,uucp,uucp) %{_bindir}/uucp
%attr(0755,root,root) %{_bindir}/uulog
%attr(4554,uucp,uucp) %{_bindir}/uuname
%attr(0755,root,root) %{_bindir}/uupick
%attr(4554,uucp,uucp) %{_bindir}/uustat
%attr(0755,root,root) %{_bindir}/uuto
%attr(4554,uucp,uucp) %{_bindir}/uux

%{_infodir}/uucp.*

%attr(755,root,root) %dir %{_libdir}/uucp
%attr(755,root,root) %{_libdir}/uucp/uucico

%{_mandir}/man[18]/*
%lang(fi) %{_mandir}/fi/man[18]/*
%lang(ja) %{_mandir}/ja/man[18]/*
%lang(pl) %{_mandir}/pl/man[18]/*

%attr(0755,uucp,uucp) %{_sbindir}/uuchk
%attr(4554,uucp,uucp) %{_sbindir}/uucico
%attr(0755,uucp,uucp) %{_sbindir}/uuconv
%attr(0755,root,root) %{_sbindir}/uusched
%attr(4554,uucp,uucp) %{_sbindir}/uuxqt

%attr(755,uucp,uucp) %dir /var/spool/uucppublic
%attr(755,uucp,uucp) %dir /var/spool/uucp

%attr(750,uucp,root) %dir /var/log/uucp
%attr(750,uucp,root) %dir /var/log/archiv/uucp
%attr(750,uucp,root) %dir /var/lock/uucp
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Debug
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Log
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Stats

%files server
%defattr(644,root,root,755)
%attr(640,root,root) %config /etc/sysconfig/rc-inetd/uucp
