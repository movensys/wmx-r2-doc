Computer Setup
==============

WMX ROS2 needs a real-time Linux kernel, ROS 2, and Docker on the
target computer before you install the WMX-ROS2 packages. 

Supported targets
-----------------

.. list-table::
   :header-rows: 1
   :widths: 32 14 20 34

   * - Target
     - Arch
     - Ubuntu
     - Kernel source
   * - General x86/amd64
     - x86_64
     - 22.04 / 24.04
     - kernel.org vanilla + RT patch
   * - Intel XPU (Panther Lake)
     - x86_64
     - 24.04
     - Intel ``mainline-tracking`` (v6.17)
   * - Jetson Orin NX
     - arm64
     - JetPack (L4T)
     - NVIDIA L4T real-time kernel
   * - Jetson Orin AGX
     - arm64
     - JetPack (L4T)
     - NVIDIA L4T real-time kernel
   * - Jetson Thor
     - arm64
     - JetPack (L4T)
     - NVIDIA L4T real-time kernel

1. Install the base OS
----------------------

Pick your target and install the operating system.

.. tab-set::

   .. tab-item:: General x86/amd64

      Install Ubuntu 22.04 or 24.04 the usual way with the standard Ubuntu
      installer, then update fully.

      - Ubuntu 22.04 LTS — `download <https://releases.ubuntu.com/jammy/>`__
      - Ubuntu 24.04 LTS — `download <https://releases.ubuntu.com/noble/>`__
      - Install guide — `Install Ubuntu desktop
        <https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview>`__

      .. code-block:: bash

         sudo apt update && sudo apt full-upgrade -y

      In firmware/BIOS, disable **Secure Boot** for now. Signing a custom
      kernel is extra work you can add later.

   .. tab-item:: Intel XPU (Panther Lake)

      Install Ubuntu 24.04 the usual way with the standard Ubuntu installer,
      then update fully.

      - Ubuntu 24.04 LTS — `download <https://releases.ubuntu.com/noble/>`__
      - Install guide — `Install Ubuntu desktop
        <https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview>`__

      .. code-block:: bash

         sudo apt update && sudo apt full-upgrade -y

      In firmware/BIOS, disable **Secure Boot** for now. Also review
      **C-states**, **SpeedStep**, and **Turbo**, plus any "low-power E-core"
      options; you will likely pin these down later for latency (see
      :ref:`core isolation <computer-setup-isolate>`).

   .. tab-item:: Jetson Developer Kit

      The Jetson developer kit's built-in eMMC storage is small — too small
      for JetPack plus ROS 2, MoveIt2, Docker images, and perception models.
      To add this storage capacity, install an NVMe SSD card in the Jetson
      developer kit's carrier board (in the M.2 Key M slot) before flashing,
      then flash the OS onto the SSD.

      Flash the board's Board Support Package (BSP) with **NVIDIA SDK
      Manager**, which installs JetPack (the L4T Linux distribution) for your
      Jetson model — Jetson Orin NX, Jetson Orin AGX, or Jetson Thor. In SDK
      Manager, select the NVMe SSD as the storage device so JetPack is
      installed on the SSD rather than the eMMC.

      - `Install Jetson with SDK Manager
        <https://docs.nvidia.com/sdk-manager/install-with-sdkm-jetson/index.html>`__

      After flashing, record the L4T release — you need it to match the
      correct real-time kernel in the next step:

      .. code-block:: bash

         cat /etc/nv_tegra_release   # e.g. R38 (release), REVISION: 4.x  ->  L4T r38.4

2. Install the real-time kernel
-------------------------------

Install a PREEMPT_RT kernel for your target.

