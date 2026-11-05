WMX R2 Documentation
=======================

WMX R2 brings the ROS 2 ecosystem into deterministic real-time industrial
motion control. It connects a ROS 2 interface to the WMX motion engine and
drives industrial servos over EtherCAT. EtherCAT is one of the most widely used
real-time industrial Ethernet networks, and it links the controller to the servo
drives and I/O over a single cable.


Turn Physical AI decisions into precise industrial motion
--------------------------------------------------------------------

WMX R2 turns planner output, such as MoveIt2 and Nav2 trajectories, into
precisely timed servo commands. It also gives direct control of the axes, the
I/O, the motion engine and the EtherCAT network, which is what industrial
commissioning and diagnostics need. In the *See–Think–Act* loop of Physical AI,
WMX R2 is the *Act* layer. It executes what the AI decides, on real industrial
hardware, in deterministic real time.

.. figure:: /_static/images/AI_Decision_Servo_WMX-R2_Workflow.png
   :alt: From AI decision to servo through WMX R2
   :align: center
   :width: 100%

   From AI decision to servo. WMX R2 computes the robot kinematics and path
   inside the real-time loop, every cycle.

The chips are here and the AI models are here. What is missing is real-time
execution. WMX R2 completes **One-Chip Physical AI**: perception, reasoning,
planning, kinematics and motion control all running on a single chip.

.. figure:: /_static/images/WMX_R2_One_Chip.png
   :alt: WMX R2: One-Chip Physical AI
   :align: center
   :width: 100%

   WMX R2 completes One-Chip Physical AI. ROS 2 perception, reasoning and
   planning, and WMX R2 real-time execution share one SoC (CPU, GPU and NPU)
   and drive robot arms, servos and I/O directly over EtherCAT.


Bring modern robotics capability to industrial-grade motion
--------------------------------------------------------------------

Industrial motion controllers execute deterministically but have no path to
modern robotics software, and ROS 2 has that software but cannot guarantee
cycle-accurate execution on real hardware. WMX R2 closes the gap. ROS 2 nodes
reason, plan and control, and the WMX motion engine turns their output into
precisely timed servo commands on a fixed cycle over EtherCAT.

.. figure:: /_static/images/the_gap.png
   :alt: WMX R2 closing the gap between ROS 2 and industrial motion control
   :align: center
   :width: 100%

   WMX R2 closing the gap between ROS 2 and industrial motion control.


Drive any EtherCAT robot or machine, regardless of the brand
--------------------------------------------------------------------

WMX R2 commands the servo drives directly over EtherCAT using CoE (CANopen over
EtherCAT), the standard protocol industrial servo drives already implement. It
does not go through the robot manufacturer's controller. It controls axes rather
than a specific robot model, so neither the brand of the robot nor the brand of
the drives matters. A six-axis arm on an assembly line, a mobile base moving
material through a plant and a custom multi-axis machine are all driven the same
way.


Free to start with
--------------------------------------------------------------------

You can evaluate WMX R2 on real industrial hardware at no cost. The WMX motion
engine runs **free in 6-hour sessions**, renewed by restarting the engine. That
is enough to commission a machine, work through the examples, and develop and
test a complete application. A commercial license lifts the session time limit, and is what
production use requires.

The ROS 2 interface is open source under the MIT license. It handles the
timing-sensitive step: smoothing trajectories, coordinating joints and emitting
commands at the rate servo drivers expect. It runs on the WMX motion engine,
which keeps motion on a deterministic cycle and exposes more than 200 APIs for
trajectory conversion, EtherCAT, I/O and engine control. The WMX engine, its SDK and
its binaries are proprietary of `Movensys <https://movensys.com/>`_. :doc:`licensing` sets out the boundary.


Start from ready-made examples instead of from scratch
------------------------------------------------------------------

Four companion repositories show how these pieces fit together on real
hardware. Each one is a working reference implementation built on WMX R2, and a
starting point for an industrial application of your own:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Repository
     - What it provides
   * - `movensys-manipulator <https://github.com/movensys/movensys-manipulator>`_
     - Manipulator scenarios with MoveIt2 / Isaac cuMotion planning and
       Nvblox / YOLO / AprilTag perception
   * - `movensys-navigation <https://github.com/movensys/movensys-navigation>`_
     - A differential-drive mobile base with Nav2 planning, EKF odometry and
       SLAM mapping
   * - `movensys-intelligence <https://github.com/movensys/movensys-intelligence>`_
     - A voice-driven VLM/LLM application (the Robopoly game) built on top of
       the manipulator stack
   * - `movensys-simulation <https://github.com/movensys/movensys-simulation>`_
     - The Isaac Sim scenes used by the manipulator and navigation scenarios

