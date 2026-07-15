Install WMX ROS2 Package
========================

With the :doc:`computer_setup` complete (real-time kernel, ROS 2, and the WMX
runtime in place), build the WMX ROS2 packages.

Configure the environment
-------------------------

Add the following to your ``~/.bashrc``:

.. code-block:: bash

   export ROS_DOMAIN_ID=70                         #use any number
   export ROS_DISTRO=jazzy                         #support {jazzy, humble}
   export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

   source /opt/ros/$ROS_DISTRO/setup.bash
   source ~/workspaces/movensys_ws/install/setup.bash

Apply the changes:

.. code-block:: bash

   source ~/.bashrc


Install Required ROS2 Dependencies
----------------------------------------------

.. code-block:: bash

   sudo apt update
   sudo apt install -y ros-${ROS_DISTRO}-graph-msgs \
                    ros-${ROS_DISTRO}-moveit-ros \
                    ros-${ROS_DISTRO}-moveit-planners \
                    ros-${ROS_DISTRO}-moveit-plugins \
                    ros-${ROS_DISTRO}-moveit-setup-assistant \
                    ros-${ROS_DISTRO}-moveit-configs-utils \
                    ros-${ROS_DISTRO}-moveit-task-constructor-core \
                    ros-${ROS_DISTRO}-ros2-control \
                    ros-${ROS_DISTRO}-ros2-controllers \
                    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp
   sudo apt install -y python3-colcon-common-extensions python3-rosdep


Create Workspace and Build
--------------------------

**Create workspace**

.. code-block:: bash

   mkdir -p ~/workspaces/movensys_ws/src
   cd ~/workspaces/movensys_ws/src && \
   git clone https://github.com/movensys/wmx-ros2.git

**Rosdep update**

.. code-block:: bash

   sudo rosdep init   # only needed once per system
   rosdep update
   cd ~/workspaces/movensys_ws
   rosdep install --from-paths src --ignore-src -y

**Build** (``wmx_ros2_package`` depends on ``wmx_ros2_message``, so build the
message package first):

.. code-block:: bash

   cd ~/workspaces/movensys_ws

   # Stage 1: build the message package first
   colcon build --packages-select wmx_ros2_message
   source install/setup.bash

   # Stage 2: build all remaining packages
   colcon build
   source install/setup.bash


Verify Installation
-------------------

.. code-block:: bash

   ros2 pkg list | grep wmx && ros2 pkg executables wmx_ros2_package

Expected:

.. code-block:: text

   wmx_ros2_control
   wmx_ros2_message
   wmx_ros2_package
   wmx_ros2_package differential_drive_controller
   wmx_ros2_package gripper_controller
   wmx_ros2_package joint_state_broadcaster
   wmx_ros2_package joint_trajectory_controller
   wmx_ros2_package wmx_core_motion_node
   wmx_ros2_package wmx_engine_node
   wmx_ros2_package wmx_ethercat_node
   wmx_ros2_package wmx_io_node



Testing WMX ROS2
----------------

Once WMX ROS2 is installed and built, you can validate it in two ways: in
simulation (no physical hardware required) or against real EtherCAT hardware.
Start with simulation to verify basic behavior, then move to real hardware.

The WMX ROS2 nodes communicate directly with the WMX engine over EtherCAT —
there is no built-in mock hardware mode. The mode is selected in
``/opt/wmx3/Module.ini`` by enabling either the simulation or the EtherCAT
platform. Select your mode below, then continue with the common test steps
that follow.