.. tab-set::

   .. tab-item:: General x86/amd64

      Build a PREEMPT_RT kernel from the kernel.org vanilla source plus the
      official RT patch, then install the resulting ``.deb`` packages. 

      **Install build dependencies:**

      .. code-block:: bash

         sudo apt update
         sudo apt install -y build-essential libncurses-dev bison flex libssl-dev \
              libelf-dev bc zstd kmod cpio rsync git wget gnupg2 rt-tests stress-ng

      **Fetch the kernel and RT patch (with signatures):**

      Not every kernel release ships a matching RT patch. Pick a ``KVER`` that
      has one and set ``RTVER`` to its revision. Browse the
      `RT patch index <https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/>`__,
      or list the revisions available for a version from the terminal:

      .. code-block:: bash

         uname -r   # your PC's current kernel version, e.g. 6.15.2-generic
         # RT patch revisions available for a kernel version (here 6.15)
         wget -qO- https://mirrors.edge.kernel.org/pub/linux/kernel/projects/rt/6.15/ | grep -oE 'patch-[0-9.]+-rt[0-9]+'

      Set the version you chose, then download it:

      .. code-block:: bash

         export KVER=6.15 RTVER=rt2
         mkdir -p ~/rt-build && cd ~/rt-build
         wget -N https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KVER}.tar.xz \
                 https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-${KVER}.tar.sign
         wget -N https://cdn.kernel.org/pub/linux/kernel/projects/rt/${KVER}/patch-${KVER}-${RTVER}.patch.xz \
                 https://cdn.kernel.org/pub/linux/kernel/projects/rt/${KVER}/patch-${KVER}-${RTVER}.sign

      **Verify the GPG signatures:**

      .. code-block:: bash

         gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org
         gpg2 --locate-keys bigeasy@linutronix.de
         xz -dk linux-${KVER}.tar.xz patch-${KVER}-${RTVER}.patch.xz
         gpg2 --verify linux-${KVER}.tar.sign linux-${KVER}.tar
         gpg2 --verify patch-${KVER}-${RTVER}.sign patch-${KVER}-${RTVER}.patch

      A "not certified" warning is normal.

      **Apply the patch and configure PREEMPT_RT:**

      .. code-block:: bash

         tar xf linux-${KVER}.tar && cd linux-${KVER}
         patch -p1 < ../patch-${KVER}-${RTVER}.patch
         cp /boot/config-$(uname -r) .config
         make olddefconfig
         scripts/config --disable PREEMPT_VOLUNTARY --disable PREEMPT \
                        --disable PREEMPT_DYNAMIC --enable PREEMPT_RT
         # avoid distro signing-cert traps for a personal build
         scripts/config --set-str SYSTEM_TRUSTED_KEYS "" \
                        --set-str SYSTEM_REVOCATION_KEYS ""
         scripts/config --disable MODULE_SIG
         make olddefconfig
         grep '^CONFIG_PREEMPT_RT=y' .config   # expect a match

      **Build and install the ``.deb`` packages, then reboot:**

      .. code-block:: bash

         make -j"$(nproc)" bindeb-pkg
         sudo dpkg -i ../linux-image-*${RTVER}*.deb ../linux-headers-*${RTVER}*.deb
         sudo update-grub
         sudo reboot

   .. tab-item:: Intel XPU (Panther Lake)

      Build the RT kernel from Intel's
      `mainline-tracking <https://github.com/intel/mainline-tracking>`_ tree,
      which carries the platform enablement for current Intel silicon.

      **Install build dependencies:**

      .. code-block:: bash

         sudo apt update
         sudo apt install -y build-essential libncurses-dev bison flex libssl-dev \
              libelf-dev bc dwarves zstd git fakeroot

      **Clone the tree and check out the target branch:**

      .. code-block:: bash

         git clone https://github.com/intel/mainline-tracking.git
         cd mainline-tracking
         git checkout linux/v6.17   # or the latest v6.17 tag on that branch

      .. note::

         Panther Lake Linux support is in active flux. Pin the exact
         commit/tag you build so you can reproduce it, and expect to rebuild
         as fixes land.

      **Start from your running config plus Intel defaults, then enable RT:**

      .. code-block:: bash

         cp /boot/config-$(uname -r) .config
         make olddefconfig
         ./scripts/config --enable PREEMPT_RT
         ./scripts/config --disable PREEMPT_VOLUNTARY --disable PREEMPT --disable PREEMPT_NONE
         make olddefconfig                       # resolves the RT dependency chain
         grep PREEMPT_RT .config                 # expect CONFIG_PREEMPT_RT=y

      **Clear the distro signing keys for a personal build:**

      .. code-block:: bash

         ./scripts/config --set-str SYSTEM_TRUSTED_KEYS ""
         ./scripts/config --set-str SYSTEM_REVOCATION_KEYS ""
         make olddefconfig
         grep -E 'SYSTEM_TRUSTED_KEYS|SYSTEM_REVOCATION_KEYS' .config

      **Build the ``.deb`` packages:**

      .. code-block:: bash

         sudo apt update
         sudo apt install -y debhelper libdw-dev gawk
         make -j"$(nproc)" bindeb-pkg LOCALVERSION=-preempt-rt DPKG_FLAGS=-d
         ls -1 ~/linux-image-*preempt-rt*.deb ~/linux-headers-*preempt-rt*.deb

      **Install (clean install/rollback) and reboot:**

      .. code-block:: bash

         sudo dpkg -i ../linux-image-*preempt-rt*.deb ../linux-headers-*preempt-rt*.deb
         sudo update-grub
         sudo reboot

      **Install the AI/accelerator stack** — once the RT kernel has booted,
      install the GPU/NPU drivers and inference runtimes for the platform:

      .. code-block:: bash

         sudo bash -c "$(wget -qLO - https://raw.githubusercontent.com/open-edge-platform/edge-developer-kit-reference-scripts/refs/heads/main/main_installer.sh)"

      .. note::

         The installer targets the stock HWE kernel; on a custom RT kernel the
         DKMS driver builds should work against your installed headers, but be
         ready to install the GPU/NPU drivers manually if the script balks.

   .. tab-item:: Jetson Developer Kit

      The Jetson boards ship without a real-time kernel. Enable PREEMPT_RT by
      following NVIDIA's real-time kernel guide **for the L4T version you
      recorded** when flashing the BSP (for example, L4T r38.4):

      - `Jetson Real-Time Kernel
        <https://docs.nvidia.com/jetson/archives/r38.4/DeveloperGuide/SD/Kernel/RealTimeKernel.html>`__

      After installing and rebooting into the RT kernel, lock the board to
      maximum performance:

      .. code-block:: bash

         sudo /usr/bin/jetson_clocks
         sudo /usr/sbin/nvpmodel -m 0

      Then continue to the verification step below.