Each application repository runs in its own container and talks to WMX R2 over
DDS, so the planning stack and the real-time stack stay separate processes on
the same machine.

See :doc:`examples/examples` to run these scenarios from start to finish.

.. figure:: /_static/images/wmx-r2_overview.drawio.png
   :alt: WMX R2 architecture overview
   :align: center
   :width: 100%

   WMX R2 architecture overview.


Integrate with the most popular ROS 2 ecosystem you already use
-------------------------------------------------------------------------

WMX R2 works with the widely popular projects of the ROS 2 ecosystem, so an
industrial machine can reuse what the robotics community already builds:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Project
     - What it is popular for
   * - `MoveIt2 <https://moveit.ai/>`_
     - Manipulator motion planning
   * - `Nav2 <https://nav2.org/>`_
     - Mobile robot navigation
   * - `ros2_control <https://control.ros.org/>`_
     - Hardware interface and controller management
   * - `Intel OpenVINO <https://docs.openvino.ai/2026/index.html>`_
     - Optimized inference on Intel XPU and integrated accelerators
   * - `NVIDIA Isaac Sim <https://developer.nvidia.com/isaac/sim>`_ and
       `Gazebo <https://gazebosim.org/>`_
     - Simulation and hardware-in-the-loop testing
   * - `NVIDIA Isaac ROS <https://developer.nvidia.com/isaac/ros>`_
     - NVIDIA GPU accelerated perception and control
   * - `YOLO <https://docs.ultralytics.com/>`_
     - Real-time object detection
   * - `Gemma <https://ai.google.dev/gemma>`_ and other multimodal LLMs and VLMs
     - Natural language task specification and high-level reasoning

See WMX R2 in action:

.. raw:: html

   <div style="position: relative; width: 100%; max-width: 800px; margin: 1em auto; aspect-ratio: 16 / 9;">
     <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
             src="https://www.youtube-nocookie.com/embed/2JlqxwyMN_E"
             title="WMX R2 demo video for Intel Edge Day"
             allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
             allowfullscreen></iframe>
   </div>


.. raw:: html

   <div style="position: relative; width: 100%; max-width: 800px; margin: 1em auto; aspect-ratio: 16 / 9;">
     <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
             src="https://www.youtube-nocookie.com/embed/h-G9vtAGAIU"
             title="WMX R2 demo video for GTC conference"
             allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
             allowfullscreen></iframe>
   </div>


One-Chip Physical AI: from AI decision to precision motion
--------------------------------------------------------------------

WMX R2 runs real-time robot motion on the same chip that runs the AI.
Perception, reasoning, planning and motion control share one SoC. No second
computer and no motion controller box are needed. The servo drives, sensors and
cables stay outside the chip.

.. figure:: /_static/images/wmx-r2_overview_one-chip.drawio.png
   :alt: WMX R2 One-Chip Physical AI architecture overview
   :align: center
   :width: 100%

   WMX R2 on one chip. Robotics AI packages and the WMX R2 nodes share the
   SoC with the WMX motion engine in the real-time domain. The engine drives
   robot arms, servos, I/O and AMRs over EtherCAT.

Why one chip
~~~~~~~~~~~~

* **Fewer boxes.** One computer replaces an AI PC plus a motion controller.
* **Less wiring.** The chip drives the servos directly over one EtherCAT cable.
* **A shorter path.** The AI decision reaches the servos without a hop to
  another controller.
* **One software stack.** One system to install, update and maintain.

.. figure:: /_static/images/one_ipc.png
   :alt: Conventional motion control versus WMX software motion on a single PC
   :align: center
   :width: 100%

   Conventional motion control goes through a separate motion controller. WMX
   software motion drives the servos directly from the chip that runs the AI.

Who does what on the chip
~~~~~~~~~~~~~~~~~~~~~~~~~

The AI stack thinks. WMX R2 moves.

.. list-table::
   :header-rows: 1
   :widths: 22 38 40

   * - Layer
     - What it does
     - What runs it
   * - Perception
     - Sees objects, poses and obstacles
     - AI models on the GPU or NPU
   * - Reasoning
     - Understands the task, often from voice or text
     - LLMs and VLMs on the GPU or NPU
   * - Planning
     - Finds a safe path for the robot
     - MoveIt2, Nav2 or a GPU planner
   * - Motion control
     - Turns the path into servo commands on a fixed cycle
     - WMX R2 on isolated CPU cores
   * - Field network
     - Sends commands to the drives and reads feedback
     - WMX R2 EtherCAT master on a standard Ethernet port

