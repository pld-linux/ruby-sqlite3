%define		pkgname	sqlite3
Summary:	SQLite3 module for Ruby
Summary(pl.UTF-8):	Moduł SQLite3 dla Ruby
Name:		ruby-sqlite3
Version:	1.3.9
Release:	3
License:	GPL
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	7b7d8efe8af40a627090d3b257231453
URL:		https://github.com/sparklemotion/sqlite3-ruby
BuildRequires:	ruby-modules
BuildRequires:	sqlite3-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SQLite3 module for Ruby.

%description -l pl.UTF-8
Moduł SQLite3 dla Ruby.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

cd ext/%{pkgname}
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -fPIC"

rdoc --ri --op ri lib
rdoc --op rdoc lib
# rm -r ri/NOT_THIS_MODULE_RELATED_DIRS
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorarchdir}/sqlite3,%{ruby_vendorlibdir},%{ruby_ridir}} \
	$RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version} \
	$RPM_BUILD_ROOT%{ruby_specdir}

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ext/sqlite3/ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a ext/sqlite3/rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

install -p ext/sqlite3/sqlite3_native.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/sqlite3

cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README*
%dir %{ruby_vendorarchdir}/sqlite3
%attr(755,root,root) %{ruby_vendorarchdir}/sqlite3/sqlite3_native.so
%{ruby_vendorlibdir}/sqlite3
%{ruby_vendorlibdir}/sqlite3.rb
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/
