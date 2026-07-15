movensys-navigation Setup
=========================

Set up the ``movensys-navigation`` stack once before running any of the
navigation scenarios. Like the manipulator examples, the scenarios run inside a
Docker container; the host only needs the environment variables, network tuning,
and the cloned repository described below. Commands run inside the container
through the ``nros`` helper (the navigation counterpart of ``mros``).

1. Host environment
-------------------

Add the following to your ``~/.bashrc`` (source it afterwards). The variables
select the ROS distro, the build flavor, the CPU architecture, and the robot
model, and define the ``nros`` helper used to run commands inside the container.

.. code-block:: bash

   export ROS_DOMAIN_ID=73                         # use any number
   export ROS_DISTRO=jazzy                         # {jazzy, humble}
   export MOVENSYS_ROS_VERSION=isaac-ros_4.1       # {isaac-ros_4.1, isaac-ros_3.2, general}
   export CPU_ARCH=amd64                           # {amd64, arm64}
   export NAVIGATION_MODEL=diffbot                 # {diffbot}

   export HOST_USER_UID=$(id -u)
   export HOST_USER_GID=$(id -g)
   export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

   export MOVENSYS_NAVIGATION_PACKAGES=~/workspaces/movensys_ws/src/movensys-navigation
   export ISAAC_ROS_WS=~/workspaces/isaac_ros-dev

   nros() {
     if [ $# -eq 0 ]; then
       docker exec -it -u admin movensys_navigation_container \
         bash -lc 'source /opt/ros/${ROS_DISTRO}/setup.bash && source /home/admin/workspaces/movensys_ws/install/setup.bash && exec bash -i'
     else
       docker exec -it -u admin movensys_navigation_container \
         bash -lc "source /opt/ros/\${ROS_DISTRO}/setup.bash && source /home/admin/workspaces/movensys_ws/install/setup.bash && $*"
     fi
   }

Allow the container to reach the host X server and reload the shell:

.. code-block:: bash

   xhost +local:docker
   source ~/.bashrc

2. CycloneDDS network buffers
-----------------------------

Raise the kernel socket-buffer limits so the CycloneDDS RMW can carry the
odometry, laser scan, and image traffic without drops:

.. code-block:: bash

   sudo tee /etc/sysctl.d/99-network-buffers.conf << 'EOF'
   net.core.rmem_max=67108864
   net.core.rmem_default=67108864
   net.core.wmem_max=67108864
   net.core.wmem_default=67108864
   EOF

   sudo sysctl -p /etc/sysctl.d/99-network-buffers.conf
   sysctl net.core.rmem_max net.core.rmem_default net.core.wmem_max net.core.wmem_default

3. Clone the repository
-----------------------

.. code-block:: bash

   mkdir -p ~/workspaces/movensys_ws/src
   cd ~/workspaces/movensys_ws/src
   git clone git@github.com:movensys/movensys-navigation.git

4. Build and start the container
--------------------------------

.. note::

   For the ``isaac-ros_*`` build flavors, complete the
   `Isaac ROS getting-started setup
   <https://nvidia-isaac-ros.github.io/getting_started/index.html>`_ first
   (the ``release-3.2`` and ``release-4.1`` guides match
   ``MOVENSYS_ROS_VERSION=isaac-ros_3.2`` / ``isaac-ros_4.1``).

The compose files combine the ROS-version layer with the per-architecture
navigation layer:

.. code-block:: bash

   cd ${MOVENSYS_NAVIGATION_PACKAGES}/docker
   docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml down
   docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml build
   docker compose -f ${MOVENSYS_ROS_VERSION}.yaml -f movensys_navigation.${CPU_ARCH}.yaml up -d

Follow the container startup logs:

.. code-block:: bash

   docker logs movensys_navigation_container -f

5. Enter the container
----------------------

All scenario commands run through ``nros``, which executes inside the
``movensys_navigation_container``. Open an interactive shell:

.. code-block:: bash

   nros

Verify the build by launching the robot description in RViz:

.. code-block:: bash

   nros ros2 launch movensys_navigation_description movensys_navigation_rviz.launch.py

For SIL and Real modes, the base is brought up with WMX R2 (see
``wmx-r2/doc/launch_<NAVIGATION_MODEL>_navigation.md`` and
:doc:`../getting_started/install_wmx3`).

.. note:: **Isaac Sim scenes**

   The Simulation and SIL modes load USD scenes in NVIDIA Isaac Sim. See
   :doc:`isaacsim_setup` for the Isaac Sim installation and the scene layout.
