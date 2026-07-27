AprilTag + Obstacle Avoidance
=============================

Combines AprilTag-driven pick-and-place with Nvblox obstacle avoidance: Isaac
cuMotion plans collision-free motion against a live Nvblox reconstruction while
Isaac ROS AprilTag locates the target. See :doc:`examples` for the shared
manipulator setup. All commands run through ``mros``.

.. tab-set::

   .. tab-item:: Simulation

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQA9AvezFL6rRqAk2lkE2t2pAVITAVf0p90ZtDtATjCjM4g?e=pU18j7&download=1
         :alt: AprilTag based Obstacle Avoidance
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQA9AvezFL6rRqAk2lkE2t2pAVITAVf0p90ZtDtATjCjM4g?e=pU18j7&download=1
         :align: center
         :width: 100%

         AprilTag based Obstacle Avoidance on simulation
   
   .. tab-item:: SIL

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQA9AvezFL6rRqAk2lkE2t2pAVITAVf0p90ZtDtATjCjM4g?e=pU18j7&download=1
         :alt: AprilTag based Obstacle Avoidance
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQA9AvezFL6rRqAk2lkE2t2pAVITAVf0p90ZtDtATjCjM4g?e=pU18j7&download=1
         :align: center
         :width: 100%

         AprilTag based Obstacle Avoidance on simulation-in-loop (SIL).

   .. tab-item:: Real

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQDxqbaey2rhRJ4qPuWfbd9sAYPrIkuX3Ztz16QSwkvpTmY?e=Br0Ybv&download=1
         :alt: AprilTag based Obstacle Avoidance
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQDxqbaey2rhRJ4qPuWfbd9sAYPrIkuX3Ztz16QSwkvpTmY?e=Br0Ybv&download=1
         :align: center
         :width: 100%

         AprilTag based Obstacle Avoidance on real-world scenario.

.. tab-set::

   .. tab-item:: Simulation

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/7a_apriltag_obstacle_avoidance_simulation.usd``

      2. Run the simulator bridge:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config sim_bridge.launch.py \
                 simulator:=isaacsim use_sim_time:=true

      3. Launch cuMotion + Nvblox:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion_nvblox.launch.py use_sim_time:=true

      4. Launch Isaac AprilTag:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_isaac_ros_config isaac_apriltag.launch.py use_sim_time:=true

      5. Run AprilTag pick-and-place with obstacle avoidance:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config apriltag_pick_and_place.launch.py \
                 use_sim_time:=true target_spawn:=false

   .. tab-item:: SIL

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/7b_apriltag_obstacle_avoidance_hil.usd``

      2. Start WMX R2 for the manipulator (real WMX runtime) with
         ``use_sim_time:=true`` (see
         ``~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<MANIPULATOR_MODEL>_manipulator.md``).

      3. Launch cuMotion + Nvblox:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion_nvblox.launch.py use_sim_time:=true

      4. Launch Isaac AprilTag:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_isaac_ros_config isaac_apriltag.launch.py use_sim_time:=true

      5. Run AprilTag pick-and-place with obstacle avoidance:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config apriltag_pick_and_place.launch.py \
                 use_sim_time:=true target_spawn:=false

   .. tab-item:: Real

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/7c_apriltag_obstacle_avoidance_real.usd``

      2. Start WMX R2 for the manipulator on the robot (see
         ``~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<MANIPULATOR_MODEL>_manipulator.md``).

      3. Launch cuMotion + Nvblox:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion_nvblox.launch.py

      4. Launch Isaac AprilTag:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_isaac_ros_config isaac_apriltag.launch.py

      5. Run AprilTag pick-and-place with obstacle avoidance:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config apriltag_pick_and_place.launch.py \
                 use_sim_time:=false target_spawn:=true