You can use the AI stack of the chip vendor or open-source ROS 2 packages.
WMX R2 works with both.

Why the motion layer matters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An EtherCAT master only moves data between the computer and the drives. A
robot needs more:

* trajectory generation and smoothing
* coordinated motion across many axes
* interpolation of lines, arcs and splines
* a new command for every servo on every cycle
* error handling at the servo level

The WMX motion engine provides all of this. WMX R2 brings it to ROS 2 and to
the Physical AI chip.

Chip platforms
~~~~~~~~~~~~~~

WMX R2 is software. It runs on x86-64 and arm64 with a real-time Linux kernel.
The same stack runs on both, from an industrial PC to a developer kit or a
laptop.

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Chip
     - Architecture
     - How the work splits
   * - NVIDIA Jetson Thor and Jetson Orin
     - arm64
     - Isaac ROS, cuMotion and Nvblox run on the GPU. WMX R2 runs the motion
       on isolated CPU cores.
   * - Intel Core Ultra Series 3
     - x86-64
     - Open-source ROS 2 packages with OpenVINO run on the NPU and GPU. WMX R2
       runs the motion on isolated CPU cores.

These combinations have been run with WMX R2:

.. list-table::
   :header-rows: 1
   :widths: 34 34 32

   * - Computer
     - Chip
     - OS
   * - Advantech MIC-743
     - NVIDIA Jetson Thor
     - Ubuntu 24.04
   * - Advantech MIC-733-AO
     - NVIDIA Jetson Orin AGX
     - Ubuntu 22.04
   * - NVIDIA Jetson AGX Orin Developer Kit
     - NVIDIA Jetson Orin AGX
     - Ubuntu 24.04
   * - Advantech UNO-258
     - Intel Core Ultra Series 3
     - Ubuntu 24.04
   * - Intel Robotics Kit
     - Intel Core Ultra Series 3
     - Ubuntu 24.04

The :doc:`examples/robopoly_game` example runs the full loop on one chip:
voice, VLM, YOLO, MoveIt2 and WMX R2 driving the arm over EtherCAT.


Take robotics from the laboratory to the production floor
--------------------------------------------------------------------

A research robot can tolerate jitter, missed cycles and frequent restarts. An
industrial robot on a production machine cannot. It has to hold path accuracy,
react to I/O within a known time and run for long periods without drift. WMX R2
keeps the ROS 2 development workflow and adds what production needs:
deterministic cycle timing, servo-level error handling and direct access to the
drives.


Cut tracking error by 85% against an external controller
--------------------------------------------------------------------

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item::

      .. figure:: /_static/images/graph_1.png
         :alt: Representative single run, joint-angle tracking
         :width: 100%

         Representative run: joint-angle tracking for the commanded reference,
         a traditional external motion controller, and WMX R2.

   .. grid-item::

      .. figure:: /_static/images/graph_2.png
         :alt: Mean absolute tracking error across ten runs
         :width: 100%

         Per-sample mean absolute error across ten runs.

WMX R2 followed the commanded trajectory with **85% lower mean absolute error
(MAE)** than a conventional external motion controller. We ran the same
trajectory ten times on each setup. The left panel shows a representative run,
and the right panel shows the per-sample MAE across all ten. The gain comes from
removing the TCP/IP hop and the redundant control stage that an external
controller adds, which cuts communication latency out of the control path.


Customers and Partners
----------------------------------------

WMX R2 is built on the WMX motion engine, which has a long, proven industrial
track record:

* 25+ years of development with 40+ patents worldwide
* 40,000+ cumulative licenses sold
* 500+ customers, mainly in the semiconductor industry

.. Add customer and partner logos or names here.


Where to go next
----------------------------------------

* Follow the :doc:`getting_started/index` guide to set up the environment and run the package.
* Work through the :doc:`examples/examples` to run trajectory, perception, and intelligence demos.
* See :doc:`integration/integration` for the supported motion-planning and application integrations.
* Work through :doc:`try_your_robot/index` before moving a physical robot;
  parameter validation, first motion, safety responsibilities, and the list of
  validated robots.
* Refer to the :doc:`api_reference/api_reference` for ROS2 services, topics, and actions.
* Consult :doc:`support` for common issues and their resolutions.
* Read :doc:`licensing` for the boundary between the MIT-licensed ROS 2
  interface and the proprietary WMX motion engine.








.. toctree::
   :maxdepth: 3

   getting_started/index
   examples/examples
   try_your_robot/index
   integration/integration
   api_reference/api_reference
   support
   licensing
   about
