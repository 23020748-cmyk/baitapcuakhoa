from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def _include(package, launch_file, arguments):
    path = PathJoinSubstitution([
        get_package_share_directory(package), 'launch', launch_file
    ])
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(path), launch_arguments=arguments.items()
    )


def generate_launch_description():
    model = LaunchConfiguration('model')
    rviz = LaunchConfiguration('rviz')
    world = LaunchConfiguration('world')
    gui = LaunchConfiguration('gui')
    map_yaml = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    return LaunchDescription([
        SetEnvironmentVariable(name='FASTDDS_BUILTIN_TRANSPORTS', value='UDPv4'),
        DeclareLaunchArgument('model', default_value='lite', choices=['lite']),
        DeclareLaunchArgument('rviz', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('world', default_value='maze', choices=['maze', 'warehouse']),
        DeclareLaunchArgument('gui', default_value='false', choices=['true', 'false']),
        DeclareLaunchArgument('use_sim_time', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('map', default_value=PathJoinSubstitution([
            get_package_share_directory('turtlebot4_slam_nav2'), 'maps', 'tb4_maze.yaml'
        ]), description='Saved occupancy-grid map YAML'),
        _include('turtlebot4_slam_nav2', 'ignition.launch.py', {
            'world': world, 'model': model, 'use_sim_time': use_sim_time, 'gui': gui
        }),
        _include('turtlebot4_slam_nav2', 'turtlebot4_spawn.launch.py', {
            'model': model, 'use_sim_time': use_sim_time, 'rviz': rviz, 'world': world,
            'slam': 'false', 'localization': 'false', 'nav2': 'false'
        }),
        # Let Gazebo spawn the robot before AMCL and the Nav2 lifecycle nodes start.
        TimerAction(period=8.0, actions=[
            _include('turtlebot4_navigation', 'localization.launch.py', {
                'map': map_yaml, 'use_sim_time': use_sim_time
            }),
            _include('turtlebot4_navigation', 'nav2.launch.py', {
                'use_sim_time': use_sim_time
            }),
        ]),
    ])





