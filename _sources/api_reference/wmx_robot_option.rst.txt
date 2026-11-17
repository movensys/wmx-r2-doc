wmx_robot_option_node
=====================

Overview
--------

``wmx_robot_option_node`` (``wmx_r2_package/src/wmx_robot_option_node.cpp``)
is a lifecycle node that exposes the **WMX3 Robot Option**: the
kinematics and robot-motion layer (``KinematicsApi``, ``RobotMotionApi``,
``CoordinateApi``) that sits above CoreMotion.

Where ``wmx_core_motion_node`` commands axes one by one, this node commands
the robot as a whole. The WMX3 kinematics engine turns a joint target or a
tool pose into coordinated axis motion, as a point-to-point (PTP) move or a
straight-line tool path. Both nodes drive the same axes, so only one of them
may drive at a time; see `Arbitration`_.

.. mermaid::
   :caption: wmx_robot_option_node

   flowchart LR
       SRP["set_robot_param<br/><i>XML / URDF</i>"] --> RON
       SM["start_motion<br/><i>ptp / line</i>"] --> RON
       STOP["stop_motion<br/>e_stop / release_e_stop"] --> RON
       TC["set / get_tool_coordinate"] --> RON
       RON["wmx_robot_option_node<br/><i>lifecycle, one robot, tool 0</i>"]
       RON -->|SetRobotParam| KIN["WMX3 Kinematics"]
       RON -->|StartPTPPos / StartMotion| KIN
       RON -->|UpdateRobotStatus @ rate| ST["/wmx/robot/status"]

.. important::

   The Robot Option runs **free in renewable 6-hour sessions**, the same as
   the WMX engine: restarting the engine starts a new session, and a
   commercial license removes the time limit. See :doc:`../licensing`.

   This node speaks WMX3 poses over services. It does **not** serve
   ``FollowJointTrajectory`` and is not a MoveIt2 backend; for MoveIt2 use
   ``wmx_r2_manipulator.launch.py``. See :doc:`wmx_r2_package`.

Launch
------

``wmx_r2_robot_option.launch.py`` starts the general nodes plus
``joint_state_broadcaster`` and ``wmx_robot_option_node``. The broadcaster
is required: it clears the amp alarms and switches the servos on at
activation, and it publishes ``/joint_states``. The robot option node does
neither.

.. code-block:: bash

   wros ros2 launch wmx_r2_package wmx_r2_robot_option.launch.py \
       use_sim_time:=false \
       'config_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_config.yaml' \
       'wmx_param_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_wmx_parameters_deg.xml' \
       'robot_param_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_parameters.xml'

.. list-table::
   :header-rows: 1
   :widths: 22 22 56

   * - Argument
     - Default
     - Description
   * - ``use_sim_time``
     - ``false``
     - Use the simulation clock
   * - ``config_file``
     - ``config/wmx_r2_robot_option_config.yaml``
     - YAML with the general-node, broadcaster and robot option parameters.
       That default file is not shipped, so always pass one — for example
       ``example/cr3a_robot_option_config.yaml``.
   * - ``wmx_param_file``
     - ``""``
     - WMX3 **axis** parameter XML imported at engine start
   * - ``robot_param_file``
     - ``""``
     - **Robot** parameter XML or URDF registered at ``configure``. Overrides
       the YAML value; empty leaves the node waiting for
       ``/wmx/robot/set_robot_param``

.. warning:: **The axes must be scaled in degree/mm.**

   The WMX3 SDK states it in ``RobotMotionParam``: *"WMX User unit must be
   degree / mm unit."* The robot module does no unit conversion; the joint
   values it computes go to the axes as user units. On a radian-scaled axis
   every move is 57.3 times too large, and the joint limits, being degree
   figures, never catch it.

   Use ``cr3a_wmx_parameters_deg.xml`` (``AxisGearRatioDenominator`` 360),
   **not** ``cr3a_wmx_parameters.xml`` (2π), which is for the MoveIt2 stack.
   ``cr3a_robot_option_config.yaml`` then sets
   ``degree_to_radian_axes: [0, 1, 2, 3, 4, 5]`` on
   ``joint_state_broadcaster`` so ``/joint_states``, Isaac Sim and Gazebo
   still receive radians. See :ref:`other-axis-units`.

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 24 12 64

   * - Parameter
     - Default
     - Meaning
   * - ``robot_param_file``
     - ``""``
     - Absolute path to the robot parameter file, read once at
       ``on_configure``. A ``.urdf`` suffix (any case) selects
       ``ImportParamURDF``, anything else ``ImportParamXML``. Empty logs a
       warning and configures anyway.
   * - ``robot_status_rate``
     - ``10``
     - ``/wmx/robot/status`` rate in Hz. Values ``<= 0`` fall back to 10.
       The CR3A example sets ``1``.