.. _computer-setup-verify:

3. Verify the real-time install
-------------------------------

Confirm the RT kernel is running, then run ``cyclictest`` to measure worst-case
latency. ``rt-tests`` was installed with the build dependencies above; on
targets where it is not present, install it with:

.. code-block:: bash

   sudo apt install -y rt-tests

.. code-block:: bash

   uname -r                  # RT kernel version (e.g. 6.15.0-rt2, or the Jetson L4T RT build)
   uname -v | grep PREEMPT_RT
   cat /sys/kernel/realtime  # 1
   lsb_release -a            # Ubuntu 22.04 or 24.04

   # baseline, then again under load (run the stressor in another terminal):
   #   stress-ng --cpu $(nproc) --io 4 --vm 2 --vm-bytes 1G --timeout 5m
   sudo cyclictest -m -S -p 90 -i 200 -d 0 -D 5m

Watch the **Max** latency. On a tuned PREEMPT_RT x86 box you typically want the
worst case in the low tens of microseconds; high spikes point to firmware/SMI
or power-management issues to chase (BIOS C-states, SpeedStep, Turbo).

.. tip::

   For a longer soak test, keep the stressor running across all cores in one
   terminal and ``cyclictest`` in another for several hours, watching the max
   latency stay bounded.

4. Set the hostname
-------------------

.. code-block:: bash

   sudo hostnamectl set-hostname <new-host-name>
   sudo reboot

5. Install ROS 2
----------------

Install ROS 2 on the target, matching the Ubuntu version — **Jazzy** on Ubuntu
24.04, **Humble** on Ubuntu 22.04. Follow the official installation guide, then
add the CycloneDDS RMW that WMX ROS2 uses.

.. tab-set::

   .. tab-item:: Jazzy (Ubuntu 24.04)

      Follow the `ROS 2 Jazzy installation guide
      <https://docs.ros.org/en/jazzy/Installation.html>`_, then install the
      CycloneDDS RMW:

      .. code-block:: bash

         sudo apt install -y ros-jazzy-rmw-cyclonedds-cpp
         echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc

   .. tab-item:: Humble (Ubuntu 22.04)

      Follow the `ROS 2 Humble installation guide
      <https://docs.ros.org/en/humble/Installation.html>`_, then install the
      CycloneDDS RMW:

      .. code-block:: bash

         sudo apt install -y ros-humble-rmw-cyclonedds-cpp
         echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc

6. Install Docker
-----------------

Docker is used to run the containerized WMX ROS2 and perception workloads.

**Set up the Docker apt repository:**

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y ca-certificates curl gnupg
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
     https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update

**Install the Docker packages:**

.. code-block:: bash

   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   sudo systemctl restart docker

**Run Docker without sudo:**

.. code-block:: bash

   sudo usermod -aG docker $USER
   newgrp docker
