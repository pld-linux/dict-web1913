%define		dictname web1913
%define		dictversion 0.46-a
Summary:	Webster's Revised Unabridged Dictionary for dictd
Summary(pl):	S³ownik Webster's Revised Unabridged Dictionary dla dictd
Name:		dict-%{dictname}
Version:	1.4
Release:	6
License:	Free for personal or research use, distributable
Group:		Applications/Dictionaries
Source0:	ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
# Source0-md5:	3b1eda03a3eb12d5d0f857bd990d7ab5
Source1:	ftp://ftp.dict.org/pub/dict/%{dictname}-%{dictversion}.tar.gz
# Source1-md5:	e957fe5b670cabb48b1c3b43998084ae
Patch0:		%{name}-ac.patch
Patch1:		%{name}-sparc.patch
URL:		http://www.dict.org/
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	dictzip
BuildRequires:	flex
Requires:	dictd
Requires:	%{_sysconfdir}/dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Webster's Revised Unabridged Dictionary (1913).

%description -l pl
S³ownik Webstera (angielsko-angielski): Webster's Revised Unabridged
Dictionary (1913).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
cd libmaa
%{__autoconf}
cd ..
%configure \
	--with-local-libmaa \
	--with-datapath=%{dictname}-%{dictversion}
%{__make}
tar xfz %{SOURCE1}
%{__make} db

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}
#make install dictdir="$RPM_BUILD_ROOT%{_datadir}/dictd"

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# Webster's Revised Unabridged Dictionary
database %{dictname} {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf
mv %{dictname}.{dict.dz,index} $RPM_BUILD_ROOT%{_datadir}/dictd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
