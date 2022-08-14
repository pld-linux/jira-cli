%define		vendor_ver	1.0.0

Summary:	Feature-rich Interactive Jira Command Line
Name:		jira-cli
Version:	1.1.0
Release:	1
License:	MIT
Group:		Applications/Console
#Source0Download: https://github.com/ankitpokhrel/jira-cli/releases
Source0:	https://github.com/ankitpokhrel/jira-cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8c7865c3e8f36e12009d38bc4cc1f14a
# cd jira-cli-%{version}
# go mod vendor
# cd ..
# tar cJf jira-cli-vendor-%{version}.tar.xz jira-cli-v%{version}/vendor
Source1:	%{name}-vendor-%{vendor_ver}.tar.xz
# Source1-md5:	2b6e99c6b78425cfcdd14014e2cf664f
URL:		https://github.com/ankitpokhrel/jira-cli
BuildRequires:	golang >= 1.17
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
JiraCLI is an interactive command line tool for Atlassian Jira that
will help you avoid Jira UI to some extent.

%package -n bash-completion-jira-cli
Summary:	bash-completion for jira-cli
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-jira-cli
This package provides bash-completion for jira-cli.

%package -n zsh-completion-jira-cli
Summary:	Zsh completion for jira-cli
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-jira-cli
Zsh completion for jira-cli.

%prep
%setup -q -a1

%{__mv} jira-cli-%{vendor_ver}/vendor .

%{__mkdir_p} .go-cache

%build
%__go build -v -mod=vendor -ldflags "-X github.com/ankitpokhrel/jira-cli/internal/version.Version=%{version}" -o bin/jira github.com/ankitpokhrel/jira-cli/cmd/jira

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man7,%{bash_compdir},%{zsh_compdir}}

cp -p bin/jira $RPM_BUILD_ROOT%{_bindir}

$RPM_BUILD_ROOT%{_bindir}/jira man --generate --output $RPM_BUILD_ROOT%{_mandir}/man7
$RPM_BUILD_ROOT%{_bindir}/jira completion bash > $RPM_BUILD_ROOT%{bash_compdir}/jira
$RPM_BUILD_ROOT%{_bindir}/jira completion zsh > $RPM_BUILD_ROOT%{zsh_compdir}/_jira

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/jira
%{_mandir}/man7/jira*.7*

%files -n bash-completion-jira-cli
%defattr(644,root,root,755)
%{bash_compdir}/jira

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_jira
