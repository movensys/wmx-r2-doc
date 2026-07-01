WMX ROS2 Documentation
=======================

WMX ROS2 brings industrial deterministic real-time motion control into the
ROS2 ecosystem. It provides ROS2 packages that drive robot platforms
through the WMX motion control engine over EtherCAT. It turns planner
output such as MoveIt2 and Nav2 trajectories into the precisely timed servo motion
that industrial applications demand such as semiconductor equipment,
manufacturing automation, and precision robotics.

The entire stack runs on a single industrial PC (IPC) or edge device with no separate motion
controller, combining perception and deterministic motion into edge
physical AI so a machine can sense and act in the real world on one
device.

WMX ROS2 integrates with widely used projects in the ROS2 ecosystem:

* `MoveIt2 <https://moveit.ai/>`_ for manipulator motion planning
* `Nav2 <https://nav2.org/>`_ for mobile robot navigation
* `ros2_control <https://control.ros.org/>`_ for hardware interface and controller management
* `NVIDIA Isaac Sim <https://developer.nvidia.com/isaac/sim>`_ and
  `Gazebo <https://gazebosim.org/>`_ for simulation
* `NVIDIA Isaac ROS <https://developer.nvidia.com/isaac/ros>`_ for GPU
  accelerated perception
* `YOLO <https://docs.ultralytics.com/>`_ for real time object detection
* `Intel OpenVINO <https://docs.openvino.ai/2026/index.html>`_ for optimized inference on
  CPU and integrated accelerators
* Multimodal large language models (LLMs) and vision language models
  (VLMs) for natural language task specification and high level reasoning



.. figure:: /_static/images/wmx-ros2_overview.drawio.png
   :alt: WMX ROS2 architecture overview
   :align: center
   :width: 100%

   WMX ROS2 architecture overview.

Why WMX ROS2?
----------------------------------------

A real-time OS provides the kernel-level timing guarantees, but ROS2
still leaves one step uncovered. A planner such as MoveIt2 or Nav2 produces a
trajectory and `ros2_control <https://control.ros.org/>`_ sends joint
commands to the hardware. Those commands still need to become the
precisely timed signals servo drivers execute on a fixed cycle. Most
ROS2 setups bridge this execution gap with a closed industrial
controller over TCP/IP, which adds latency the planner can never
recover. The other common option sends raw EtherCAT commands and leaves
smoothing and coordination to ROS2, which is not built for hard
real-time work. Both approaches become the limiting factor once a line
needs production-grade cycle accuracy. The WMX ROS2 package closes the
gap by bringing the WMX motion control engine into ROS2, so the
planner's output runs as smooth and deterministic motion without
leaving the ROS2 ecosystem.

What is WMX ROS2?
----------------------------------------

WMX ROS2 is an open source MIT-licensed ROS2 package layer that owns the
timing-sensitive step: smoothing trajectories, coordinating joints, and
emitting commands at the rate servo drivers expect. It runs in
simulation, in hardware-in-the-loop, and on real EtherCAT hardware across
x86 industrial PCs and NVIDIA Jetson boards on a real-time Linux kernel
(PREEMPT_RT). It also brings AI to the edge as physical AI, hosting
workloads such as `NVIDIA Isaac ROS <https://developer.nvidia.com/isaac/ros>`_,
`YOLO <https://docs.ultralytics.com/>`_,
`Intel OpenVINO <https://docs.openvino.ai/2026/index.html>`_, and
vision-language models on the same device that drives the servo. It is
built on the WMX motion control engine, which keeps motion on a
deterministic cycle and exposes more than 200 APIs for trajectory
conversion, EtherCAT, I/O, and engine control. Proven over a decade in
semiconductor, manufacturing, and precision robotics. WMX runs free in
renewable 1-hour sessions that you extend by restarting the engine, and a
commercial license removes the limit for production.

Where to go next
----------------------------------------

* Follow the :doc:`getting_started/index` guide to set up the environment and run the package.
* Work through the :doc:`examples/examples` to run trajectory, perception, and intelligence demos.
* See :doc:`integration/integration` for the supported motion-planning and application integrations.
* Refer to the :doc:`api_reference/api_reference` for ROS2 services, topics, and actions.
* Consult :doc:`support` for common issues and their resolutions.







.. toctree::
   :maxdepth: 3

   getting_started/index
   examples/examples
   integration/integration
   api_reference/api_reference
   support
   about