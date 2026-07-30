Commissioning
=============

.. warning:: **Read this before moving a physical robot.**

   WMX R2 drives servo drives directly over EtherCAT. It does not use the robot
   manufacturer's original controller, so the parameters that decide *how far*
   and *in which direction* a joint moves come from files in this stack, not
   from the robot vendor's firmware.

   A wrong gear ratio, encoder resolution, joint direction, or home offset
   produces unexpected motion **even when every piece of software is working
   correctly**. Following the instructions in this documentation does not by
   itself guarantee safe or expected motion on physical hardware. You must
   verify every robot-specific parameter and put your own safety measures in
   place before operating a physical system. See :doc:`safety` for what those
   measures are and who is responsible for them.

This section covers everything between "the software is installed" and "the
robot moves the way you intended": configuring and validating the
robot-specific parameters, bringing the first axis to life at low speed, and
understanding which safety functions this stack does and does not provide.

.. _simulation-first-workflow:

The simulation-first workflow
-----------------------------

Every stage below exists to catch a class of error while it is still cheap.
Do not skip stages, and do not run a later stage until the previous one is
clean.

.. list-table::
   :header-rows: 1
   :widths: 6 26 40 28

   * - #
     - Stage
     - What it proves
     - What it catches
   * - 1
     - **Parameter configuration and review**

       (:doc:`robot_parameters`)
     - The joint↔axis map, gear ratios, encoder resolution, directions, home
       offsets, and limits are written down and cross-checked against the
       URDF, the MoveIt configuration, and the WMX parameter file.
     - Typos, copied-from-another-robot values, and URDF/WMX disagreement.
   * - 2
     - **Simulation**

       (Isaac Sim or Gazebo, no WMX runtime)
     - The kinematics, planning scene, joint limits, and application logic are
       correct.
     - Bad URDF, unreachable targets, planner and collision errors.
   * - 3
     - **HIL**

       (simulator visuals, real WMX runtime, simulated bus)
     - The real WMX engine loads your parameter file, accepts the planner's
       trajectories, and produces the motion you expect — with no drive
       powered.
     - Parameter-file load failures, unit and scaling mistakes, trajectory
       rejections, engine and timing problems.
   * - 4
     - **Low-speed single-axis jogging**

       (:doc:`first_motion`)
     - Each physical axis is the joint you think it is, moves in the direction
       you think it does, travels the distance you command, and reports
       feedback that agrees.
     - Swapped axes, inverted polarity, wrong gear ratio, wrong home offset.
   * - 5
     - **Multi-axis motion on physical hardware**
     - Coordinated motion stays inside the workspace and clear of the robot's
       own structure and its surroundings.
     - Collisions and limit violations that a single axis cannot reveal.
   * - 6
     - **Trajectory execution**
     - Planner output executes end to end at working speed.
     - Timing, blending, and tracking-error problems.

.. note::

   Stages 2 and 3 map directly onto the **Simulation** and **HIL** tabs used
   throughout :doc:`../examples/examples`. Stage 6 is the **Real** tab. Stages
   4 and 5 sit between them and are described in :doc:`first_motion`.

Where the stages are documented
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Page
     - Covers
   * - :doc:`robot_parameters`
     - Every robot-specific parameter, where it lives, what it means, where
       its value comes from, and how to verify it against the running engine.
   * - :doc:`first_motion`
     - The commissioning and first-motion procedure: single axis, low speed,
       what to check at each step, and the exact stopping behavior of the jog
       tools.
   * - :doc:`safety`
     - Which safety functions are *not* provided when the original robot
       controller is bypassed, and the separate measures a physical system
       requires.
   * - :doc:`validated_hardware`
     - Which robots have been validated on physical hardware, which functions
       were tested, and what is untested or experimental.

.. toctree::
   :maxdepth: 2
   :hidden:

   robot_parameters
   first_motion
   safety
   validated_hardware
