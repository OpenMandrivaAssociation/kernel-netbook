# -*- Mode: rpm-spec -*-
#
# (c) Mandriva
#

%define kernelversion	2
%define patchlevel	6
%define sublevel	31

# kernel Makefile extraversion is substituted by 
# kpatch/kgit/kstable wich are either 0 (empty), rc (kpatch), git (kgit) 
# or stable release (kstable)
%define kpatch		rc8
%define kstable		0

# kernel.org -gitX patch (only the number after "git")
%define kgit		0

# this is the releaseversion
%define mdvrelease 	2

# This is only to make life easier for people that creates derivated kernels
# a.k.a name it kernel-tmb :)
%define ktag		netbook
%define kname 		kernel-%{ktag}

%define rpmtag		%distsuffix
%if %kpatch
%if %kgit
%define rpmrel		%mkrel 0.%{kpatch}.%{kgit}.%{mdvrelease}
%else
%define rpmrel		%mkrel 0.%{kpatch}.%{mdvrelease}
%endif
%else
%define rpmrel		%mkrel %{mdvrelease}
%endif

# theese two never change, they are used to fool rpm/urpmi/smart
%define fakever		1
%define fakerel		%mkrel 1

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %kpatch
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver	  	%{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%else
%if %kstable
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%define tar_ver   	%{kernelversion}.%{patchlevel}.%{sublevel}
%else
%define kversion  	%{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver   	%{kversion}
%endif
%endif
%define kverrel   	%{kversion}-%{rpmrel}

# used for not making too long names for rpms or search paths
%if %kpatch
%if %kgit
%define buildrpmrel     0.%{kpatch}.%{kgit}.%{mdvrelease}%{rpmtag}
%else
%define buildrpmrel     0.%{kpatch}.%{mdvrelease}%{rpmtag}
%endif
%else
%define buildrpmrel     %{mdvrelease}%{rpmtag}
%endif

%define buildrel        %{kversion}-%{buildrpmrel}

# having different top level names for packages means that you have to remove them by hard :(
%define top_dir_name    %{kname}-%{_arch}

%define build_dir       ${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir         %{build_dir}/linux-%{tar_ver}

# disable useless debug rpms...
%define _enable_debug_packages  %{nil}
%define debug_package           %{nil}

# build defines
%define build_doc 0
%define build_source 1
%define build_devel 1

%define build_kernel 1

%define distro_branch %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1.$2"' /etc/mandriva-release)

# End of user definitions
%{?_without_kernel: %global build_kernel 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}

%{?_with_kernel: %global build_kernel 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}

%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make 
%endif
# there are places where parallel make don't work
%define smake make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/")

# src.rpm description
Summary: 	The Linux kernel (the core of the Linux operating system)
Name:           %{kname}
Version:        %{kversion}
Release:        %{rpmrel}
License: 	GPLv2
Group: 		System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64
ExclusiveOS: 	Linux
URL:		http://wiki.mandriva.com/en/Docs/Howto/Manbo_Kernels#kernel-netbook

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1:        ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign

# This is for disabling mrproper and other targets on -devel rpms
Source2:	disable-mrproper-in-devel-rpms.patch
# This disables removal of bounds.h and asm-offsets.h in -devel rpms
Source3:	kbuild-really-dont-remove-bounds-asm-offsets-headers.patch

Source4:  	README.kernel-sources
Source5:  	README.MandrivaLinux

# Kernel defconfigs
Source20: 	i386_defconfig
Source21: 	x86_64_defconfig


####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing

%if %kpatch
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kstable
Patch1:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif
# kernel.org -git
%if %kgit
Patch2:         ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2
Source11:       ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-git%{kgit}.bz2.sign
%endif

# patches to be added on stable updates

# Make boot faster
Patch107:	linux-2.6.29-retry-root-mount.patch
Patch108:	linux-2.6.29-dont-wait-for-mouse.patch
Patch109:	linux-2.6.29-enable-async-by-default.patch

Patch120:	gpu-drm-nouveau.patch

Patch130:	kernel-pid-export-find_task_by_vpid-symbol-for-fglrx.patch

Patch142:	platform-x86-dell-laptop-Fix-rfkill-state-setting.patch

Patch150:	fs-inotify-do-not-send-a-block-of-zeros-when-no-pathname-is-available.patch

#END
####################################################################

# Defines for the things that are needed for all the kernels
%define requires1 module-init-tools >= 3.0-%mkrel 7
%define requires2 mkinitrd >= 3.4.43-%mkrel 10
%define requires3 bootloader-utils >= 1.9
%define requires4 sysfsutils module-init-tools >= 0.9.15
%define requires5 kernel-firmware >= 2.6.27-0.rc2.2mdv

%define kprovides kernel = %{tar_ver}, alsa

BuildRoot: 	%{_tmppath}/%{name}-%{kversion}-build-%{_arch}
Autoreqprov: 	no
BuildRequires: 	gcc module-init-tools >= 0.9.15

%description
Source package to build the Linux kernel.

#
# kernel: Symmetric MultiProcessing kernel
#
%if %build_kernel
%package -n %{kname}-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
%ifarch %{ix86}
Summary:	Linux Kernel for netbook use with i586 & 4GB RAM
%else
Summary:	Linux Kernel for netbook use with %{_arch}
%endif
Group:		System/Kernel and hardware
Provides:	%kprovides
Provides:	should-restart = system
Requires:	%requires1
Requires:	%requires2
Requires:	%requires3
Requires:	%requires4
Requires: 	%requires5

%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-%{buildrel}
%ifarch %{ix86}
This kernel is compiled for netbook use, single or multiple i586 
processor(s)/core(s) and less than 4GB RAM, using HZ_1000, voluntary
preempt, CFS cpu scheduler and cfq i/o scheduler.
This kernel relies on in-kernel smp alternatives to switch between 
up & smp mode depending on detected hardware. To force the kernel
to boot in single processor mode, use the "nosmp" boot parameter.
%else
This kernel is compiled for netbook use, single or multiple %{_arch}
processor(s)/core(s), using HZ_1000, voluntary preempt, CFS cpu 
scheduler and cfq i/o scheduler.
This kernel relies on in-kernel smp alternatives to switch between 
up & smp mode depending on detected hardware. To force the kernel
to boot in single processor mode, use the "nosmp" boot parameter.
%endif

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate
%endif # build_kernel


#
# kernel-source: kernel sources
#
%if %build_source
%package -n %{kname}-source-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Provides:	%{kname}-source, kernel-source = %{kverrel}, kernel-devel = %{kverrel}
Provides:	%{kname}-source-%{kernelversion}.%{patchlevel}
Requires:	glibc-devel, ncurses-devel, make, gcc, perl
Summary:	The source code for the Linux kernel
Group:		Development/Kernel
Autoreqprov: 	no
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-%{buildrel}
The %{kname}-source package contains the source code files for the 
Linux kernel. These source files are only needed if you want to build 
your own custom kernel that is better tuned to your particular hardware.

If you only want the files needed to build 3rdparty (nVidia, Ati, dkms-*,...)
drivers against, install the *-devel-* rpm that is matching your kernel.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate
%endif #build_source


# 
# kernel-devel: stripped kernel sources 
#
%if %build_devel
%package -n %{kname}-devel-%{buildrel}
Version:	%{fakever}
Release:	%{fakerel}
Provides:	kernel-devel = %{kverrel}
Summary:	The %{kname} devel files for 3rdparty modules build
Group:		Development/Kernel
Autoreqprov:	no
Requires:	glibc-devel, ncurses-devel, make, gcc, perl
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-devel-%{buildrel}
This package contains the kernel-devel files that should be enough to build 
3rdparty drivers against for use with the %{kname}-%{buildrel}.

If you want to build your own kernel, you need to install the full 
%{kname}-source-%{buildrel} rpm.
%endif #build_devel


#
# kernel-doc: documentation for the Linux kernel
#
%if %build_doc
%package -n %{kname}-doc
Version:        %{kversion}
Release:        %{rpmrel}
Summary:	Various documentation bits found in the kernel source
Group:		Books/Computer books
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-doc
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

For instructions for update, see:
http://www.mandriva.com/en/security/kernelupdate
%endif #build_doc


#
# kernel-latest: virtual rpm
#
%if %build_kernel
%package -n %{kname}-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-%{buildrel}
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname} installed...
%endif #build_kernel


#
# kernel-source-latest: virtual rpm
#
%if %build_source
%package -n %{kname}-source-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-source
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-source-%{buildrel}
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-source installed...
%endif #build_source


#
# kernel-devel-latest: virtual rpm
#
%if %build_devel
%package -n %{kname}-devel-latest
Version:        %{kversion}
Release:        %{rpmrel}
Summary: 	Virtual rpm for latest %{kname}-devel
Group: 	  	System/Kernel and hardware
Requires: 	%{kname}-devel-%{buildrel}
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-devel installed...
%endif #build_devel


#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

cd %{src_dir}

%if %kpatch
%patch1 -p1
%endif
%if %kstable
%patch1 -p1
%endif
%if %kgit
%patch2 -p1
%endif

# extra patches

%patch107 -p1
%patch108 -p1
%patch109 -p1

# nouveau
%patch120 -p1

# fix fglrx build
%patch130 -p1

# rfkill fixes
%patch142 -p1

# fix inotify regression in -rc8 causing boot hang/failure
%patch150 -p1

# PATCH END

#
# Setup Begin
#


# Install defconfigs...
install %{SOURCE20} %{build_dir}/linux-%{tar_ver}/arch/x86/configs/
install %{SOURCE21} %{build_dir}/linux-%{tar_ver}/arch/x86/configs/

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile


%build
# Common target directories
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _kerneldir /usr/src/linux-%{kversion}-%{ktag}-%{buildrpmrel}
%define _develdir /usr/src/linux-%{kversion}-%{ktag}-devel-%{buildrpmrel}


# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_source %{temp_root}%{_kerneldir}
%define temp_devel %{temp_root}%{_develdir}


# Create a simulacro of buildroot
rm -rf %{temp_root}
install -d %{temp_root}


# make sure we are in the directory
cd %{src_dir}

# make sure EXTRAVERSION says what we want it to say
%if %kstable
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{kstable}-%{ktag}-%{buildrpmrel}/" Makefile
%else
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{ktag}-%{buildrpmrel}/" Makefile
%endif

# Prepare the kernel
%smake -s mrproper
%ifarch %{ix86} x86_64
	cp arch/x86/configs/%{target_arch}_defconfig .config
%else
	cp arch/%{target_arch}/defconfig .config
%endif
%smake oldconfig

# Build the kernel
%kmake all

# Install kernel
install -d %{temp_boot}
install -m 644 System.map \
               %{temp_boot}/System.map-%{kversion}-%{ktag}-%{buildrpmrel}
install -m 644 .config %{temp_boot}/config-%{kversion}-%{ktag}-%{buildrpmrel}
cp -f arch/%{target_arch}/boot/bzImage \
      %{temp_boot}/vmlinuz-%{kversion}-%{ktag}-%{buildrpmrel}

# Install modules
install -d %{temp_modules}/%{kversion}-%{ktag}-%{buildrpmrel}
%smake INSTALL_MOD_PATH=%{temp_root} \
       KERNELRELEASE=%{kversion}-%{ktag}-%{buildrpmrel} \
       modules_install

# remove /lib/firmware, we use a separate kernel-firmware
rm -rf %{temp_root}/lib/firmware

# Save devel tree
mkdir -p %{temp_devel}
for i in $(find . -name 'Makefile*'); do cp -R --parents $i %{temp_devel};done
for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i %{temp_devel};done
cp -fR include %{temp_devel}
cp -fR scripts %{temp_devel}
%ifarch %{ix86} x86_64
	cp -fR arch/x86/kernel/asm-offsets.{c,s} %{temp_devel}/arch/x86/kernel/
	cp -fR arch/x86/kernel/asm-offsets_{32,64}.c %{temp_devel}/arch/x86/kernel/
	cp -fR arch/x86/include %{temp_devel}/arch/x86/
%else
	cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} %{temp_devel}/arch/%{target_arch}/kernel/
	cp -fR arch/%{target_arch}/include %{temp_devel}/arch/%{target_arch}/
%endif

# Needed for generation of kernel/bounds.s
cp -fR kernel/bounds.c %{temp_devel}/kernel/

# Needed for lguest
cp -fR drivers/lguest/lg.h %{temp_devel}/drivers/lguest/

cp -fR .config Module.symvers %{temp_devel}

# Needed for truecrypt build (Danny)
cp -fR drivers/md/dm.h %{temp_devel}/drivers/md/

# Needed for external dvb tree (#41418)
cp -fR drivers/media/dvb/dvb-core/*.h %{temp_devel}/drivers/media/dvb/dvb-core/
cp -fR drivers/media/dvb/frontends/lgdt330x.h %{temp_devel}/drivers/media/dvb/frontends/

# add acpica header files, needed for fglrx build
cp -fR drivers/acpi/acpica/*.h %{temp_devel}/drivers/acpi/acpica/

# Disable bounds.h and asm-offsets.h removal
patch -p1 -d %{temp_devel} -i %{SOURCE3}

# Check and clean the -devel tree
pushd %{temp_devel} >/dev/null
    %smake -s prepare scripts clean
    rm -f .config.old
popd >/dev/null

# Disable mrproper and other targets
patch -p1 -d %{temp_devel} -i %{SOURCE2}

# Fix permissions
chmod -R a+rX %{temp_devel}

#make sure we are in the directory
cd %src_dir

# kernel-source is shipped as an unprepared tree
%smake -s mrproper


###
### Install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_devel %{buildroot}%{_develdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu \
	 microblaze mn10300 parisc powerpc ppc sh sh64 s390 sparc v850 xtensa; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i

%if %build_devel
	rm -rf %{target_devel}/arch/$i
	rm -rf %{target_devel}/include/asm-$i
%endif
done

# remove arch files based on target arch
%ifnarch %{ix86} x86_64
	rm -rf %{target_source}/arch/x86
	rm -rf %{target_source}/include/asm-x86
%if %build_devel
	rm -rf %{target_devel}/arch/x86
	rm -rf %{target_devel}/include/asm-x86
%endif
%endif

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.tmp_gas_check,.mailmap,.missing-syscalls.d,arch/.gitignore}

#endif %build_source
%endif


# gzipping modules
find %{target_modules} -name "*.ko" | xargs gzip -9


# We used to have a copy of PrepareKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

for i in %{target_modules}/*; do
  rm -f $i/build $i/source
done


# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here
pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

for i in *; do
	pushd $i
	echo "Creating module.description for $i"
	modules=`find . -name "*.ko.gz"`
	echo $modules | xargs /sbin/modinfo-25 \
	| perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
	popd
done
popd


###
### Clean
###

%clean
rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 


###
### Scripts
###

### kernel
%if %build_kernel
%preun -n %{kname}-%{buildrel}
/sbin/installkernel -R %{kversion}-%{ktag}-%{buildrpmrel}
if [ -L /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/build ]; then
    rm -f /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/source ]; then
    rm -f /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/source
fi
pushd /boot > /dev/null
if [ -L vmlinuz-%{ktag} ]; then
    if [ "$(readlink vmlinuz-%{ktag})" = "vmlinuz-%{kversion}-%{ktag}-%{buildrpmrel}" ]; then
	rm -f vmlinuz-%{ktag}
    fi
fi
if [ -L initrd-%{ktag}.img ]; then
    if [ "$(readlink initrd-%{ktag}.img)" = "initrd-%{kversion}-%{ktag}-%{buildrpmrel}.img" ]; then
	rm -f initrd-%{ktag}.img
    fi
fi
popd > /dev/null
exit 0

%post -n %{kname}-%{buildrel}
/sbin/installkernel -L %{kversion}-%{ktag}-%{buildrpmrel}
if [ -d /usr/src/linux-%{kversion}-%{ktag}-devel-%{buildrpmrel} ]; then
    ln -sf /usr/src/linux-%{kversion}-%{ktag}-devel-%{buildrpmrel} \
           /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/build
    ln -sf /usr/src/linux-%{kversion}-%{ktag}-devel-%{buildrpmrel} \
           /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/source
fi
pushd /boot > /dev/null
if [ -L vmlinuz-%{ktag} ]; then
    rm -f vmlinuz-%{ktag}
fi
ln -sf vmlinuz-%{kversion}-%{ktag}-%{buildrpmrel} vmlinuz-%{ktag}
if [ -L initrd-%{ktag}.img ]; then
    rm -f initrd-%{ktag}.img
fi
ln -sf initrd-%{kversion}-%{ktag}-%{buildrpmrel}.img initrd-%{ktag}.img
popd > /dev/null

%postun -n %{kname}-%{buildrel}
/sbin/kernel_remove_initrd %{buildrel}
%endif # build_kernel


### kernel-devel
%if %build_devel
%post -n %{kname}-devel-%{buildrel}
# place /build and /source symlinks in place.
if [ -d /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel} ]; then
    ln -sf /usr/src/linux-%{kversion}-%{ktag}-devel-%{buildrpmrel} \
           /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/build
    ln -sf /usr/src/linux-%{kversion}-%{ktag}-devel-%{buildrpmrel} \
           /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/source
fi

%preun -n %{kname}-devel-%{buildrel}
# we need to delete <modules>/{build,source} at uninstall
if [ -L /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/build ]; then
    rm -f /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/build
fi
if [ -L /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/source ]; then
    rm -f /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/source
fi
exit 0
%endif #build_devel


### kernel-source
%if %build_source
%post -n %{kname}-source-%{buildrel}
if [ -d "/lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}" ]; then
	if [ ! -L $i/build -a ! -L $i/source ]; then
		rm -f $i/{build,source}
	        ln -sf /usr/src/linux-%{kversion}-%{ktag}-%{buildrpmrel} \
	               $i/build
	        ln -sf /usr/src/linux-%{kversion}-%{ktag}-%{buildrpmrel} \
	               $i/source
	fi
fi

%preun -n %{kname}-source-%{buildrel}
for i in /lib/modules/%{kversion}-%{ktag}-%{buildrpmrel}/{build,source}; do
	if [ -L $i ]; then
		if [ "$(readlink $i)" = "/usr/src/linux-%{kversion}-%{ktag}-%{buildrpmrel}" ]; then
			rm -f $i
		fi
	fi
done
exit 0
%endif # build_source


###
### file lists
###

# kernel
%if %build_kernel
%files -n %{kname}-%{buildrel}
%defattr(-,root,root)
%{_bootdir}/config-%{kversion}-%{ktag}-%{buildrpmrel}
%{_bootdir}/vmlinuz-%{kversion}-%{ktag}-%{buildrpmrel}
%{_bootdir}/System.map-%{kversion}-%{ktag}-%{buildrpmrel}
%dir %{_modulesdir}/%{kversion}-%{ktag}-%{buildrpmrel}/
%{_modulesdir}/%{kversion}-%{ktag}-%{buildrpmrel}/kernel
%{_modulesdir}/%{kversion}-%{ktag}-%{buildrpmrel}/modules.*
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif # build_kernel

# kernel-source
%if %build_source
%files -n %{kname}-source-%{buildrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.gitignore
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/Kbuild
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/arch/Kconfig
%ifarch %{ix86} x86_64
%{_kerneldir}/arch/x86
%endif
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/firmware
%{_kerneldir}/fs
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%ifarch %{ix86} x86_64
%{_kerneldir}/include/asm-x86
%endif
%{_kerneldir}/include/crypto
%{_kerneldir}/include/drm
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/trace
%{_kerneldir}/include/video
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/keys
%{_kerneldir}/include/rdma
%{_kerneldir}/include/xen
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/samples
%{_kerneldir}/scripts
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/virt
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif # build_source

# kernel-devel
%if %build_devel
%files -n %{kname}-devel-%{buildrel}
%defattr(-,root,root)
%dir %{_develdir}
%dir %{_develdir}/arch
%dir %{_develdir}/include
%{_develdir}/.config
%{_develdir}/Documentation
%{_develdir}/Kbuild
%{_develdir}/Makefile
%{_develdir}/Module.symvers
%{_develdir}/arch/Kconfig
%ifarch %{ix86} x86_64
%{_develdir}/arch/x86
%endif
%{_develdir}/arch/um
%{_develdir}/block
%{_develdir}/crypto
%{_develdir}/drivers
%{_develdir}/firmware
%{_develdir}/fs
%{_develdir}/include/Kbuild
%{_develdir}/include/acpi
%{_develdir}/include/asm
%{_develdir}/include/asm-generic
%ifarch %{ix86} x86_64
%{_develdir}/include/asm-x86
%endif
%{_develdir}/include/config
%{_develdir}/include/crypto
%{_develdir}/include/drm
%{_develdir}/include/keys
%{_develdir}/include/linux
%{_develdir}/include/math-emu
%{_develdir}/include/mtd
%{_develdir}/include/net
%{_develdir}/include/pcmcia
%{_develdir}/include/rdma
%{_develdir}/include/scsi
%{_develdir}/include/sound
%{_develdir}/include/trace
%{_develdir}/include/video
%{_develdir}/include/media
%{_develdir}/include/rxrpc
%{_develdir}/include/xen
%{_develdir}/init
%{_develdir}/ipc
%{_develdir}/kernel
%{_develdir}/lib
%{_develdir}/mm
%{_develdir}/net
%{_develdir}/samples
%{_develdir}/scripts
%{_develdir}/security
%{_develdir}/sound
%{_develdir}/tools
%{_develdir}/usr
%doc README.kernel-sources
%doc README.MandrivaLinux
%endif # build_devel


%if %build_doc
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif # build_doc

%if %build_kernel
%files -n %{kname}-latest
%defattr(-,root,root)
%endif # build_kernel

%if %build_source
%files -n %{kname}-source-latest
%defattr(-,root,root)
%endif # build_source

%if %build_devel
%files -n %{kname}-devel-latest
%defattr(-,root,root)
%endif # build_devel
