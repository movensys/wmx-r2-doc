Install WMX Runtime
===================

With the real-time kernel in place (see :doc:`computer_setup`), install the WMX
runtime, isolate the CPU cores for the real-time threads, and point the runtime
at the EtherCAT NIC.

1. Install the WMX runtime
--------------------------

WMX3 is MOVENSYS's software-defined motion control stack. It connects the PC to
the servo drives over EtherCAT and provides the deterministic cycle loop. Select
the tab that matches your hardware.

.. tab-set::

   .. tab-item:: x86-based PC
      :sync: x86

      **Download the WMX3 installer** — pick the archive that matches your
      Ubuntu version:

      .. code-block:: bash

         # Ubuntu 22.04
         wget --user=guest --password=guest http://download.movensys.com:8111/webdav/WMX3_Installer/Linux/Ubuntu22.04_linux5.19.0_rt10.zip
         # Ubuntu 24.04
         wget --user=guest --password=guest http://download.movensys.com:8111/webdav/WMX3_Installer/Linux/Ubuntu24.04_linux6.15.2_rt2.zip

      **Install WMX3** — extract the archive and run the installer:

      .. code-block:: bash

         # Ubuntu 22.04
         unzip Ubuntu22.04_linux5.19.0_rt10.zip
         cd Ubuntu22.04_linux5.19.0_rt10
         sudo dpkg -i *wmx3-installer.deb

         # Ubuntu 24.04
         unzip Ubuntu24.04_linux6.15.2_rt2.zip
         cd Ubuntu24.04_linux6.15.2_rt2
         sudo dpkg -i *wmx3-installer.deb

   .. tab-item:: ARM-based PC
      :sync: arm

      **Download the WMX3 installer:**

      .. code-block:: bash

         wget --user=guest --password=guest http://download.movensys.com:8111/webdav/WMX3_Installer/Linux/wmx3_arm64_installers.zip
         unzip wmx3_arm64_installers.zip

      **Install the package for your board:**

      .. code-block:: bash

         # NVIDIA Jetson Orin NX Developer Kit (Advantech MIC-713), Ubuntu 20.04
         sudo dpkg -i 20260403_Ubuntu20.04_linux-5.10.120-rt70-jetson-orin-nx-mic-713-wmx3-installer.deb

         # NVIDIA Jetson Orin AGX Developer Kit (Advantech MIC-733ao), Ubuntu 22.04
         sudo dpkg -i 20260403_Ubuntu22.04_linux-5.15.148-rt-jetson-agx-orin-mic-733ao-wmx3-installer.deb

         # NVIDIA Jetson Thor Developer Kit (Advantech MIC-743), Ubuntu 24.04
         sudo dpkg -i 20260403_Ubuntu24.04_linux-6.8.12-rt-jetson-thor-mic-743-wmx3-installer.deb

The installer places the WMX3 runtime at ``/opt/wmx3/``. Confirm the required
headers and libraries are present:

.. code-block:: bash

   ls /opt/wmx3/include/WMX3Api.h
   ls /opt/wmx3/lib/libwmx3api.so
   ls /opt/wmx3/lib/libimdll.so

All files must exist before proceeding. If any are missing, re-run the installer
or contact your MOVENSYS representative.

.. _computer-setup-isolate:

2. Isolate cores for WMX
------------------------

Determinism comes from dedicating CPU cores to the WMX real-time threads and
keeping housekeeping work off them. Add the isolation parameters to
``/etc/default/grub`` for your platform:

.. tab-set::

   .. tab-item:: General x86/amd64 & Jetson

      Set ``GRUB_CMDLINE_LINUX`` (example: reserve core ``3`` for the control
      loop and leave cores ``0,1,2`` for housekeeping):

      .. code-block:: text

         GRUB_CMDLINE_LINUX="quiet splash isolcpus=3 nohz_full=3 rcu_nocbs=3 irqaffinity=0,1,2 acpi_irq_nobalance noirqbalance"

   .. tab-item:: Intel XPU (Panther Lake)

      Set ``GRUB_CMDLINE_LINUX_DEFAULT``:

      .. code-block:: text

         GRUB_CMDLINE_LINUX_DEFAULT="isolcpus=managed_irq,domain,<rt_cpus> nohz_full=<rt_cpus> rcu_nocbs=<rt_cpus> irqaffinity=<housekeeping_cpus> intel_pstate=disable processor.max_cstate=1 idle=poll"

      - Replace ``<rt_cpus>`` with the cores reserved for the control loop (for
        example ``2,3``) and ``<housekeeping_cpus>`` with the remaining cores.
      - ``idle=poll`` trades power for latency; measure with ``cyclictest`` to
        confirm it helps on your hardware.
      - On hybrid Intel silicon (Panther Lake mixes P-cores, E-cores, and
        LP-E-cores), pin the control loop to isolated **P-cores** for the most
        consistent latency.

