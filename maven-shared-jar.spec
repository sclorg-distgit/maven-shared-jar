%global pkg_name maven-shared-jar
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.1
Release:        7.8%{?dist}
# Maven-shared defines maven-shared-jar version as 1.1
Epoch:          1
Summary:        Maven JAR Utilities
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-shared-jar
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.apache.bcel:bcel)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-model)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-collections:commons-collections)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-digest)


%description
Utilities that help identify the contents of a JAR, including Java class
analysis and Maven metadata analysis.

This is a replacement package for maven-shared-jar

%package javadoc
Summary:        Javadoc for %{pkg_name}
    
%description javadoc
API documentation for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x

%pom_add_dep org.codehaus.plexus:plexus-container-default

find -type f -iname '*.jar' -delete

# Replace plexus-maven-plugin with plexus-component-metadata
find -name 'pom.xml' -exec sed \
    -i 's/<artifactId>plexus-maven-plugin<\/artifactId>/<artifactId>plexus-component-metadata<\/artifactId>/' '{}' ';'
find -name 'pom.xml' -exec sed \
    -i 's/<goal>descriptor<\/goal>/<goal>generate-metadata<\/goal>/' '{}' ';'

%mvn_file : %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# Tests require the jars that were removed
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.8
- Fix BR on maven-shared POM

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1:1.1-7.8
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1:1.1-7.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.4
- Mass rebuild 2014-02-18
- Add missing BR: maven-shared

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-7.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.1-7
- Mass rebuild 2013-12-27

* Thu Sep 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-6
- Fix BuildRequires

* Fri Aug 23 2013 Michal Srb <msrb@redhat.com> - 1:1.1-5
- Migrate away from mvn-rpmbuild (Resolves: #997500)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.1-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:1.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan 23 2013 Tomas Radej <tradej@redhat.com> - 1:1.1-2
- Removed jars and skipped tests

* Tue Jan 15 2013 Tomas Radej <tradej@redhat.com> - 1:1.1-1
- Initial version

