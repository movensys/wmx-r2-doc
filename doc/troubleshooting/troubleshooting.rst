Troubleshooting
===============

.. warning::

   Several symptoms below are caused by wrong robot parameters, and the fix is
   to correct the parameter — not to compensate for it elsewhere. Scaling a
   URDF to hide a wrong gear ratio, or flipping a sign in application code to
   hide a wrong polarity, leaves the robot able to move unexpectedly in every
   path that does not go through your workaround. See
   :doc:`../commissioning/robot_parameters`.

Robot Moves in the Wrong Direction
-----------------------------------

**Symptom:** A positive command moves the joint in the negative direction, or
RViz and the physical robot move opposite ways.

**Solutions:**

- Read back the polarity the engine actually holds:

  .. code-block:: bash

     ros2 service call /wmx/params/get wmx_r2_message/srv/GetWmxParams \
       "{index: [0,1,2,3,4,5]}"

- Correct ``AxisPolarity`` for that axis in the robot's WMX parameter XML
  (``+1`` or ``-1``) and rebuild, or override it for testing:

  .. code-block:: bash

     ros2 service call /wmx/axis/set_polarity wmx_r2_message/srv/SetAxis \
       "{index: [0], data: [-1]}"

- Confirm the URDF's sign convention for that joint (``<axis xyz>`` together
  with the joint ``<origin rpy>``) before deciding which sign is correct.
- Re-verify with the single-axis procedure in
  :doc:`../commissioning/first_motion`. A runtime polarity override is lost on
  the next engine restart — write the corrected value into the XML.

Robot Moves the Wrong Distance
-------------------------------

**Symptom:** A commanded 90° rotation produces a visibly different physical
rotation, or the robot moves by a large factor more or less than expected.

**Solutions:**

- Check ``AxisGearRatioNumerator`` and ``AxisGearRatioDenominator`` against the
  drive's encoder resolution and the joint's reducer ratio:
  ``numerator = encoder counts per motor revolution × gear ratio``.
- Confirm ``AxisGearRatioDenominator`` is 2π. Any other value changes the unit
  of every position, velocity, and acceleration in the ROS 2 interface.
- Verify against the running engine with ``/wmx/params/get``, not against the
  file — the engine may be holding values from a previous session, since the
  general nodes load no parameter file.
- Re-measure with a small commanded step and a physical reference; see
  :doc:`../commissioning/first_motion`.

Wrong Joint Moves
-----------------

**Symptom:** Commanding ``joint2`` moves a different physical joint.

**Solutions:**

- Compare ``joint_name`` and ``joint_axes`` in the robot's application YAML.
  They are matched by position: ``joint_name[i]`` is driven by
  ``joint_axes[i]``.
- Confirm the EtherCAT chain order, which is what assigns the axis indices:

  .. code-block:: bash

     ros2 service call /wmx/ecat/get_network_state \
       wmx_r2_message/srv/EcatGetNetworkState

- Re-cabling the drives in a different order shifts every axis index after the
  change, with no error anywhere in ROS 2.

All Joints Offset by a Constant
--------------------------------

**Symptom:** The robot's poses are consistently shifted from the URDF zero, in
the same direction, by roughly the same amount per joint.

**Solutions:**

- Check ``AbsoluteEncoderHomeOffset`` (and ``HomePosition``) for each axis. The
  shipped files use ``0.0``, which asserts that the drive's absolute zero is
  the URDF zero — a per-unit property, not a per-model one.
- Move each joint to a known mechanical reference and compare ``actual_pos``
  against the value the URDF zero implies.

Device Creation Failures
------------------------

**Symptom:** ``Failed to create device after N attempts``

**Solutions:**

- Verify the WMX Runtime is installed: ``ls /opt/wmx3/lib/libwmx3api.so``
- Ensure you are running with ``sudo``
- Check that no other WMX application is running (lock contention causes
  error code 297)
- If the error persists after stopping other applications, reboot to clear
  stale device locks

EtherCAT Scan Failures
-----------------------

**Symptom:** ``Failed to scan network``

**Solutions:**

- Verify the EtherCAT cable is connected to the correct dedicated Ethernet
  port
