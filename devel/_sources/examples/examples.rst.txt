Example Applications
====================

This section provides complete examples that you can run from start to finish
on the WMX R2 stack. The **manipulator scenarios** come from the
`movensys-manipulator <https://github.com/movensys/movensys-manipulator>`_
repository (Dobot CR3A / CR5A arms with MoveIt2 / Isaac cuMotion planning and
Nvblox / YOLO / AprilTag perception). The **navigation scenarios** come from the
`movensys-navigation <https://github.com/movensys/movensys-navigation>`_
repository (a differential-drive base with Nav2 planning, EKF odometry, and SLAM
mapping). The **Robopoly game** is a voice-driven VLM/LLM application from the
`movensys-intelligence <https://github.com/movensys/movensys-intelligence>`_
repository, built on top of the manipulator stack.

Every manipulator and navigation scenario runs in three execution modes:

- **Simulation** -- pure simulation (Isaac Sim or Gazebo), no hardware
- **HIL** -- hardware-in-the-loop: simulator visuals with the real WMX runtime
- **Real** -- the real robot via WMX over EtherCAT

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Application stacks

   isaacsim_setup
   movensys_manipulator
   movensys_navigation

Common Requirements
-------------------

- The core WMX R2 packages built and the WMX Runtime at ``/opt/wmx3/``
  (see :doc:`../getting_started/index`)
- Docker with ``docker compose`` (the examples run inside containers)
- An NVIDIA GPU and Isaac ROS prerequisites for the ``isaac-ros_*`` images
- EtherCAT hardware for HIL and Real modes
- The `movensys-simulation <https://github.com/movensys/movensys-simulation>`_
  repo for the Isaac Sim scenes

Before running any scenario, set up the stack once — see
:doc:`movensys_manipulator_setup` for manipulator scenarios and
:doc:`movensys_navigation_setup` for navigation scenarios.

Development Roadmap
-------------------

The examples are under active development. Planned and in-progress work is
tracked below.

.. list-table::
   :header-rows: 1
   :widths: 33 33 34

   * - 2026 Q1
     - 2026 Q2
     - 2026 Q3
   * - - Add WMX3 general node
       - Add trajectory example
       - Add Apriltag example
       - Add movensys_isaac_manipulator
       - Add movensys_intel_manipulator
       - Add movensys_thor_manipulator
       - Add robotic_isaac_sim
       - Add Apriltag example

     - - Support arm64/amd64
       - Support ROS2 humble/jazzy
       - Support dobot cr3a/cr5a
       - Add Joint Trajectory Controller node
       - Add Gripper Controller node
       - Add movensys-manipulator
       - Add movensys-simulation
       - Add movensys-intelligence
       - Add Apriltag + Obstacle avoidance example
       - Add Robopoly example
       - Delete robotic_isaac_sim
       - Delete movensys_isaac_manipulator
       - Delete movensys_intel_manipulator
       - Delete movensys_thor_manipulator
       
     - - Add movensys-navigation
       - Add Diffbot in isaacsim
       - Add differential drive controller node
       - ros2_control integration
       - Support Jetson Development Kit 
       - Universal NIC Kernel driver
       - Free license for 6 hours
