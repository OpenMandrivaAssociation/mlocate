Summary:	An utility for finding files by name via a central database
Name:		mlocate
Version:	0.24
Release:	%mkrel 5
License:	GPLv2+
Group:		File tools
URL:		http://fedorahosted.org/mlocate/
Source0:	http://fedorahosted.org/releases/m/l/mlocate/%{name}-%{version}.tar.xz
Source1:	updatedb.conf
Source2:	mlocate.cron
Requires(pre):	shadow-utils

%description
Mlocate is a locate/updatedb implementation.  It keeps a database of
all existing files and allows you to lookup files by name.

The 'm' stands for "merging": updatedb reuses the existing database to avoid
rereading most of the file system, which makes updatedb faster and does not
trash the system caches as much as traditional locate implementations.

%prep
%setup -q

%build
%configure2_5x \
	--localstatedir=%{_localstatedir}/lib \
	--disable-rpath

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# install config file:
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/updatedb.conf

# install daily cron entry:
install -D -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.daily/mlocate.cron

# for %ghost:
touch %{buildroot}%{_localstatedir}/lib/mlocate/mlocate.db

%find_lang %{name}

%clean
rm -rf %{buildroot}

%pre
if [ "$1" = "1" ]; then
	%{_sbindir}/groupadd -r -f mlocate
elif [ "$1" = "2" ]; then
	if grep	slocate	%{_sysconfdir}/group > /dev/null; then
		%{_sbindir}/groupmod -n mlocate slocate
	fi
fi

%post
# for %ghost:
touch %{_localstatedir}/lib/mlocate/mlocate.db

%check
make check

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/updatedb.conf
%{_sysconfdir}/cron.daily/mlocate.cron
%attr(2711,root,mlocate) %{_bindir}/locate
%{_bindir}/updatedb
%{_mandir}/man*/*
%dir %attr(0750,root,mlocate) /var/lib/mlocate
%ghost %{_localstatedir}/lib/mlocate/mlocate.db


%changelog
* Tue Feb 21 2012 abf
- The release updated by ABF

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.24-4mdv2011.0
+ Revision: 666467
- mass rebuild

* Fri Apr 01 2011 Jani Välimaa <wally@mandriva.org> 0.24-3
+ Revision: 649699
- fix group renaming (rename only when group slocate exists)

* Fri Apr 01 2011 Jani Välimaa <wally@mandriva.org> 0.24-2
+ Revision: 649689
- use mlocate group instead of slocate
- rename slocate group to mlocate when updating
- drop buildroot definition

* Fri Apr 01 2011 Jani Välimaa <wally@mandriva.org> 0.24-1
+ Revision: 649680
- new version 0.24
- enable build time check

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.23.1-4
+ Revision: 640331
- rebuild to obsolete old packages

* Tue Jan 18 2011 Jani Välimaa <wally@mandriva.org> 0.23.1-3
+ Revision: 631452
- properly fix (mdv#51740)

* Tue Jan 11 2011 Jani Välimaa <wally@mandriva.org> 0.23.1-2
+ Revision: 630950
- remove old obsoletes, provides and triggerpostun
- don't index cifs (mdv#51740)
- clean .spec a bit

* Sun Oct 03 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.23.1-1mdv2011.0
+ Revision: 582712
- update to new version 0.23.1

* Sat Sep 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.23-1mdv2011.0
+ Revision: 575980
- update to new version 0.23

* Sun Mar 28 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.22.4-2mdv2010.1
+ Revision: 528473
- rebuild
- update to 0.22.4

* Sun Mar 21 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0.22.3-1mdv2010.1
+ Revision: 526116
- update to new version 0.22.3

* Mon Nov 09 2009 Thierry Vignaud <tv@mandriva.org> 0.22.2-1mdv2010.1
+ Revision: 463780
- new release

* Tue Sep 15 2009 Frederik Himpe <fhimpe@mandriva.org> 0.22.1-1mdv2010.0
+ Revision: 443300
- update to new version 0.22.1

* Sat May 09 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.22-1mdv2010.0
+ Revision: 373856
- update to new version 0.22

* Fri Feb 27 2009 Gustavo De Nardin <gustavodn@mandriva.com> 0.21.1-4mdv2009.1
+ Revision: 345688
- get rid of pointless and weird bashism

* Fri Nov 21 2008 Pascal Terjan <pterjan@mandriva.org> 0.21.1-3mdv2009.1
+ Revision: 305487
- Don't index tmpfs

* Tue Nov 18 2008 Pascal Terjan <pterjan@mandriva.org> 0.21.1-2mdv2009.1
+ Revision: 304249
- List /afs only once
- Don't index sysfs and debugfs

* Tue Oct 28 2008 Frederik Himpe <fhimpe@mandriva.org> 0.21.1-1mdv2009.1
+ Revision: 298017
- Update to new version 0.21.1

* Tue Sep 30 2008 Thierry Vignaud <tv@mandriva.org> 0.21-2mdv2009.0
+ Revision: 290112
- run with io priority set as idle (prevent mad access if anacron starts it in
  the middle of the day)

* Wed Jul 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.21-1mdv2009.0
+ Revision: 230771
- update to new version 0.21
- update url
- new license policy
- do not package COPYING file
- spec file clean

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.20-2mdv2009.0
+ Revision: 219507
- really update db with decreased I/O priority at night (#41458)

* Mon Apr 14 2008 Thierry Vignaud <tv@mandriva.org> 0.20-1mdv2009.0
+ Revision: 192895
- new release

* Mon Mar 03 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.19-1mdv2008.1
+ Revision: 177953
- update to new version 0.19

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.18-3mdv2008.1
+ Revision: 153142
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Sep 24 2007 Thierry Vignaud <tv@mandriva.org> 0.18-2mdv2008.0
+ Revision: 92526
- run updatedb with ionice -c0

* Sat Aug 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.18-1mdv2008.0
+ Revision: 71195
- spec file clean
- nuke rpath
- new version

* Thu May 03 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0.17-1mdv2008.0
+ Revision: 21309
- Updated to 0.17.

* Fri Apr 20 2007 Thierry Vignaud <tv@mandriva.org> 0.16-1mdv2008.0
+ Revision: 16118
- new release


* Fri Nov 24 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.15-2mdv2007.0
+ Revision: 87061
- fix update (#27313)

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.15-1mdv2007.1
+ Revision: 86827
- Import mlocate

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.15-1mdv2007.1
- new release

* Wed Sep 20 2006 Pixel <pixel@mandriva.com> 0.14-5mdv2007.0
- add explicit conflicts with slocate

* Sun Sep 17 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.14-4mdv2007.0
- don't upgrade from slocate (#25338)

* Wed Aug 09 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.14-3mdv2007.0
- revert 2mdk, readd trigger, needed for updates (#24220

* Sun Aug 06 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.14-2mdv2007.0
- remove uneeded trigger

* Sat Aug 05 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.14-1mdv2007.0
- initial release (with ideas from rh)

