System Requirements
===================

Hardware Requirements
---------------------

**Compute Platform:**

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Component
     - Minimum
     - Recommended
   * - CPU
     - x86_64 or ARM64 (arm64)
     - Intel Core i7 or NVIDIA Jetson Orin/Thor
   * - RAM
     - 4 GB
     - 8 GB or more
   * - Storage
     - 10 GB free
     - 20 GB free (including ROS2 + MoveIt2)
   * - GPU
     - Not required for base operation
     - NVIDIA GPU with CUDA for Isaac cuMotion
   * - NPU
     - Not required for base operation
     - Intel NPU for OpenVINO inference applications

Real-Time OS requirements
-------------------------

Servo drivers expect a command every fixed cycle. Standard Linux
optimizes for throughput rather than keeping a strict deterministic
schedule, so it may pause the program for a few milliseconds to handle
a packet or a background task. That delay makes the next command arrive
late and miss its cycle. A missed cycle makes motion stutter and drops
accuracy, and on a production line it can even fault the drivers and
stop the machine. A Real-Time OS such as Linux with the PREEMPT_RT
patch guarantees motion threads run on time even under load, which is
why every industrial motion stack runs on one.

WMX Motion Control Engine
--------------------------

The WMX motion control engine is a high-performance, high-accuracy, real-time motion control
platform developed by MOVENSYS. It provides deterministic servo control over
EtherCAT fieldbus and serves as the hardware abstraction layer between ROS2
and physical servo drives.

**Key features:**

- **Real-time EtherCAT master** -- manages cyclic communication with servo
  drives at deterministic update rates
- **Multi-axis coordination** -- supports synchronized motion across 6+ servo
  axes with cubic spline interpolation (``CSplinePos``)
- **Shared-memory architecture** -- multiple ROS2 nodes connect to the same
  WMX engine instance through independent device handles, bridging the
  non-real-time ROS2 domain with the real-time WMX engine
- **Hardware abstraction** -- provides a unified C++ API (``CoreMotion``,
  ``AdvancedMotion``, ``Io``, ``Ecat``, ``WMX3Api``) so ROS2 nodes remain
  robot-agnostic; only configuration files differ between robots

The WMX runtime must be installed at ``/opt/wmx3/`` before building or
running the WMX ROS2 packages. See :doc:`computer_setup` for installation and
verification steps.

.. note::

   Root (sudo) access is required at runtime. The WMX motion control engine
   and EtherCAT communication require kernel-level access to the network
   interface.

The C++ standard required is **C++17** (set in ``CMakeLists.txt``).