import os

base = os.path.expanduser("~/wmx_r2_doc/doc")

files = {

"index.rst": """WMX R2 Driver Documentation
===============================

Overview
--------

Welcome to the WMX R2 Driver documentation. This project provides
ROS2 packages for controlling Dobot collaborative robots (CR series)
with MoveIt2 motion planning integration.

**Supported Scenarios:**

- MoveIt2 Motion Planning
- Isaac cuMotion (GPU-accelerated trajectory planning)
- Custom Planner Integration

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   environment/environment
   quick_start/quick_start

.. toctree::
   :maxdepth: 2
   :caption: Packages

   packages/packages

.. toctree::
   :maxdepth: 2
   :caption: Integration Scenarios

   integration/integration

.. toctree::
   :maxdepth: 2
   :caption: Architecture & Design

   architecture/architecture

.. toctree::
   :maxdepth: 2
   :caption: Performance

   performance/performance

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference/api_reference

.. toctree::
   :maxdepth: 2
   :caption: Deployment

   deployment/deployment

.. toctree::
   :maxdepth: 2
   :caption: Support

   troubleshooting/troubleshooting
""",

"environment/environment.rst": """Environment
===========

.. toctree::
   :maxdepth: 2

   system_requirements
   supported_models
   ros2_installation
""",

"environment/system_requirements.rst": """System Requirements
===================

Operating System
----------------

- Ubuntu 22.04 (Jammy)
- Ubuntu 24.04 (Noble)

ROS2 Distribution
-----------------

- ROS2 Humble Hawksbill
- ROS2 Jazzy Jalisco

Hardware Requirements
---------------------

- CPU: TODO
- RAM: TODO
- GPU (for cuMotion): TODO
- Network: Ethernet connection to Dobot controller

Software Dependencies
---------------------

- MoveIt2
- ros2_control
""",

"environment/supported_models.rst": """Supported Models
================

Dobot CR Series
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Model
     - Payload
     - Reach
     - Status
   * - CR3
     - 3 kg
     - 795 mm
     - TODO
   * - CR5
     - 5 kg
     - 900 mm
     - TODO
   * - CR10
     - 10 kg
     - 1525 mm
     - TODO
   * - CR16
     - 16 kg
     - 1223 mm
     - TODO
""",

"environment/ros2_installation.rst": """ROS2 Installation
=================

This guide walks through installing ROS2 on Ubuntu.

.. note::

   Follow the official `ROS 2 Installation Guide <https://docs.ros.org/en/humble/Installation.html>`_
   for the Desktop Install of ROS2 Humble.

1. Set Locale
-------------

.. code-block:: bash

   locale
   sudo apt update && sudo apt install locales
   sudo locale-gen en_US en_US.UTF-8
   sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
   export LANG=en_US.UTF-8

2. Setup Sources
----------------

.. code-block:: bash

   sudo apt install software-properties-common
   sudo add-apt-repository universe
   sudo apt update && sudo apt install curl -y
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

3. Install ROS2
----------------

.. code-block:: bash

   sudo apt update
   sudo apt upgrade
   sudo apt install ros-humble-desktop

4. Environment Setup
--------------------

.. code-block:: bash

   echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
   source ~/.bashrc

5. Verify Installation
----------------------

.. code-block:: bash

   ros2 run demo_nodes_cpp talker
""",

"quick_start/quick_start.rst": """Quick Start
===========

This guide will help you get up and running with the WMX R2 Driver.

.. note::

   This guide assumes basic familiarity with ROS2, Ubuntu, and Dobot hardware.
   See the :doc:`../environment/system_requirements` page.

.. toctree::
   :maxdepth: 2

   install_dependencies
   mock_hardware
   physical_hardware
""",

"quick_start/install_dependencies.rst": """Install Dependencies
====================

Source Build
------------

.. code-block:: bash

   mkdir -p ~/wmx_ws/src
   cd ~/wmx_ws/src

   git clone https://github.com/YOUR_ORG/dobot_moveit.git
   git clone https://github.com/YOUR_ORG/dobot_robot_interface.git
   git clone https://github.com/YOUR_ORG/dobot_description.git

   cd ~/wmx_ws
   sudo apt update
   rosdep update
   rosdep install --ignore-src --from-paths src -y

   colcon build --symlink-install
   source install/setup.bash
""",

"quick_start/mock_hardware.rst": """Launching with Mock Hardware
============================

You can test the MoveIt2 integration without a physical robot.

1. Launch MoveIt2 with Mock Hardware
-------------------------------------

.. code-block:: bash

   ros2 launch dobot_moveit dobot_moveit.launch.py use_mock:=true

2. Verify in RViz
------------------

TODO: Add RViz screenshot and verification steps
""",

"quick_start/physical_hardware.rst": """Launching with Physical Hardware
=================================

Prerequisites
-------------

- Dobot robot powered on
- Ethernet cable connected between PC and Dobot controller
- Robot IP address configured

1. Network Configuration
-------------------------

TODO: Add network setup

2. Enable Robot
----------------

.. code-block:: bash

   ros2 launch dobot_robot_interface dobot_interface.launch.py robot_ip:=192.168.1.6
   ros2 service call /EnableRobot dobot_msgs/srv/EnableRobot

3. Launch MoveIt2
------------------

.. code-block:: bash

   ros2 launch dobot_moveit dobot_moveit.launch.py
""",

"packages/packages.rst": """Packages
========

Overview of the WMX R2 packages.

.. toctree::
   :maxdepth: 2

   dobot_description
   dobot_robot_interface
   dobot_moveit
""",

"packages/dobot_description.rst": """dobot_description
=================

Overview
--------

This package contains URDF xacros and mesh assets for Dobot robots.

Package Structure
-----------------

.. code-block:: text

   dobot_description/
   ├── launch/
   ├── meshes/
   ├── urdf/
   ├── rviz/
   ├── CMakeLists.txt
   └── package.xml

Visualizing the Robot
---------------------

.. code-block:: bash

   ros2 launch dobot_description view_robot.launch.py model:=cr5
""",

"packages/dobot_robot_interface.rst": """dobot_robot_interface
=====================

Overview
--------

This package provides the ROS2 interface to the Dobot robot controller
via TCP/IP.

Key Components
--------------

- **main.cpp** - Entry point
- **CRRobotRos2** - Core communication class
- **CRCommanderRos2** - TCP command serialization

ROS2 Services
-------------

.. list-table::
   :header-rows: 1

   * - Service
     - Description
   * - /EnableRobot
     - Enable the robot
   * - /ServoJ
     - Joint servo command
   * - Other
     - Control, Motion, IO, Safety, Config

Publishers
----------

.. list-table::
   :header-rows: 1

   * - Topic
     - Type
   * - /joint_states
     - sensor_msgs/JointState
   * - /robot_status
     - TODO
   * - /tool_vector
     - TODO
""",

"packages/dobot_moveit.rst": """dobot_moveit
=============

Overview
--------

MoveIt2 Action Server for Dobot robots.

Launch Sequence
---------------

.. code-block:: text

   ros2 launch dobot_moveit
       -> dobot_moveit.launch.py
       -> Reads DOBOT_TYPE environment
       -> dobot-joint.launch.py + Model-Specific Launch

MoveIt Nodes
------------

- **joint_states** (State)
- **action_move_server** (MoveIt Action)

Usage
-----

.. code-block:: bash

   ros2 launch dobot_moveit dobot_moveit.launch.py
   DOBOT_TYPE=cr5 ros2 launch dobot_moveit dobot_moveit.launch.py
""",

"integration/integration.rst": """Integration Scenarios
=====================

.. toctree::
   :maxdepth: 2

   moveit2_integration
   cumotion_integration
   custom_planner
""",

"integration/moveit2_integration.rst": """MoveIt2 Motion Planning
========================

Overview
--------

The primary integration scenario: MoveIt2 for motion planning
and trajectory execution on Dobot collaborative robots.

Architecture
------------

.. code-block:: text

   User Application
       -> ROS2_MoveIt_Action_Server
           -> action_move_server
               -> ROS2_Dobot_Robot_Interface
                   -> ServoJ / EnableRobot
                       -> TCP/IP -> Dobot Controller -> Robot

Setup
-----

TODO: Add setup instructions

Usage Example
-------------

TODO: Add usage example
""",

"integration/cumotion_integration.rst": """Isaac cuMotion Accelerated Planning
=====================================

Overview
--------

NVIDIA Isaac cuMotion provides GPU-accelerated trajectory planning.

Prerequisites
-------------

- NVIDIA GPU with CUDA support
- Isaac ROS packages installed

TODO: Add setup and usage instructions
""",

"integration/custom_planner.rst": """Custom Planner Integration
===========================

Overview
--------

The WMX R2 Driver supports pluggable motion planners.

TODO: Add instructions for integrating custom planners
""",

"architecture/architecture.rst": """Architecture & Design
=====================

.. toctree::
   :maxdepth: 2

   system_overview
   communication
   flowcharts
""",

"architecture/system_overview.rst": """System Overview
===============

The system consists of three main layers:

1. **ROS2 MoveIt Action Server** - Motion planning and trajectory generation
2. **ROS2 Dobot Robot Interface** - ROS2 services and TCP communication
3. **Dobot Robot Controller** - Hardware control via TCP/IP Ethernet

TODO: Add architecture diagram
""",

"architecture/communication.rst": """Communication
=============

ROS2 Communication
------------------

TODO: Describe ROS2 topics, services, and actions

TCP/IP Communication
--------------------

TODO: Describe TCP connection to Dobot controller
""",

"architecture/flowcharts.rst": """Flowcharts
==========

Launch Sequence
---------------

TODO: Add launch sequence flowchart

Motion Execution Flow
---------------------

TODO: Add motion execution flowchart
""",

"performance/performance.rst": """Performance
===========

.. toctree::
   :maxdepth: 2

   nfr
   benchmarks
""",

"performance/nfr.rst": """Non-Functional Requirements
===========================

.. list-table::
   :header-rows: 1

   * - Category
     - Metric
     - Target
   * - Latency
     - Command round-trip time
     - TODO
   * - Throughput
     - Joint state publish rate
     - TODO
   * - Reliability
     - Uptime
     - TODO
   * - Safety
     - Emergency stop response time
     - TODO
""",

"performance/benchmarks.rst": """Benchmarks
==========

Test Environment
----------------

TODO: Describe test setup

Results
-------

TODO: Add benchmark data
""",

"api_reference/api_reference.rst": """API Reference
=============

.. toctree::
   :maxdepth: 2

   ros2_services
   ros2_topics
   ros2_actions
""",

"api_reference/ros2_services.rst": """ROS2 Services
==============

Control Services
----------------

.. list-table::
   :header-rows: 1

   * - Service Name
     - Description
   * - /EnableRobot
     - Enable the robot
   * - /DisableRobot
     - Disable the robot

Motion Services
---------------

.. list-table::
   :header-rows: 1

   * - Service Name
     - Description
   * - /ServoJ
     - Joint servo command

IO Services
-----------

TODO

Safety Services
---------------

TODO

Config Services
---------------

TODO
""",

"api_reference/ros2_topics.rst": """ROS2 Topics
============

Published Topics
----------------

.. list-table::
   :header-rows: 1

   * - Topic
     - Type
     - Description
   * - /joint_states
     - sensor_msgs/JointState
     - Current joint positions
   * - /robot_status
     - TODO
     - Robot status
   * - /tool_vector
     - TODO
     - Tool center point position
""",

"api_reference/ros2_actions.rst": """ROS2 Actions
=============

MoveIt Action
-------------

.. list-table::
   :header-rows: 1

   * - Action
     - Type
     - Description
   * - /action_move
     - moveit_msgs/action/MoveGroup
     - MoveIt2 motion planning and execution
""",

"deployment/deployment.rst": """Deployment
==========

.. toctree::
   :maxdepth: 2

   source_build
   debian_install
   docker
""",

"deployment/source_build.rst": """Source Build
============

.. code-block:: bash

   mkdir -p ~/wmx_ws/src
   cd ~/wmx_ws/src

   git clone https://github.com/YOUR_ORG/dobot_description.git
   git clone https://github.com/YOUR_ORG/dobot_robot_interface.git
   git clone https://github.com/YOUR_ORG/dobot_moveit.git

   cd ~/wmx_ws
   rosdep update
   rosdep install --ignore-src --from-paths src -y
   colcon build --symlink-install
   source install/setup.bash
""",

"deployment/debian_install.rst": """Debian Package Install
======================

.. note::

   Debian packages are not yet available.

Future Installation
-------------------

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install ros-humble-wmx-dobot-moveit
   sudo apt-get install ros-humble-wmx-dobot-robot-interface
""",

"deployment/docker.rst": """Docker
======

.. note::

   Docker support is planned for future releases.

.. code-block:: bash

   docker pull your-org/wmx-r2:humble
   docker run --gpus all --net=host your-org/wmx-r2:humble
""",

"troubleshooting/troubleshooting.rst": """Troubleshooting
===============

Connection Failed
-----------------

**Symptom:** Cannot connect to Dobot robot controller.

**Solution:**

- Check Ethernet cable connection
- Verify IP address: ``ping 192.168.1.6``

Robot Not Enabled
-----------------

**Symptom:** Motion commands are rejected.

**Solution:**

- Call ``/EnableRobot`` service first

MoveIt Planning Failed
----------------------

**Symptom:** MoveIt2 fails to find a trajectory.

**Solution:**

- Check joint limits in URDF
- Verify target pose is reachable

Build Errors
------------

**Solution:**

.. code-block:: bash

   rosdep install --ignore-src --from-paths src -y

Getting Help
------------

- GitHub Issues: https://github.com/YOUR_ORG/dobot_moveit/issues
""",

}

for filepath, content in files.items():
    full_path = os.path.join(base, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.lstrip('\n'))
    print(f"Created: {filepath}")

print("\nDone! All 31 files created.")