An XML file takes its robot id from its own ``<Robot ID="...">``. A URDF has
no id, so one registered at configure gets id ``0``; register a URDF under
another id at runtime through the ``robot_id`` field of
``set_robot_param``. Parameters are read once in the constructor; set them in
the YAML.

Services
--------

Every service answers ``success`` plus a ``message`` carrying the WMX3 call
name, error number and error text. Every one takes ``robot_id``, and every
one except ``set_robot_param`` rejects an id that is not the registered one.

.. note::

   The payloads below are written ``'"{...}"'`` because ``wros`` hands the
   whole command to the container's shell as one string. From a shell
   already inside the container, plain ``"{...}"`` is correct.

.. list-table::
   :header-rows: 1
   :widths: 38 30 32

   * - Service
     - Type
     - WMX3 call
   * - ``/wmx/robot/set_robot_param``
     - ``RobotSetRobotParam``
     - ``ImportParamXML`` / ``ImportParamURDF``, then ``SetRobotParam``
   * - ``/wmx/robot/release_robot``
     - ``RobotId``
     - ``ReleaseRobot``
   * - ``/wmx/robot/start_motion``
     - ``RobotStartMotion``
     - ``StartPTPPos``, ``StartToolPTPMov``, or ``SetMotion`` +
       ``StartMotion``
   * - ``/wmx/robot/stop_motion``
     - ``RobotId``
     - ``StopMotion``
   * - ``/wmx/robot/clear_motion_error``
     - ``RobotId``
     - ``ClearMotionError``
   * - ``/wmx/robot/e_stop``
     - ``RobotId``
     - ``EStop``
   * - ``/wmx/robot/release_e_stop``
     - ``RobotId``
     - ``ReleaseEStop``
   * - ``/wmx/robot/override_velocity_by_ratio``
     - ``RobotOverrideVelocityByRatio``
     - ``OverrideVelocityByRatio``
   * - ``/wmx/robot/set_tool_coordinate``
     - ``RobotSetCoordinate``
     - ``SetToolCoordinate``
   * - ``/wmx/robot/get_tool_coordinate``
     - ``RobotGetCoordinate``
     - ``GetToolCoordinate``

There is no servo service here. Servo state belongs to
``wmx_core_motion_node``, and ``/wmx/axes/set_servo_on`` stays reachable
while the robot option holds the axes. The axis list is the ``<Axis>``
values of the robot parameter file — ``0`` to ``5`` for the CR3A example.

Registration
^^^^^^^^^^^^

.. code-block:: bash

   wros ros2 service call /wmx/robot/set_robot_param wmx_r2_message/srv/RobotSetRobotParam \
     '"{param_file: /opt/wmx3/robot_sample/common/robotParamXML_MZ07L.xml, robot_id: 0}"'
   wros ros2 service call /wmx/robot/release_robot wmx_r2_message/srv/RobotId '"{robot_id: 0}"'

``set_robot_param`` replaces whatever was registered before, so it also
re-registers after ``release_robot`` and re-reads a file edited at runtime.
The response returns the ``robot_id`` and ``num_joints`` the engine
accepted; every later call must match them. After ``release_robot`` the
status topic goes quiet until a robot is registered again.

start_motion
^^^^^^^^^^^^

``start_motion`` is the one motion entry point. ``mode`` selects absolute
(``0`` pos) or relative (``1`` mov), ``frame`` what a relative pose is
measured against (``0`` base/work, ``1`` tool), ``target_type`` the target
(``0`` joint values, ``1`` tool pose), and ``path`` the interpolation
(``0`` PTP, ``1`` straight line). Eight combinations are valid:

.. list-table::
   :header-rows: 1
   :widths: 6 12 14 10 10 48

   * - #
     - ``path``
     - ``target_type``
     - ``mode``
     - ``frame``
     - What runs
   * - 1
     - ptp
     - joint
     - pos
     - —
     - Absolute joint values, joint interpolated
   * - 2
     - ptp
     - joint
     - mov
     - —
     - Per-joint distance, joint interpolated
   * - 3
     - ptp
     - pose
     - pos
     - —
     - Absolute tool pose, joint interpolated
   * - 4
     - ptp
     - pose
     - mov
     - base
     - Work-frame displacement, joint interpolated
   * - 5
     - ptp
     - pose
     - mov
     - tool
     - Tool-frame displacement, joint interpolated
   * - 6
     - line
     - pose
     - pos
     - —
     - Absolute tool pose, straight tool path
   * - 7
     - line
     - pose
     - mov
     - base
     - Work-frame displacement, straight tool path
   * - 8
     - line
     - pose
     - mov
     - tool
     - Tool-frame displacement, straight tool path

``path: 1`` with ``target_type: 0`` is rejected: a joint target has no
straight line to follow. ``frame`` is read only by rows 4, 5, 7 and 8. A PTP
move synchronizes the joints only at the endpoints, so the tool traces a
curve; only ``path: 1`` controls the shape of the tool path.

Row 7 is computed by the node, not by a single SDK call: it adds the
displacement to the currently **commanded** tool pose (``tool_pose_cmd``)
and sends the result as an absolute line. Measuring from the command rather
than the feedback keeps chained relative moves from drifting by the
following error. Rotations compose rather than add (``u``, ``v``, ``w`` are
Z-Y-X Euler angles); with all three zero the orientation is kept.

The joint values below are for the CR3A and sit inside the limits of
``cr3a_robot_option_parameters.xml``:

.. code-block:: bash

   # 1  ptp / joint / pos — absolute joint target (deg)
   wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
     '"{robot_id: 0, mode: 0, target_type: 0, path: 0,
       target_joint: [0.0, 0.0, -90.0, 0.0, 90.0, 0.0]}"'

   # 2  ptp / joint / mov — relative joint target
   wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
     '"{robot_id: 0, mode: 1, target_type: 0, path: 0,
       target_joint: [0.0, 0.0, 15.0, 0.0, 0.0, 0.0]}"'

   # 3  ptp / pose / pos — absolute tool pose (mm, deg)
   wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
     '"{robot_id: 0, mode: 0, target_type: 1, path: 0,
       target_pose: {x: 345.0, y: -70, z: 163.0, u: 180.0, v: 0.0, w: -90.0},
       s: 0, e: 0, r: 0}"'

   # 5  ptp / pose / mov / tool — retract 50 mm along the tool z axis
   wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
     '"{robot_id: 0, mode: 1, frame: 1, target_type: 1, path: 0,
       target_pose: {x: 0.0, y: 0.0, z: -50.0, u: 0.0, v: 0.0, w: 0.0},
       s: 0, e: 0, r: 0}"'

   # 6  line / pose / pos — straight line to an absolute tool pose
   wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
     '"{robot_id: 0, mode: 0, target_type: 1, path: 1,
       target_pose: {x: 345.0, y: -128, z: 163.0, u: 180.0, v: 0.0, w: -90.0}}"'

   # 7  line / pose / mov / base — shift 50 mm along work-frame y
   wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
     '"{robot_id: 0, mode: 1, frame: 0, target_type: 1, path: 1,
       target_pose: {x: 0.0, y: 50.0, z: 0.0, u: 0.0, v: 0.0, w: 0.0}}"'

   # stop the running move
   wros ros2 service call /wmx/robot/stop_motion wmx_r2_message/srv/RobotId '"{robot_id: 0}"'

``s``, ``e`` and ``r`` are the inverse-kinematics configuration flags —
shoulder (``1`` left, ``-1`` right), elbow (``1`` above, ``-1`` below) and
wrist (``1`` flip, ``-1`` no flip), ``0`` for automatic. Only the PTP pose
rows 3, 4 and 5 read them; line moves keep the configuration that holds the
tool on the line, and joint targets already fix it.