Then apply the change and reboot:

.. code-block:: bash

   sudo update-grub
   sudo reboot

Pin the WMX control loop to the isolated cores; pin AI workloads such as VLM,
Whisper, or OpenVINO to the remaining cores. A cgroup v2 slice (``cpuset`` +
``cpu.weight``) keeps the AI stack off the control cores while keeping GPU/NPU
access simple.

3. Configure the EtherCAT NIC
-----------------------------

WMX3's EtherCAT platform (``ec_platform.so``) sends and receives frames through
a NIC-driver DLL. Pick the driver that matches your transport:

.. list-table::
   :header-rows: 1
   :widths: 22 42 36

   * - Driver
     - Transport
     - Runtime prerequisites
   * - ``ndd_sock_raw.so``
     - Linux ``AF_PACKET`` / ``SOCK_RAW`` socket
     - ``CAP_NET_RAW`` (typically root)
   * - ``ndd_dpdk.so``
     - DPDK poll-mode driver (kernel bypass)
     - Hugepages, NIC bound to ``vfio-pci``/``uio``
   * - ``ndd_vnw.so``
     - Virtual network (no hardware)
     - None

Configure the driver in the section for the real-time network device
(``[rtnd0]`` for the first device) of
``/opt/wmx3/platform/ethercat/PrtTcpip.ini``. The ``UseNicDrvDll`` key selects
the driver; each driver reads its own keys from the same section.

.. tab-set::

   .. tab-item:: sock_raw

      Bind the driver to a kernel network interface. ``ifname`` is required (the
      ``NIC_DRV_DLL_IFNAME`` environment variable overrides it):

      .. code-block:: ini

         [rtnd0]
         UseNicDrvDll=ndd_sock_raw.so
         ifname=enp3s0            ; kernel interface to bind (required)
         rxprio=97               ; RX thread SCHED_FIFO priority (<=0 = default sched)

      Opening the raw socket needs ``CAP_NET_RAW``, so run the nodes as root.

   .. tab-item:: dpdk

      DPDK bypasses the kernel network stack, so reserve hugepages and bind the
      NIC to a userspace driver **before** starting the WMX3 engine.

      Reserve hugepages (2 GB as 1024 pages of 2 MB):

      .. code-block:: bash

         echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
         grep -i hugepages_ /proc/meminfo         # expect HugePages_Total: 1024

      Bind the EtherCAT NIC to ``vfio-pci`` (find the PCI address with
      ``dpdk-devbind.py --status``; pick a port that is not your management
      link, because the bound interface disappears from the kernel):

      .. code-block:: bash

         sudo modprobe vfio-pci
         sudo dpdk-devbind.py --bind=vfio-pci 0000:03:00.0

      Select the port in ``PrtTcpip.ini``. ``ifname`` is ignored; the port is
      chosen by id, pinned deterministically with an EAL allowlist:

      .. code-block:: ini

         [rtnd0]
         UseNicDrvDll=ndd_dpdk.so
         dpdk_port=0
         eal=-a 0000:03:00.0     ; allowlist the exact device, becomes port 0
         rxprio=97               ; RX thread SCHED_FIFO priority
         rxcore=3                ; pin RX poll loop to an ISOLATED core

      Binding does not survive a reboot, so re-run ``modprobe`` and the bind
      after each boot or automate them.

   .. tab-item:: vnw

      The virtual-network driver needs no hardware and takes no transport keys.
      The engine reads its virtual slave list from the same section:

      .. code-block:: ini

         [rtnd0]
         UseNicDrvDll=ndd_vnw.so
         numofslaves=6           ; number of virtual slaves (0 = empty network)

4. Test the WMX runtime
-----------------------

Connect the EtherCAT slave hardware (a single servo drive is recommended for a
first bring-up) to the configured NIC, power it on, then run the WMX3 command
line tools to bring the engine up, scan the bus, and enable the servo:

.. code-block:: bash

   cd /opt/wmx3/bin/
   sudo ./wmx3-start-engine     # start the WMX3 engine
   sudo ./wmx3-start-comm       # start cyclic EtherCAT communication
   sudo ./wmx3-ec-scan          # scan the bus for slaves
   sudo ./wmx3-ec-state         # show the EtherCAT master/slave state
   sudo ./wmx3-clear-alarm      # clear any drive alarms
   sudo ./wmx3-servo-on         # enable the servos
   sudo ./wmx3-axis-state 0     # show the state of axis 0
   sudo ./wmx3-stop-engine      # stop the engine when done
