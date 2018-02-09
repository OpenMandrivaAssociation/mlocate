Summary:	An utility for finding files by name via a central database
Name:		mlocate
Version:	0.26
Release:	16
License:	GPLv2+
Group:		File tools
Url:		http://fedorahosted.org/mlocate/
Source0:	http://fedorahosted.org/releases/m/l/mlocate/%{name}-%{version}.tar.xz
Source1:	updatedb.conf
Source2:	updatedb.timer
Source3:	updatedb.service
Requires(pre):	shadow
Requires(post):	rpm-helper

%description
Mlocate is a locate/updatedb implementation.  It keeps a database of
all existing files and allows you to lookup files by name.

The 'm' stands for "merging": updatedb reuses the existing database to avoid
rereading most of the file system, which makes updatedb faster and does not
trash the system caches as much as traditional locate implementations.

%prep
%setup -q

%build
%configure \
	--localstatedir=%{_localstatedir}/lib \
	--disable-rpath

%make

%check
make check

%install
%makeinstall_std

# install config file:
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/updatedb.conf

# for %ghost:
touch %{buildroot}%{_localstatedir}/lib/mlocate/mlocate.db

install -D -m644 %{SOURCE2} %{buildroot}%{_unitdir}/updatedb.timer
install -D -m644 %{SOURCE3} %{buildroot}%{_unitdir}/updatedb.service

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-updatedb.preset << EOF
enable updatedb.timer
EOF

%find_lang %{name}

%pre
if [ $1 -eq 1 ]; then
    if ! getent group mlocate >/dev/null 2>&1; then
	/usr/sbin/groupadd -r -f mlocate 2>/dev/null || :
    fi
elif [ $1 -eq 2 ]; then
    if grep	slocate	%{_sysconfdir}/group > /dev/null; then
	%{_sbindir}/groupmod -n mlocate slocate
    fi
fi

%post
%create_ghostfile %{_localstatedir}/lib/mlocate/mlocate.db root mlocate 0640

%files -f %{name}.lang
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/updatedb.conf
%{_presetdir}/86-updatedb.preset
%attr(2711,root,mlocate) %{_bindir}/locate
%{_bindir}/updatedb
%{_mandir}/man*/*
%{_unitdir}/updatedb.timer
%{_unitdir}/updatedb.service
%dir %attr(0750,root,mlocate) /var/lib/mlocate
%ghost %attr(0640,root,mlocate) %{_localstatedir}/lib/mlocate/mlocate.db