.. tip:: **When inverse kinematics fails.**

   ``Error=163857 (Inverse kinematic computation iteration exceeded the
   limit)`` means the solver did not converge, which is not the same as the
   point being out of reach. The solver seeds from the **current** joint
   position, so first park the arm with a joint target (rows 1 or 2, no IK
   involved) — ``[0, 0, -90, 0, 90, 0]`` is a good seed on the CR3A — then
   re-issue the pose.

   On the CR3A cell, working poses on the table sit near ``w: -90`` because
   the arm is mounted yawed -90° relative to the table. J2 is capped at
   63°, so raising ``z`` with a small ``x`` leaves the workspace first: at
   ``u: 180, v: 0``, ``(400, 0, 300)`` is reachable and ``(200, 0, 400)``
   is not. Move outward as you go up.

Stopping and speed
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Service
     - Effect
   * - ``stop_motion``
     - Decelerates to a controlled halt short of the target. There is no
       pause or resume; re-issue the move with ``start_motion``.
   * - ``e_stop``
     - Level 1 emergency stop in the kinematics engine: motion ends
       immediately, ``motion_state`` becomes EStop active and
       ``motion_error_code`` user EStop. Only ``release_e_stop`` recovers.
       This is a software stop, not a safety function — see
       :doc:`../try_your_robot/safety`.
   * - ``clear_motion_error``
     - Clears other motion errors. Does **not** recover a user EStop.
   * - ``override_velocity_by_ratio``
     - Scales the **current** motion's velocity, acceleration and
       deceleration. ``1.0`` is 100 %; values above ``1.0`` exceed the
       profile in the robot parameter file.

.. code-block:: bash

   wros ros2 service call /wmx/robot/override_velocity_by_ratio \
     wmx_r2_message/srv/RobotOverrideVelocityByRatio \
     '"{robot_id: 0, vel_ratio: 0.5, acc_ratio: 1.0, dec_ratio: 1.0}"'

There is no per-call velocity. The profile comes from the robot parameter
file — tool linear velocity and acceleration, per-joint velocity and
acceleration, the override gains, and the profile type. Change speed by
editing the file and re-registering, or at runtime with
``override_velocity_by_ratio``.

Tool coordinate
^^^^^^^^^^^^^^^

.. code-block:: bash

   # 100 mm tool offset along the flange z axis
   wros ros2 service call /wmx/robot/set_tool_coordinate wmx_r2_message/srv/RobotSetCoordinate \
     '"{robot_id: 0, pose: {x: 0.0, y: 0.0, z: 100.0}}"'
   wros ros2 service call /wmx/robot/get_tool_coordinate wmx_r2_message/srv/RobotGetCoordinate '"{robot_id: 0}"'

The work frame is set only by ``<WorkCoordinate>`` in the robot parameter
file; no service changes it at runtime.

Status topic
------------

.. list-table::
   :header-rows: 1
   :widths: 26 22 18 34

   * - Topic
     - Type
     - QoS
     - Rate
   * - ``/wmx/robot/status``
     - ``RobotStatus``
     - default, depth 1
     - ``robot_status_rate``

.. code-block:: bash

   wros ros2 topic echo /wmx/robot/status

Each tick carries ``robot_id``, ``motion_state``, ``motion_error_code``,
``motion_error_joint``, the commanded and feedback tool poses, and joint
position, velocity and torque arrays sized to ``num_joints``. Nothing is
published while no robot is registered.

Motion services **do not block**: they return as soon as the engine accepts
the command. Read completion from ``motion_state``, and raise
``robot_status_rate`` if the poll is too coarse.

.. list-table:: ``motion_state``
   :header-rows: 1
   :widths: 25 25 25 25

   * - 0–4
     - 5–9
     - 10–14
     - 15–18
   * - ``0`` idle
     - ``5`` setup
     - ``10`` error
     - ``15`` in resume
   * - ``1`` no new command
     - ``6`` in CP motion
     - ``11`` pausing CP
     - ``16`` direct teaching
   * - ``2`` stopping CP
     - ``7`` in PTP motion
     - ``12`` pausing PTP
     - ``17`` EStop stopping
   * - ``3`` stopping PTP
     - ``8`` error stopping CP
     - ``13`` paused CP
     - ``18`` EStop active
   * - ``4`` EStop (deprecated)
     - ``9`` error stopping PTP
     - ``14`` paused PTP
     -

