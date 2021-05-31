%define module_name	qca9377
%define module_version	4.5.24.4
%define module_release	alt2

%define flavour pico-imx8mq
%define karch aarch64
BuildRequires(pre): kernel-headers-modules-pico-imx8mq
%setup_kernel_module %flavour

%define module_dir /lib/modules/%kversion-%flavour-%krelease/%module_name

Summary: Qualcomm QCA9377 WLAN Driver (kernel module)
Name: kernel-modules-%module_name-%flavour
Version: %module_version
Release: %module_release.%kcode.%kbuildrelease
License: GPL
Group: System/Kernel and hardware

Packager: Kernel Maintainer Team <kernel@packages.altlinux.org>

ExclusiveOS: Linux
URL: https://github.com/TechNexion/qcacld-2.0
BuildRequires(pre): rpm-build-kernel
BuildRequires: kernel-headers-modules-%flavour = %kepoch%kversion-%krelease
BuildRequires: kernel-source-%module_name = %module_version

Provides:  kernel-modules-%module_name-%kversion-%flavour-%krelease = %version-%release
Conflicts: kernel-modules-%module_name-%kversion-%flavour-%krelease < %version-%release
Conflicts: kernel-modules-%module_name-%kversion-%flavour-%krelease > %version-%release

Requires(pre,postun): kernel-image-%flavour = %kepoch%kversion-%krelease
ExclusiveArch: %karch

%description
Qualcomm QCA9377 WLAN Driver

%prep
rm -rf kernel-source-%module_name-%module_version
tar -jxf %kernel_src/kernel-source-%module_name-%module_version.tar.bz2
%setup -D -T -n kernel-source-%module_name-%module_version

%build
. %_usrsrc/linux-%kversion-%flavour/gcc_version.inc
export CFLAGS+="%optflags"
%make_build -C %_usrsrc/linux-%kversion-%flavour M=`pwd` \
     WLAN_ROOT=`pwd` MODNAME=wlan CONFIG_QCA_WIFI_ISOC=0 \
     CONFIG_QCA_WIFI_2_0=1 CONFIG_QCA_CLD_WLAN=m WLAN_OPEN_SOURCE=1 \
     CONFIG_CLD_HL_SDIO_CORE=y CONFIG_PER_VDEV_TX_DESC_POOL=1 SAP_AUTH_OFFLOAD=1 \
     CONFIG_QCA_LL_TX_FLOW_CT=1 CONFIG_WLAN_FEATURE_FILS=y \
     CONFIG_FEATURE_COEX_PTA_CONFIG_ENABLE=y \
     CONFIG_QCA_SUPPORT_TXRX_DRIVER_TCP_DEL_ACK=y \
     CONFIG_WLAN_WAPI_MODE_11AC_DISABLE=y TARGET_BUILD_VARIANT=user \
     CONFIG_NON_QC_PLATFORM=y CONFIG_HDD_WLAN_WAIT_TIME=10000 \
     modules

%install
install -d %buildroot%module_dir
install -p -m644 wlan.ko %buildroot%module_dir

%files
%defattr(644,root,root,755)
%module_dir

%changelog
* %(LC_TIME=C date "+%%a %%b %%d %%Y") %{?package_signer:%package_signer}%{!?package_signer:%packager} %version-%release
- Build for kernel-image-%flavour-%kversion-%krelease.

* Mon May 31 2021 Pavel Nakonechnyi <zorg@altlinux.org> 4.5.24.4-alt2
- hardcode kflavour and karch

* Sun Jul 07 2019 Pavel Nakonechnyi <zorg@altlinux.org> 4.5.24.4-alt1
- initial build
