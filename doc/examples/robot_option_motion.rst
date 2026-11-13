Robot Option Motion
===================

Move the arm with the WMX3 Robot Option instead of MoveIt2. The kinematics
run inside the WMX engine: ``wmx_robot_option_node`` takes a joint target or
a tool pose in millimetres and degrees, and the engine plans and executes a
point-to-point (PTP) or straight-line move. No planner container is needed.

The scene setup is the same as in :doc:`trajectory_planning`. Only the WMX R2
launch changes, and the motion commands are ``/wmx/robot/*`` service calls run
through ``wros``. For every service and field, see
:doc:`../api_reference/wmx_robot_option`.

.. important::

   - The Robot Option runs **free in renewable 6-hour sessions**, the same as
     the WMX engine. When a session ends, restart the engine to start a new
     one. A commercial license removes the time limit; see
     :doc:`../licensing`.
   - The package ships a robot option configuration for the **Dobot CR3A**
     only. Run this example with ``MANIPULATOR_MODEL=dobot_cr3a``.
   - The robot option stack needs **degree-scaled axes**, so it loads
     ``cr3a_wmx_parameters_deg.xml``, not the radian file the MoveIt2 stack
     uses. ``/joint_states`` and the simulator topics are still published in
     radians. See :ref:`other-axis-units`.
   - There is no Simulation tab. The Robot Option runs inside the WMX engine,
     so it needs HIL or Real.

.. tab-set::

   .. tab-item:: HIL

      1. Open the scene:

         .. tab-set::

            .. tab-item:: Isaac Sim
               :sync: isaacsim

               Open
               ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/3b_trajectory_hil.usd``

            .. tab-item:: Gazebo
               :sync: gazebo

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_description gazebo_trajectory_hil.launch.py

      2. Start WMX R2 with the robot option (real WMX runtime, simulation
         platform) and ``use_sim_time:=true``:

         .. code-block:: bash

            wros ros2 launch wmx_r2_package wmx_r2_robot_option.launch.py \
                use_sim_time:=true \
                'config_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_config.yaml' \
                'wmx_param_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_wmx_parameters_deg.xml' \
                'robot_param_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_parameters.xml'

         Wait until the lifecycle manager reports ``wmx_robot_option_node``
         as ``active``. The node registers the CR3A from
         ``robot_param_file`` at ``configure``, and
         ``joint_state_broadcaster`` switches the servos on.

      3. Command the robot option. See :ref:`robot-option-commands` below.

   .. tab-item:: Real

      1. (optional) Open the matching scene for visualization:

         .. tab-set::

            .. tab-item:: Isaac Sim
               :sync: isaacsim

               Open
               ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/3c_trajectory_real.usd``

            .. tab-item:: Gazebo
               :sync: gazebo

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_description gazebo_trajectory_real.launch.py

      2. Start WMX R2 with the robot option on the robot (EtherCAT platform):

         .. code-block:: bash

            wros ros2 launch wmx_r2_package wmx_r2_robot_option.launch.py \
                use_sim_time:=false \
                'config_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_config.yaml' \
                'wmx_param_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_wmx_parameters_deg.xml' \
                'robot_param_file:=$(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_parameters.xml'

         .. warning::

            The servos switch on as soon as the node graph comes up. Before the
            first move, complete :doc:`../try_your_robot/first_motion` with
            this degree-scaled parameter file, keep a hardware emergency stop
            within reach (:doc:`../try_your_robot/safety`), and run the HIL tab
            first. ``/wmx/robot/e_stop`` is a software stop, not a safety
            function.

      3. Command the robot option. See :ref:`robot-option-commands` below.

.. _robot-option-commands:

Step 3 — Robot option commands
------------------------------

The same commands serve HIL and Real. Run them from a second terminal. The
joint values and poses are for the CR3A and sit inside the limits of
``cr3a_robot_option_parameters.xml``. Joint values are degrees; poses are
``x``, ``y``, ``z`` in mm and ``u``, ``v``, ``w`` in degrees.

.. note::

   The payloads are written ``'"{...}"'`` because ``wros`` hands the whole
   command to the container's shell as one string. Inside the container,
   use plain ``"{...}"``.

a. **Check the node and watch the status.** Keep the status echo open in its
   own terminal. ``motion_state`` ``0`` is idle, ``7`` is a PTP move in
   progress and ``6`` a straight-line move. Any non-zero
   ``motion_error_code`` is an error.

   .. code-block:: bash

      wros ros2 lifecycle get /wmx_robot_option_node
      wros ros2 service list | grep /wmx/robot/
      wros ros2 topic echo /wmx/robot/status

   If the robot was not registered at launch, register it by hand:

   .. code-block:: bash

      wros ros2 service call /wmx/robot/set_robot_param wmx_r2_message/srv/RobotSetRobotParam \
        '"{param_file: $(ros2 pkg prefix --share wmx_r2_package)/example/cr3a_robot_option_parameters.xml, robot_id: 0}"'

   The single quotes keep ``$(...)`` from expanding on the host, so the
   container resolves it to the absolute path the SDK needs.

b. **Slow the motion down** for the first moves. The override scales the
   profile in the robot parameter file; ``0.5`` is half speed:

   .. code-block:: bash

      wros ros2 service call /wmx/robot/override_velocity_by_ratio \
        wmx_r2_message/srv/RobotOverrideVelocityByRatio \
        '"{robot_id: 0, vel_ratio: 0.5, acc_ratio: 0.5, dec_ratio: 0.5}"'

c. **PTP to a joint target.** No inverse kinematics is involved, so this
   is the safe first move. It also parks the arm in a good starting
   configuration for the pose moves that follow:

   .. code-block:: bash

      wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
        '"{robot_id: 0, mode: 0, target_type: 0, path: 0,
          target_joint: [0.0, 0.0, -90.0, 0.0, 90.0, 0.0]}"'

   Relative joint move, 15° on J3:

   .. code-block:: bash

      wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
        '"{robot_id: 0, mode: 1, target_type: 0, path: 0,
          target_joint: [0.0, 0.0, 15.0, 0.0, 0.0, 0.0]}"'

d. **PTP to a tool pose.** The engine solves the inverse kinematics; the
   tool's path between the endpoints is a curve:

   .. code-block:: bash

      wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
        '"{robot_id: 0, mode: 0, target_type: 1, path: 0,
          target_pose: {x: 345.0, y: -70.0, z: 163.0, u: 180.0, v: 0.0, w: -90.0},
          s: 0, e: 0, r: 0}"'

e. **Straight-line moves.** ``path: 1`` keeps the tool on a straight line.
   An absolute target, then a 50 mm shift along the work-frame y axis, then
   a 50 mm retract along the tool's own z axis:

   .. code-block:: bash

      wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
        '"{robot_id: 0, mode: 0, target_type: 1, path: 1,
          target_pose: {x: 345.0, y: -128.0, z: 163.0, u: 180.0, v: 0.0, w: -90.0}}"'

      wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
        '"{robot_id: 0, mode: 1, frame: 0, target_type: 1, path: 1,
          target_pose: {x: 0.0, y: 50.0, z: 0.0, u: 0.0, v: 0.0, w: 0.0}}"'

      wros ros2 service call /wmx/robot/start_motion wmx_r2_message/srv/RobotStartMotion \
        '"{robot_id: 0, mode: 1, frame: 1, target_type: 1, path: 1,
          target_pose: {x: 0.0, y: 0.0, z: -50.0, u: 0.0, v: 0.0, w: 0.0}}"'

   Wait for ``motion_state`` to return to ``0`` before sending the next move.
   The services return as soon as the engine accepts a command.

f. **Stop and recover.**

   .. code-block:: bash

      # controlled stop of the running move
      wros ros2 service call /wmx/robot/stop_motion wmx_r2_message/srv/RobotId '"{robot_id: 0}"'

      # software EStop, then release it
      wros ros2 service call /wmx/robot/e_stop wmx_r2_message/srv/RobotId '"{robot_id: 0}"'
      wros ros2 service call /wmx/robot/release_e_stop wmx_r2_message/srv/RobotId '"{robot_id: 0}"'

      # clear any other motion error
      wros ros2 service call /wmx/robot/clear_motion_error wmx_r2_message/srv/RobotId '"{robot_id: 0}"'

.. tip:: **A pose move fails with** ``Error=163857``.

   The inverse-kinematics solver did not converge. That does not always mean
   the point is out of reach. Run the joint move in step c to re-seed it, then
   send the pose again. On the CR3A, table poses sit near ``w: -90``, and
   raising ``z`` close to the base leaves the workspace before moving outward
   does. See :doc:`../api_reference/wmx_robot_option`.

.. note::

   While ``wmx_robot_option_node`` is active it owns the axes:
   ``/wmx/axes/start_pos``, ``start_mov``, ``start_vel``, ``start_jog`` and
   ``start_home`` answer ``success: false``. ``/wmx/axes/stop`` and the servo
   services stay available. To go back to MoveIt2, stop this launch and start
   the manipulator launch from :doc:`trajectory_planning` with the radian
   parameter file.