.. list-table:: ``motion_error_code``
   :header-rows: 1
   :widths: 33 33 34

   * - 0–5
     - 6–11
     - 12–16
   * - ``0`` none
     - ``6`` axis vel limit
     - ``12`` axis following error
   * - ``1`` system EStop
     - ``7`` axis acc limit
     - ``13`` axis offline
   * - ``2`` trajectory calc error
     - ``8`` axis amp error
     - ``14`` axis interrupt mismatch
   * - ``3`` inverse kinematics error
     - ``9`` tool range error
     - ``15`` collision EStop
   * - ``4`` inverse dynamics error
     - ``10`` servo off
     - ``16`` axis command mode mismatch
   * - ``5`` axis pos limit
     - ``11`` user EStop
     -

Units and conventions
---------------------

- **Poses are millimetres and degrees.** ``RobotCartesianPose`` maps one to
  one onto the WMX3 ``CartesianPose``: ``x``, ``y``, ``z`` in mm and ``u``,
  ``v``, ``w`` as Z-Y-X Euler angles (roll, pitch, yaw) in degrees. This is
  the WMX3 convention, not the ROS one; nothing here is a
  ``geometry_msgs/Pose``.
- **Joint values are axis user units** — degrees for revolute joints, mm for
  prismatic ones.
- **Joint arrays must be exactly** ``num_joints`` **long**; anything else is
  rejected before the SDK is called.
- **Poses are in the work frame**, with the tool offset from
  ``set_tool_coordinate`` applied. ``tool_pose_cmd`` and ``tool_pose_fb``
  use the same frames.

Robot parameter file
--------------------

``robot_param_file`` is not the WMX axis parameter XML. The two describe
different things and are read by different nodes:

.. list-table::
   :header-rows: 1
   :widths: 18 41 41

   * -
     - ``wmx_param_file``
     - ``robot_param_file``
   * - Describes
     - Axes: gear ratio, units, polarity, encoder, limits
     - Robot: model, joint geometry, limits, motion profile
   * - Read by
     - ``wmx_engine_node`` at engine start
     - ``wmx_robot_option_node`` at configure
   * - Shipped
     - ``example/cr3a_wmx_parameters_deg.xml``
     - ``example/cr3a_robot_option_parameters.xml``
   * - SDK samples
     - ``/opt/wmx3/robot_sample/common/wmx_parameter_*.xml``
     - ``/opt/wmx3/robot_sample/common/robotParamXML_*.xml``

.. code-block:: xml

   <Robot ID="0">
     <RobotName>CR3A</RobotName>
     <RobotType>0</RobotType>
     <Joint ID="0">
       <JointType>RotateZAxis</JointType>
       <Axis>0</Axis>
       <JointOrigin x="0.0" y="0.0" z="128.3" u="0.0" v="0.0" w="0.0"/>
       <MaxAngle>3.0</MaxAngle>
       <MinAngle>-3.0</MinAngle>
       <VelocityLimit>3.0</VelocityLimit>
       <AccelerationLimit>12.0</AccelerationLimit>
     </Joint>
     ...
     <WorkCoordinate x="0.0" y="0.0" z="0.0" u="0.0" v="0.0" w="0.0"/>
     <ToolCoordinate x="0.0" y="0.0" z="134.0" u="0.0" v="0.0" w="0.0"/>
     <ToolVelocity>140.0</ToolVelocity>
     ...
   </Robot>

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Tag
     - Meaning
   * - ``Robot ID``
     - The id every service must pass
   * - ``RobotType``
     - Kinematic model: ``0`` articulated 6-axis (joint-origin form), ``1``
       SCARA, ``2`` cartesian, ``3`` delta, ``4`` H-bot, ``5`` / ``6``
       DH-based 6-axis, ``7`` / ``8`` dual-tool SCARA, ``9`` user defined
   * - ``Joint/Axis``
     - **WMX3 axis index**, and the axis list for ``set_servo_on``
   * - ``Joint/JointOrigin``
     - Offset from the previous joint
   * - ``Joint/MaxAngle``, ``MinAngle``, ``VelocityLimit``,
       ``AccelerationLimit``
     - Hard joint limits
   * - ``ToolCoordinate``
     - Default tool coordinate (the CR3A example: 134 mm along the flange
       z axis); ``set_tool_coordinate`` overrides it at runtime
   * - ``WorkCoordinate``
     - The work frame — the only way to set it
   * - ``Tool*``, ``Axis*``, ``*Override``, ``ProfileType``
     - The motion profile every move uses

