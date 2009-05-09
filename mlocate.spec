Summary:	An utility for finding files by name via a central database
Name:		mlocate
Version:	0.22
Release:	%mkrel 1
License:	GPLv2+
Group:		File tools
URL:		http://fedorahosted.org/mlocate/
Source0:	http://fedorahosted.org/releases/m/l/mlocate/%{name}-%{version}.tar.bz2
Source1:	updatedb.conf
Source2:	mlocate.cron
Requires(pre):	shadow-utils
Requires(triggerpostun):	shadow-utils
Requires(post):	grep, sed
Obsoletes:	slocate <= 3.1
Provides:	slocate = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
	--localstatedir=/var/lib \
	--disable-rpath

%make groupname=slocate

%install
rm -rf %{buildroot}
%makeinstall_std groupname=slocate

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
# install config file:
install -c -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/updatedb.conf
# install daily cron entry:
install -c -m 755 %{SOURCE2} %{buildroot}/etc/cron.daily/mlocate.cron
# for %ghost:
touch %{buildroot}/var/lib/mlocate/mlocate.db

%find_lang %{name}

%clean
rm -rf %{buildroot}

# for smooth updates:
%triggerpostun -- slocate <= 3.1
%{_sbindir}/groupadd -r -f slocate

%pre
%{_sbindir}/groupadd -r -f slocate 

%post
# for %ghost:
touch /var/lib/mlocate/mlocate.db

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/updatedb.conf
%{_sysconfdir}/cron.daily/mlocate.cron
%attr(2711,root,slocate) %{_bindir}/locate
%{_bindir}/updatedb
%{_mandir}/man*/*
%dir %attr(0750,root,slocate) /var/lib/mlocate
%ghost /var/lib/mlocate/mlocate.db
