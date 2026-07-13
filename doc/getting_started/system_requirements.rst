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
     - x86_64/amd64 or arm64
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

A servo drive needs a new command at a fixed interval, for example one
every millisecond. Regular Linux is built to get as much work done as
possible, not to hit that interval exactly, so it may pause the servo
control loop for a few milliseconds to handle a network packet or a
background job. When that happens the next command arrives late and
misses its deadline. Even one missed deadline makes the motion jerk and
lose both accuracy and speed, and on a production line it can trip the
drives and stop the machine. A real-time OS, such as Linux with the
PREEMPT_RT patch, makes sure the motion code always runs on time even
when the computer is busy. That is why industrial motion systems run on
one.

Installing this real-time kernel is covered in :doc:`computer_setup`,
and configuring it for use (isolating CPU cores for the WMX real-time
threads and tuning latency) is covered in :doc:`install_wmx_runtime`.

WMX Motion Control Engine
--------------------------

The WMX motion control engine is a high-performance, high-accuracy, real-time motion control
platform developed by MOVENSYS. It provides deterministic servo control over
EtherCAT fieldbus and serves as the hardware abstraction layer for physical servo drives.

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