- Ensure all servo drives are powered on
- Check the ``eni/`` directory has the correct EtherCAT Network Information
  files for your servo drives
- Verify the EtherCAT Ethernet port does **not** have an IP address assigned

Communication Start Failures
-----------------------------

**Symptom:** ``Failed to start communication``

**Solutions:**

- Check that the EtherCAT network scan succeeded (look for earlier scan
  errors in the log)
- Verify servo drives are properly daisy-chained (IN port to OUT port)
- Remove any IP address from the EtherCAT network interface
- Check the WMX engine status:

  .. code-block:: bash

     ros2 service call /wmx/engine/get_status std_srvs/srv/Trigger

Joint States All Zero
---------------------

**Symptom:** ``/joint_states`` publishes but all position values are zero.

**Solutions:**

- Verify engine is in ``Communicating`` state (see above)
- Check that servo drives are enabled (no amplifier alarms):

  .. code-block:: bash

     ros2 topic echo /wmx/axis/state --field amp_alarm

- Verify ``wmx_param_file_path`` in the config YAML points to the correct
  WMX parameter XML file for your robot
- Clear alarms and re-enable servos:

  .. code-block:: bash

     ros2 service call /wmx/axis/clear_alarm wmx_r2_message/srv/SetAxis \
       "{index: [0,1,2,3,4,5], data: [0,0,0,0,0,0]}"

Servo Alarm Errors
------------------

**Symptom:** Servo drives report amplifier alarms; motion commands are
rejected.

**Solutions:**

- Clear alarms via the service:

  .. code-block:: bash

     ros2 service call /wmx/axis/clear_alarm wmx_r2_message/srv/SetAxis \
       "{index: [0,1,2,3,4,5], data: [0,0,0,0,0,0]}"

- Check for physical obstructions or overcurrent conditions on the robot
- Verify gear ratios and polarities match the physical servo configuration
  (see :doc:`../commissioning/robot_parameters`). A wrong polarity drives the
  joint away from its target, which shows up as a following error or an
  overcurrent alarm rather than as an obviously wrong direction.

Trajectory Execution Failures
------------------------------

**Symptom:** ``FollowJointTrajectory`` goal is aborted with a WMX error
code.

**Solutions:**

- Check that the trajectory has at most 1000 waypoints
- Verify all servos are enabled and in the correct mode
- Check the WMX error description in the action result ``error_string``


Gripper Not Responding
-----------------------

**Symptom:** Gripper open/close service calls succeed but the gripper
does not move.

**Solutions:**

- Verify the I/O module is part of the EtherCAT daisy chain
- Check EtherCAT communication is active (engine state = ``Communicating``)
- Test the I/O directly:

  .. code-block:: bash

     ros2 service call /wmx/set_gripper std_srvs/srv/SetBool "{data: true}"

Nodes Not Found
---------------

**Symptom:** ``ros2 pkg list | grep wmx`` returns nothing.

**Solutions:**

- Source the workspace: ``source ~/wmx_r2_ws/install/setup.bash``
- Rebuild if needed: ``cd ~/wmx_r2_ws && colcon build``
- Check the two-stage build was done correctly (message package first).
  See :doc:`../getting_started/index`.

Build Errors
------------

**Symptom:** Linker errors referencing ``coremotionapi``, ``wmx3api``, or
other WMX libraries.

**Solutions:**

- Verify the WMX Runtime and SDK are installed. The MIT-licensed ROS 2
  packages link against the proprietary WMX libraries and cannot be built
  without them (see :doc:`../licensing`): ``ls /opt/wmx3/lib/``
- Ensure ``LD_LIBRARY_PATH`` includes ``/opt/wmx3/lib/``:

  .. code-block:: bash

     export LD_LIBRARY_PATH=/opt/wmx3/lib:$LD_LIBRARY_PATH

- Install missing ROS2 dependencies:

  .. code-block:: bash

     cd ~/wmx_r2_ws
     rosdep install --from-paths src --ignore-src -y

Getting Help
------------

For additional support, contact your MOVENSYS representative or file an
issue on the project repository.
