%define		dictname web1913
%define		dictversion 0.46-a
Summary:	Webster's Revised Unabridged Dictionary for dictd
Summary(pl.UTF-8):	Słownik Webster's Revised Unabridged Dictionary dla dictd
Name:		dict-%{dictname}
Version:	1.4
Release:	9
License:	Free for personal or research use, distributable
Group:		Applications/Dictionaries
Source0:	ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
# Source0-md5:	3b1eda03a3eb12d5d0f857bd990d7ab5
Source1:	ftp://ftp.dict.org/pub/dict/%{dictname}-%{dictversion}.tar.gz
# Source1-md5:	e957fe5b670cabb48b1c3b43998084ae
Patch0:		%{name}-ac.patch
Patch1:		%{name}-sparc.patch
Patch2:		%{name}-gcc.patch
URL:		http://www.dict.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	dictzip
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{_sysconfdir}/dictd
Requires:	dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Webster's Revised Unabridged Dictionary (1913).

%description -l pl.UTF-8
Słownik Webstera (angielsko-angielski): Webster's Revised Unabridged
Dictionary (1913).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
cp -f /usr/share/automake/config.* .
cd libmaa
%{__autoconf}
cp -f /usr/share/automake/config.* .
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
%service -q dictd restart

%postun
if [ "$1" = 0 ]; then
	%service -q dictd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