.. important::

   **Angles are radians in the file and degrees in the API.** ``MaxAngle``
   ``2.9670597`` reads back as ``170.0``. Joint values on ``start_motion``
   and the status topic are degrees.

   A ``robot.xml`` written for the previous WMX kinematics SDK looks similar
   but is a **different schema**. ``ImportParamXML`` returns success and
   silently produces an unusable robot — every joint with ``axis = -1`` and
   zero origins. ``MotorID`` became ``Axis``, ``VecFrom`` became
   ``JointOrigin``, and ``RobotType`` uses a different enum.

The CR3A example takes its joint origins and limits from the CR3A
description in ``movensys-manipulator``, ``VelocityLimit`` 3.0 rad/s from the
same description, and ``AccelerationLimit`` 12 rad/s² as a derived figure
(Dobot publishes none). The commanded profile is a bring-up derate:
30 °/s and 60 °/s² per joint, 140 mm/s and 280 mm/s² at the tool, with 10 %
velocity and acceleration overrides. The joint limits are tighter than the arm's
mechanical range (J3 −146° to 11.5°, J5 −5.7° to 171.9°), so the engine
refuses some poses the arm could physically reach. Confirm both the
acceleration figure and the limits against your cell before production use.

Lifecycle and arbitration
-------------------------

The node is brought up by ``wmx_lifecycle_manager_node`` once the engine is
communicating, like every other managed node.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Transition
     - Effect
   * - ``configure``
     - Attaches to the WMX3 device as ``wmx_robot_option_node``. If
       ``robot_param_file`` is set, imports it and calls ``SetRobotParam``;
       a failure closes the device and fails the transition, so a bad path
       is caught at bring-up.
   * - ``activate``
     - Advertises the ten services, the status publisher and timer
   * - ``deactivate``
     - Removes them; the device stays attached and the robot registered
   * - ``cleanup``
     - Closes the device and unregisters the robot

.. _Arbitration:

**Arbitration.** The robot option stack lists ``wmx_robot_option_node`` in
the ``motion_controllers`` of ``wmx_core_motion_node``. While it is
``active``, ``/wmx/axes/start_pos``, ``start_mov``, ``start_vel``,
``start_jog`` and ``start_home`` answer ``success: false``.
``/wmx/axes/stop``, the servo services and ``clear_amp_alarm`` stay open.
Deactivating the node hands the axes back:

.. code-block:: bash

   wros ros2 lifecycle set /wmx_robot_option_node deactivate

The guard is one-way: nothing blocks ``/wmx/robot/start_motion`` while a
manipulator controller is active. Do not run the robot option and the
MoveIt2 controllers against the same axes at the same time.

Known limitations
-----------------

- **One robot per node.** A second ``robot_id`` is rejected; run one node
  per robot.
- **Tool index 0 only.** Dual-tool models are not reachable.
- **Up to six joints**, the SDK's ``MAX_NUMBER_OF_JOINT``.
- **No blocking wait.** Poll ``motion_state`` on the status topic.
- **The session time is not reported.** The node does not expose how much
  of the 6-hour evaluation session is left. When a session ends, restart the
  engine.
- **Not exposed:** input shaping, gravity compensation and direct teaching,
  collision detection, and streamed pose buffers.

Interface types
---------------

All types live in ``wmx_r2_message``; see :doc:`wmx_r2_message`. ``RobotId``
is shared by five services, so six service types cover ten services.

.. code-block:: bash

   wros ros2 service list -t | grep /wmx/robot/
   wros ros2 interface show wmx_r2_message/srv/RobotStartMotion
   wros ros2 lifecycle get /wmx_robot_option_node

See also
--------

- :doc:`../examples/robot_option_motion` -- HIL and Real walkthrough
- :doc:`wmx_r2_package` -- launch files and example configurations
- :doc:`wmx_r2_message` -- ``RobotStatus``, ``RobotCartesianPose`` and the
  robot services
- :doc:`../try_your_robot/robot_parameters` -- axis units and the
  degree-scaled parameter file
- :doc:`wmx3_api` -- the WMX3 SDK reference, including the Robot Option
