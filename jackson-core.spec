%_javapackages_macros
Name:          jackson-core
Version:       2.2.2
Release:       3.0%{?dist}
Summary:       Core part of Jackson
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonHome
Source0:       https://github.com/FasterXML/jackson-core/archive/%{name}-%{version}.tar.gz
# jackson-core package don't include the license file
# https://github.com/FasterXML/jackson-core/issues/88
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: java-devel
BuildRequires: mvn(com.fasterxml:oss-parent) >= 10

# test deps
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: maven-install-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-provider-junit4
BuildRequires: replacer

Provides:      jackson2-core = %{version}-%{release}
Obsoletes:     jackson2-core < %{version}-%{release}

BuildArch:     noarch

%description
Core part of Jackson that defines Streaming API as well
as basic shared abstractions.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%pom_xpath_remove "pom:build/pom:extensions/pom:extension[pom:artifactId='wagon-gitsite']"
# remove unavailable com.google.doclava doclava 1.0.3
%pom_xpath_remove "pom:reporting/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:configuration"
%pom_xpath_inject "pom:reporting/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']" '
<configuration>
  <encoding>${project.reporting.outputEncoding}</encoding>
  <quiet>true</quiet>
  <source>${javac.src.version}</source>
</configuration>'

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt

%build
%mvn_file : %{name}
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt README.md

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- review fixes

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- 2.2.2
- renamed jackson-core

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-core

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm