AprilTag Pick-and-Place
=======================

Detect an AprilTag-marked object and pick and place it. Detection uses either
OpenCV AprilTag (with MoveIt2 OMPL) or Isaac ROS AprilTag (with cuMotion). See
:doc:`examples` for the shared manipulator setup. All commands run through
``mros``.

.. tab-set::

   .. tab-item:: Simulation

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQCB1lM577qcRpSUZcgT0-BaAfLORo1zAq44SypAFNvkGmA?e=IijcRD&download=1
         :alt: AprilTag based pick-and-place
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQCB1lM577qcRpSUZcgT0-BaAfLORo1zAq44SypAFNvkGmA?e=IijcRD&download=1
         :align: center
         :width: 100%

         AprilTag based pick-and-place on simulation

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/4a_apriltag_pick_and_place_simulation.usd``

      2. Run the simulator bridge:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config sim_bridge.launch.py \
                 simulator:=isaacsim use_sim_time:=true

      3. Launch the planner and AprilTag detector:

         .. tab-set::

            .. tab-item:: MoveIt2 OMPL + OpenCV AprilTag
               :sync: ompl

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_perception apriltag_detector.launch.py use_sim_time:=true

            .. tab-item:: cuMotion + Isaac AprilTag
               :sync: cumotion

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion_apriltag.launch.py use_sim_time:=true

      4. Run the pick-and-place:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config apriltag_pick_and_place.launch.py \
                 use_sim_time:=true target_spawn:=false

   .. tab-item:: HIL

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQCB1lM577qcRpSUZcgT0-BaAfLORo1zAq44SypAFNvkGmA?e=IijcRD&download=1
         :alt: Manipulator executing a planned trajectory
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQCB1lM577qcRpSUZcgT0-BaAfLORo1zAq44SypAFNvkGmA?e=IijcRD&download=1
         :align: center
         :width: 100%

         AprilTag based pick-and-place on hardware-in-the-loop (HIL).

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/4b_apriltag_pick_and_place_hil.usd``

      2. Start WMX R2 for the manipulator (real WMX runtime) with
         ``use_sim_time:=true`` (see
         ``~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<MANIPULATOR_MODEL>_manipulator.md``).

      3. Launch the planner and AprilTag detector (with ``use_sim_time:=true``):

         .. tab-set::

            .. tab-item:: MoveIt2 OMPL + OpenCV AprilTag
               :sync: ompl

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_perception apriltag_detector.launch.py use_sim_time:=true

            .. tab-item:: cuMotion + Isaac AprilTag
               :sync: cumotion

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion_apriltag.launch.py use_sim_time:=true

         Add ``rsp:=false`` if using Gazebo or ``ros2_control`` -- both already
         publish ``/robot_description``.

      4. Run the pick-and-place:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config apriltag_pick_and_place.launch.py \
                 use_sim_time:=true target_spawn:=false

   .. tab-item:: Real

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQB-HDVUWfjsTavu8eyMafmrAY5gd92cerTYSNIcK_3OJgo?e=yUqLho&download=1
         :alt: Manipulator executing a planned trajectory
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQB-HDVUWfjsTavu8eyMafmrAY5gd92cerTYSNIcK_3OJgo?e=yUqLho&download=1
         :align: center
         :width: 100%

         AprilTag based pick-and-place on real-world scenario.

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/4c_apriltag_pick_and_place_real.usd``

      2. Start WMX R2 for the manipulator on the robot (see
         ``~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<MANIPULATOR_MODEL>_manipulator.md``).

      3. Launch the planner and AprilTag detector:

         .. tab-set::

            .. tab-item:: MoveIt2 OMPL + OpenCV AprilTag
               :sync: ompl

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_perception apriltag_detector.launch.py

            .. tab-item:: cuMotion + Isaac AprilTag
               :sync: cumotion

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion_apriltag.launch.py

         Add ``rsp:=false`` if using Gazebo or ``ros2_control`` -- both already
         publish ``/robot_description``.

      4. Run the pick-and-place (``target_spawn:=true`` spawns the target on the real
         setup):

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config apriltag_pick_and_place.launch.py \
                 use_sim_time:=false target_spawn:=true
