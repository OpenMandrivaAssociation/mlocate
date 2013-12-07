Summary:	An utility for finding files by name via a central database
Name:		mlocate
Version:	0.26
Release:	7
License:	GPLv2+
Group:		File tools
Url:		http://fedorahosted.org/mlocate/
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
%makeinstall_std

# install config file:
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/updatedb.conf

# install daily cron entry:
install -D -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.daily/mlocate.cron

# for %ghost:
touch %{buildroot}%{_localstatedir}/lib/mlocate/mlocate.db

%find_lang %{name}

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
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/updatedb.conf
%{_sysconfdir}/cron.daily/mlocate.cron
%attr(2711,root,mlocate) %{_bindir}/locate
%{_bindir}/updatedb
%{_mandir}/man*/*
%dir %attr(0750,root,mlocate) /var/lib/mlocate
%ghost %{_localstatedir}/lib/mlocate/mlocate.db

