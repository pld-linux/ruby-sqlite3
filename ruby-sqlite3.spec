#
# Conditional build:
%bcond_without	doc			# don't build ri/rdoc

%define		pkgname	sqlite3
Summary:	SQLite3 module for Ruby
Summary(pl.UTF-8):	Moduł SQLite3 dla Ruby
Name:		ruby-sqlite3
Version:	1.4.2
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	cbea8e3b843acd9cf36402538cf1e9dd
URL:		https://github.com/sparklemotion/sqlite3-ruby
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel
BuildRequires:	ruby-hoe
BuildRequires:	ruby-minitest
BuildRequires:	ruby-modules
BuildRequires:	ruby-rake-compiler
BuildRequires:	sqlite3-devel
Obsoletes:	sqlite3-ruby
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
# noarch subpackages only when building with rpm5
BuildArch:	noarch

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby
# noarch subpackages only when building with rpm5
BuildArch:	noarch

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
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorarchdir}/sqlite3,%{ruby_vendorlibdir},%{ruby_specdir}} \
	$RPM_BUILD_ROOT

cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}
install -p ext/sqlite3/sqlite3_native.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/sqlite3

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a ext/sqlite3/ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a ext/sqlite3/rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
%endif

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

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}
%endif
