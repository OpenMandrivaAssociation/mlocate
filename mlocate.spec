Summary:  An utility for finding files by name via a central database
Name:     mlocate
Version:  0.16
Release:  %mkrel 1
License:  GPL
Group:    File tools
URL:      http://carolina.mff.cuni.cz/~trmac/blog/mlocate/
Source0:  %name-%version.tar.bz2
Source1:  updatedb.conf
Source2:  mlocate.cron
BuildRoot: %_tmppath/%name-%version-root
Requires(pre): shadow-utils
Requires(triggerpostun): shadow-utils
Requires(post): grep, sed
Obsoletes: slocate <= 3.1
Provides: slocate = %version

%description
Mlocate is a locate/updatedb implementation.  It keeps a database of
all existing files and allows you to lookup files by name.

The 'm' stands for "merging": updatedb reuses the existing database to avoid
rereading most of the file system, which makes updatedb faster and does not
trash the system caches as much as traditional locate implementations.

%prep
%setup -q

%build
%configure --localstatedir=/var/lib
%make groupname=slocate

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT groupname=slocate

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/cron.daily
# install config file:
install -c -m 644 %SOURCE1 $RPM_BUILD_ROOT%_sysconfdir/updatedb.conf
# install daily cron entry:
install -c -m 755 %SOURCE2 $RPM_BUILD_ROOT/etc/cron.daily/mlocate.cron
# for %ghost:
touch $RPM_BUILD_ROOT/var/lib/mlocate/mlocate.db

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

# for smooth updates:
%triggerpostun -- slocate <= 3.1
%_sbindir/groupadd -r -f slocate

%pre
%_sbindir/groupadd -r -f slocate 

%post
# for %ghost:
touch /var/lib/mlocate/mlocate.db

%files -f mlocate.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%config(noreplace) %_sysconfdir/updatedb.conf
%_sysconfdir/cron.daily/mlocate.cron
%attr(2711,root,slocate) %_bindir/locate
%_bindir/updatedb
%_mandir/man*/*
%dir %attr(0750,root,slocate) /var/lib/mlocate
%ghost /var/lib/mlocate/mlocate.db


