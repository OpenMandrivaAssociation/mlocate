Summary:	An utility for finding files by name via a central database
Name:		mlocate
Version:	0.23.1
Release:	%mkrel 3
License:	GPLv2+
Group:		File tools
URL:		http://fedorahosted.org/mlocate/
Source0:	http://fedorahosted.org/releases/m/l/mlocate/%{name}-%{version}.tar.xz
Source1:	updatedb.conf
Source2:	mlocate.cron
Requires(pre):	shadow-utils
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
	--localstatedir=%{_localstatedir}/lib \
	--disable-rpath

%make groupname=slocate

%install
rm -rf %{buildroot}
%makeinstall_std groupname=slocate

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
%{_sbindir}/groupadd -r -f slocate 

%post
# for %ghost:
touch %{_localstatedir}/lib/mlocate/mlocate.db

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/updatedb.conf
%{_sysconfdir}/cron.daily/mlocate.cron
%attr(2711,root,slocate) %{_bindir}/locate
%{_bindir}/updatedb
%{_mandir}/man*/*
%dir %attr(0750,root,slocate) /var/lib/mlocate
%ghost %{_localstatedir}/lib/mlocate/mlocate.db
