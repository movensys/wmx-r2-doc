YOLO Pick-and-Place
===================

Detect cubes and dice with YOLO and pick and place them. The detector moves to
a scan pose, visually servos over each detected object, picks it, and places it
in the per-class drop box. See :doc:`examples` for the shared manipulator
setup. All commands run through ``mros``.

.. tab-set::

   .. tab-item:: Simulation

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQAKSfUzPqN9QbQ1exoS5K_TAcv7l0fPK0dwXwBQWrZUuOM?e=jYXiL9&download=1
         :alt: Yolo pick-and-place
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQA9AvezFL6rRqAk2lkE2t2pAVITAVf0p90ZtDtATjCjM4g?e=pU18j7&download=1
         :align: center
         :width: 100%

         Yolo pick-and-place on simulation

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/8a_yolo_pick_and_place_simulation.usd``

      2. Run the simulator bridge:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config sim_bridge.launch.py \
                 simulator:=isaacsim use_sim_time:=true

      3. Launch the planner and service API:

         .. tab-set::

            .. tab-item:: MoveIt2 OMPL
               :sync: ompl

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_moveit_config moveit.launch.py use_sim_time:=true

            .. tab-item:: Isaac cuMotion
               :sync: cumotion

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion.launch.py use_sim_time:=true

      4. Launch the YOLO cube detector (the simulation scene contains cubes
         only):

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_perception yolo_cube_detector.launch.py use_sim_time:=true

      5. Execute the YOLO pick-and-place:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config yolo_pick_and_place.launch.py use_sim_time:=true

         (Pick/drop poses are loaded from ``config/<MANIPULATOR_MODEL>/yolo_trajectory.yaml``.)

         Debug the detections (optional):

         .. code-block:: bash

            ros2 run rqt_image_view rqt_image_view /yolo_cube_detector/debug_image

   .. tab-item:: HIL

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQAKSfUzPqN9QbQ1exoS5K_TAcv7l0fPK0dwXwBQWrZUuOM?e=jYXiL9&download=1
         :alt: Yolo pick-and-place
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQA9AvezFL6rRqAk2lkE2t2pAVITAVf0p90ZtDtATjCjM4g?e=pU18j7&download=1
         :align: center
         :width: 100%

         Yolo pick-and-place on hardware-in-the-loop (HIL)

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/8b_yolo_pick_and_place_hil.usd``

      2. Start WMX R2 for the manipulator (real WMX runtime) with
         ``use_sim_time:=true`` (see
         ``~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<MANIPULATOR_MODEL>_manipulator.md``).

      3. Launch the planner and service API with ``use_sim_time:=true``:

         .. tab-set::

            .. tab-item:: MoveIt2 OMPL
               :sync: ompl

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_moveit_config moveit.launch.py use_sim_time:=true

            .. tab-item:: Isaac cuMotion
               :sync: cumotion

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion.launch.py use_sim_time:=true

         Add ``rsp:=false`` if using Gazebo or ``ros2_control`` -- both already
         publish ``/robot_description``.

      4. Launch the YOLO cube and dice detector:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_perception yolo_dice_and_cube_detector.launch.py use_sim_time:=true

      5. Execute the YOLO pick-and-place:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config yolo_pick_and_place.launch.py use_sim_time:=true

   .. tab-item:: Real

      .. figure:: https://softservogroup.sharepoint.com/:i:/s/Storage/IQBwJ10DEqUuTYIEju5NsoetAbTusZtOxT2Zx6GPbd8Izrs?e=vOCl68&download=1
         :alt: Yolo pick-and-place
         :target: https://softservogroup.sharepoint.com/:i:/s/Storage/IQDxqbaey2rhRJ4qPuWfbd9sAYPrIkuX3Ztz16QSwkvpTmY?e=Br0Ybv&download=1
         :align: center
         :width: 100%

         Yolo pick-and-place on real-world scenario

      1. Open the Isaac Sim scene:
         ``~/workspaces/movensys-simulation/<MANIPULATOR_MODEL>/8c_yolo_pick_and_place_real.usd``

      2. Start WMX R2 for the manipulator on the robot (see
         ``~/workspaces/movensys_ws/src/wmx-r2/doc/launch_<MANIPULATOR_MODEL>_manipulator.md``).

      3. Launch the planner and service API:

         .. tab-set::

            .. tab-item:: MoveIt2 OMPL
               :sync: ompl

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_moveit_config moveit.launch.py

            .. tab-item:: Isaac cuMotion
               :sync: cumotion

               .. code-block:: bash

                  mros ros2 launch movensys_manipulator_isaac_ros_config isaac_cumotion.launch.py

         Add ``rsp:=false`` if using Gazebo or ``ros2_control`` -- both already
         publish ``/robot_description``.

      4. Launch the YOLO cube and dice detector:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_perception yolo_dice_and_cube_detector.launch.py

         Debug the detections (optional):

         .. code-block:: bash

            ros2 run rqt_image_view rqt_image_view /yolo_dice_detector/debug_image
            ros2 run rqt_image_view rqt_image_view /yolo_cube_detector/debug_image

      5. (optional) Execute the YOLO pick-and-place:

         .. code-block:: bash

            mros ros2 launch movensys_manipulator_moveit_config yolo_pick_and_place.launch.py

.. note::

   The YOLO pick-and-place is the perception layer used by the
   :doc:`robopoly_game`, which adds voice and VLM/LLM control on top.