.. tab-set::

   .. tab-item:: Simulation
      :sync: sim

      Use the simulation platform to test without any physical hardware
      connected.

      **Setup WMX in simulation mode**

      Modify ``/opt/wmx3/Module.ini`` to disable the EtherCAT platform and
      enable the simulation platform:

      .. code-block:: ini

         [Platform 0]
         Location = ./platform/ethercat
         DllName = ec_platform.so
         NumOfMaster = 1
         disable = 1

         [Platform 1]
         Location = ./platform/simu
         DllName = simu_platform.so
         NumOfMaster = 1
         disable = 0

   .. tab-item:: Real Hardware
      :sync: real

      This covers testing against any EtherCAT hardware (a robot, a standalone
      servo drive, an I/O module, etc.). The examples below use the Dobot CR3A
      manipulator, but the same procedure applies to any EtherCAT device.

      **Prerequisites**

      - The WMX ROS2 workspace is built and sourced
      - The WMX Runtime is installed at ``/opt/wmx3/``
      - EtherCAT cable is connected between compute platform and first EtherCAT device
      - The hardware and all servo drives are powered on
      - You have ``sudo`` privileges

      **EtherCAT Wiring**

      .. code-block:: text

         ┌──────────────┐    Ethernet     ┌──────────┐    ┌──────────┐         ┌──────────┐
         │  Compute PC  │────(EtherCAT)──►│ Servo J1 │───►│ Servo J2 │── ... ──│ Servo J6 │
         │  (dedicated  │                 └──────────┘    └──────────┘         └──────────┘
         │   NIC port)  │
         └──────────────┘

      - Use a **dedicated Ethernet port** for EtherCAT
      - Servo drives are daisy-chained (each drive has IN and OUT ports)
      - The I/O module for gripper control is part of the same chain

      **Setup WMX in real hardware mode**

      Modify ``/opt/wmx3/Module.ini`` to enable the EtherCAT platform and
      disable the simulation platform:

      .. code-block:: ini

         [Platform 0]
         Location = ./platform/ethercat
         DllName = ec_platform.so
         NumOfMaster = 1
         disable = 0

         [Platform 1]
         Location = ./platform/simu
         DllName = simu_platform.so
         NumOfMaster = 1
         disable = 1

Test the WMX ROS2 General Nodes (Standalone)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo --preserve-env=PATH \
     --preserve-env=AMENT_PREFIX_PATH \
     --preserve-env=COLCON_PREFIX_PATH \
     --preserve-env=PYTHONPATH \
     --preserve-env=LD_LIBRARY_PATH \
     --preserve-env=ROS_DISTRO \
     --preserve-env=ROS_VERSION \
     --preserve-env=ROS_PYTHON_VERSION \
     --preserve-env=ROS_DOMAIN_ID \
     --preserve-env=RMW_IMPLEMENTATION \
     bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && source $HOME/workspaces/movensys_ws/install/setup.bash && \
     ros2 launch wmx_ros2_package wmx_ros2_general_nodes.launch.py"

Startup Sequence
^^^^^^^^^^^^^^^^

When launched, four nodes initialize in parallel:

1. **Device creation** -- Each node creates a WMX device handle
2. **EtherCAT scan** -- Network scan discovers all servo drives
3. **Communication start** -- Real-time EtherCAT communication begins
4. **Parameter loading** -- Gear ratios and axis polarities loaded from XML
5. **Servo enable** -- All 6 joint servos cleared and enabled
6. **Ready** -- All nodes report ready

Testing WMX ROS2 Services and Topics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The general nodes expose the WMX engine, axis, I/O, and EtherCAT control
interfaces as ROS2 services and topics. List what is available and confirm the
engine is communicating:

.. code-block:: bash

   ros2 service list | grep /wmx                                  # Available WMX services
   ros2 topic list | grep /wmx                                    # Available WMX topics
   ros2 service call /wmx/engine/get_status std_srvs/srv/Trigger  # Expect: "Communicating"
   ros2 service call /wmx/ecat/get_network_state \
        wmx_ros2_message/srv/EcatGetNetworkState                  # EtherCAT master/slave status

For the complete list of services, topics, and message types exposed by the
general nodes — engine control, axis motion, I/O, and EtherCAT — see the
`WMX ROS2 General Nodes reference
<https://github.com/movensys/wmx-ros2/blob/main/doc/reference_wmx_ros2_general_nodes.md>`_.

Shutdown
^^^^^^^^

Press ``Ctrl+C`` in the launch terminal. The nodes will automatically disable
servos, stop EtherCAT communication, and close the WMX device.
