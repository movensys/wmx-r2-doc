WMX R2 Documentation
=======================

**From AI decision to precision motion. All on one chip.**

WMX R2 gives Physical AI robots the real-time motion control they need. The AI
decides what the robot should do. WMX R2 makes the robot do it with precise
and repeatable motion. Both run on the same chip, and WMX R2 talks to the
servo drives over EtherCAT, the industrial network that most servo drives
already support.


One-Chip Physical AI
--------------------------------------------------------------------

Every Physical AI robot works in a loop of three steps. It **sees** the world
through cameras and sensors. It **thinks** about what to do with AI models.
Then it **acts** by moving its joints or wheels.

Modern chips are now powerful enough to run the seeing and thinking parts. AI
models are ready too. The missing piece has been the acting part. Robot motion
must happen on a strict schedule, often every millisecond, and the AI computer
could not guarantee that. So most robots still need a separate motion
controller box.

WMX R2 fills that gap. It runs real-time motion control as software on the same
chip as the AI. Seeing, thinking and acting all happen on one chip. We call this
**One-Chip Physical AI**.

.. figure:: /_static/images/WMX_R2_One_Chip.png
   :alt: WMX R2: One-Chip Physical AI
   :align: center
   :width: 100%

   One-Chip Physical AI. The AI and WMX R2 share one chip (CPU, GPU and NPU)
   and control robots, servos and I/O over EtherCAT.


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


From AI decision to servo
--------------------------------------------------------------------

WMX R2 is the *act* step of the loop. The AI decides where the robot should go.
WMX R2 works out how each joint must move to get there. Then it sends a new
command to every servo on every cycle, right on time.

.. figure:: /_static/images/AI_Decision_Servo_WMX-R2_Workflow.png
   :alt: From AI decision to servo through WMX R2
   :align: center
   :width: 100%

   From AI decision to servo. WMX R2 computes the robot kinematics and path
   inside the real-time loop, every cycle.

Inside one chip, the work is shared. The GPU and NPU are built for AI, so they
take care of seeing, thinking and planning. WMX R2 runs on a few CPU cores that
are kept just for motion. Nothing else runs there, so the servos get their
commands on time even when the AI is busy. You can also keep the AI tools you
already like. Use the robotics software that comes with your chip or build with
open-source ROS 2 packages. Either way, WMX R2 takes the plan from the AI and
turns it into motion.


One architecture for any device
--------------------------------------------------------------------

WMX R2 uses the same software for every machine. A robot arm, a mobile robot or
a set of servos and I/O all run on the same stack. What changes from one machine
to the next is only its configuration. You describe your machine in four files
and WMX R2 does the rest. There is no code to write.

.. figure:: /_static/images/wmx-r2_overview_one-chip.drawio.png
   :alt: WMX R2 One-Chip Physical AI architecture overview
   :align: center
   :width: 100%

   The WMX R2 architecture on one chip. Robotics AI packages, WMX R2 and the
   WMX3 motion engine run side by side. Four configuration files adapt it to
   your machine.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Configuration file
     - What you describe in it
   * - WMX-R2 config
     - How the robot appears in ROS 2: its joints, controllers, topics and
       services.
   * - WMX3 Params
     - How each axis behaves: gear ratio, encoder resolution, direction,
       limits and home position.
   * - WMX3 Robot Option Params
     - What kind of robot it is, such as a 6-axis arm or a SCARA, and its
       dimensions.
   * - ENI files
     - Which drives and I/O modules are on the EtherCAT network, and in what
       order.

This saves a lot of engineering time. You do not build a new controller for
each machine. You fill in the files and start testing. See
:doc:`try_your_robot/index` to set them up for your robot.


Why one chip
--------------------------------------------------------------------

Putting everything on one chip makes a robot simpler to build and to own.

* **Fewer boxes.** One computer does the job of an AI PC and a motion
  controller.
* **Less wiring.** A single EtherCAT cable runs from the computer to the servo
  drives.
* **Faster response.** The AI decision goes straight to the servos. It does not
  pass through another controller first.
* **Easier upkeep.** There is one system to install, update and maintain.

.. figure:: /_static/images/one_ipc.png
   :alt: Conventional motion control versus WMX software motion on a single PC
   :align: center
   :width: 100%

   Left: a conventional setup needs a separate motion controller. Right: WMX
   drives the servos directly from the same chip that runs the AI.

WMX R2 is pure software. It runs on both x86-64 and arm64 chips with real-time
Linux. You can use an industrial PC, a developer kit or even a laptop. The same
software and the same setup work on all of them.

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

Bring modern robotics capability to industrial-grade motion
--------------------------------------------------------------------

Industrial motion controllers execute deterministically but have no path to
modern robotics software, and ROS 2 has that software but cannot guarantee
cycle-accurate execution on real hardware. WMX R2 closes the gap. ROS 2 nodes
reason, plan and control, and the WMX motion engine turns their output into
precisely timed servo commands on a fixed cycle over EtherCAT.

Drive any EtherCAT robot or machine, regardless of the brand
--------------------------------------------------------------------

WMX R2 commands the servo drives directly over EtherCAT, the standard protocol industrial servo drives already implement. It
does not go through the robot manufacturer's controller. It controls axes rather
than a specific robot model, so neither the brand of the robot nor the brand of
the drives matters. A six-axis arm on an assembly line, a mobile base moving
material through a plant and a custom multi-axis machine are all driven the same
way.

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
