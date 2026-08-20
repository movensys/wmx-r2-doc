Testing WMX R2
===============

Once WMX R2 is installed and built, you can validate it in two ways: in
simulation (no physical hardware required) or against real EtherCAT hardware.
Start with simulation to verify basic behavior, then move to real hardware.

1. Setup Operation Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The WMX R2 nodes communicate directly with the WMX engine over EtherCAT —
there is no built-in mock hardware mode. The mode is selected in
``/opt/wmx3/Module.ini`` by enabling either the simulation or the EtherCAT
platform. Select your mode below, then continue with the common test steps
that follow.


.. warning:: **Real Hardware mode moves a physical machine.**

   Start with the Simulation platform. Before switching to EtherCAT and
   enabling servos on a robot, complete :doc:`../commissioning/index` —
   parameter validation, the low-speed single-axis procedure, and the separate
   safety measures described in :doc:`../commissioning/safety`.


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

      - The WMX R2 workspace is built and sourced
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




2. Launch the General Nodes (Standalone)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Start the four robot-agnostic nodes (``wmx_engine_node``, ``wmx_core_motion_node``, ``wmx_io_node``, and ``wmx_ethercat_node``).

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
     ros2 launch wmx_r2_package wmx_r2_general_nodes.launch.py"


.. note::

   1. **Device creation** -- ``wmx_engine_node`` creates the WMX device handle,
   retrying up to five times if another application holds the lock
   (error 297). The remaining nodes then attach to that device.
   
   2. **Communication start** -- ``StartCommunication`` brings up the real-time
   EtherCAT cycle, which discovers the drives on the bus.
   
   3. **Ready** -- each node publishes on its ``ready`` topic and begins serving
   its services and topics.



3. Test Services and Topics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The general nodes expose the WMX engine, axis, I/O, and EtherCAT control
interfaces as ROS2 services and topics. List what is available and confirm the
engine is communicating:

.. code-block:: bash

   ros2 service list | grep /wmx                                  # Available WMX services
   ros2 topic list | grep /wmx                                    # Available WMX topics
   ros2 service call /wmx/engine/get_status std_srvs/srv/Trigger  # Expect: "Communicating"
   ros2 service call /wmx/ecat/get_network_state \
        wmx_r2_message/srv/EcatGetNetworkState                  # EtherCAT master/slave status

For the complete list of services, topics, and message types exposed by the
general nodes — engine control, axis motion, I/O, and EtherCAT — see the
`WMX R2 General Nodes reference
<https://github.com/movensys/wmx-r2/blob/main/doc/reference_wmx_r2_general_nodes.md>`_.



.. warning:: **The general nodes load no robot parameters and enable no
   servos.**

   These four nodes are robot-agnostic by design. They do **not** apply a
   ``<robot>_wmx_parameters.xml`` file, so the gear ratios, polarities,
   command modes, and limits in the engine are whatever was left there by a
   previous session — not your robot's values. They also do not enable the
   servos; that is an explicit ``/wmx/axis/set_on`` call.

   Robot parameters are applied by the per-robot launches
   (``wmx_r2_<robot>_manipulator.launch.py`` and
   ``wmx_r2_diffbot_navigation.launch.py``), which pass
   ``wmx_param_file_path`` to their controllers, or by the ``ros2_control``
   hardware plugin. If you command motion from the general nodes alone, load
   the parameters first:

   .. code-block:: bash

      ros2 service call /wmx/params/load wmx_r2_message/srv/LoadWmxParams \
           "{file_path: '/abs/path/to/<robot>_wmx_parameters.xml'}"
      ros2 service call /wmx/params/get wmx_r2_message/srv/GetWmxParams \
           "{index: [0,1,2,3,4,5]}"

   See :doc:`../commissioning/robot_parameters`.



4. Shutdown
^^^^^^^^^^^^^^^^

Press ``Ctrl+C`` in the launch terminal. The nodes will automatically disable
servos, stop EtherCAT communication, and close the WMX device.
