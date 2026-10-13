# TurtleBot 4 SLAM Toolbox and Nav2

ROS 2 Humble package for TurtleBot 4 Lite simulation, mapping with SLAM Toolbox, localization, and Nav2. It uses the local `maze` world and a lightweight robot description without the OAK-D camera. The dock and auxiliary Create3 range sensors are disabled by default to reduce WSL load; the main GPU LiDAR publishes `/scan`.

## Build

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select turtlebot4_slam_nav2
source install/setup.bash
```

Required packages include `ros-humble-turtlebot4-simulator`, `ros-humble-turtlebot4-navigation`, `ros-humble-slam-toolbox`, `ros-humble-nav2-bringup`, and `ros-humble-teleop-twist-keyboard`.

## 1. Mapping

Start the simulation, SLAM Toolbox, and RViz2. Gazebo's GUI is off by default; RViz2 provides the robot and map view.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch turtlebot4_slam_nav2 mapping.launch.py model:=lite world:=maze gui:=false rviz:=true
```

In another terminal, drive the robot slowly with keyboard teleoperation:

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/cmd_vel
```

Use `i` to move, `j`/`l` to turn, `k` to stop, and `Ctrl+C` to quit. Cover the accessible corridors and open areas with overlapping scans. In RViz, use fixed frame `map` and display `/map` and `/scan`.

Save the map after surveying the environment:

```bash
mkdir -p ~/ros2_ws/src/turtlebot4_slam_nav2/maps
ros2 run nav2_map_server map_saver_cli -t /map -f ~/ros2_ws/src/turtlebot4_slam_nav2/maps/tb4_maze
```

This should create `tb4_maze.yaml` and `tb4_maze.pgm`. Confirm that the map has walls and passages before stopping the mapping launch.

## 2. Localization and navigation

Stop mapping, then launch a fresh simulator with the saved map:

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch turtlebot4_slam_nav2 localization_navigation.launch.py \
  model:=lite world:=maze gui:=false rviz:=true \
  map:=$HOME/ros2_ws/src/turtlebot4_slam_nav2/maps/tb4_maze.yaml
```

In RViz, set **2D Pose Estimate** at the robot's Gazebo spawn location and wait for scan/map alignment. Use **Nav2 Goal** to send at least two goals in different open areas. Do not use teleoperation after setting a goal; confirm Nav2 reaches each one without collision.

## Checks

```bash
ros2 topic hz /scan
ros2 topic hz /odom
ros2 topic info /cmd_vel
ros2 action list | grep navigate_to_pose
```

## WSL renderer configuration

The 2026-10-13 check resolved the all-range-min LiDAR input by using OGRE2 for the sensor/server renderer and OGRE for the Gazebo GUI, with `LIBGL_ALWAYS_SOFTWARE=1`. The scan contained 360 beams with finite distances from 1.00 to 11.64 m; SLAM produced an initial 341 x 237 occupancy grid. A velocity test moved the robot 0.109 m and stopped it. The current saved map is 459 x 441 cells at 0.05 m/cell; 72.2% of cells inside the 20 x 20 m world bounds are known. The remaining area needs more survey passes. Localization and Nav2 goals were not tested in this run.

Use `bash reports/turtlebot4_video/run.sh mapping` from the workspace for the software-rendering profile, and see `reports/turtlebot4_video/README.md` for the recording sequence. WSL has about 1.8 GB RAM on this machine, so simultaneous GUI processes may run slowly. A partial saved map is available at src/turtlebot4_slam_nav2/maps/map.yaml and map.pgm. Localization and Nav2 goals remain to be tested.

