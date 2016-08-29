%define name python-cb-cyphort-connector
%define version 2.2
%define unmangled_version 2.2
%define release 1
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Summary: Carbon Black Cyphort Bridge
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: Commercial
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Carbon Black <support@carbonblack.com>
Url: http://www.carbonblack.com/

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version}

%build
pyinstaller cb-cyphort-connector.spec

%install
python setup.py install_cb --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans
mkdir -p /usr/share/cb/integrations/cyphort/db
chkconfig --add cb-cyphort-connector
chkconfig --level 345 cb-cyphort-connector on

# not auto-starting because conf needs to be updated
#/etc/init.d/cb-cyphort-connector start


%preun
/etc/init.d/cb-cyphort-connector stop

# only delete the chkconfig entry when we uninstall for the last time,
# not on upgrades
if [ "X$1" = "X0" ]
then
    chkconfig --del cb-cyphort-connector
fi


%files -f INSTALLED_FILES
%defattr(-,root,root)
