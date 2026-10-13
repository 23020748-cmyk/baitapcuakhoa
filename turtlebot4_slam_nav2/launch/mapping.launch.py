from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
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
    return LaunchDescription([
        SetEnvironmentVariable(name='FASTDDS_BUILTIN_TRANSPORTS', value='UDPv4'),
        DeclareLaunchArgument('model', default_value='lite', choices=['lite']),
        DeclareLaunchArgument('rviz', default_value='true', choices=['true', 'false']),
        # The local spawn wrapper forwards this world name to the sensor bridge.
        DeclareLaunchArgument('world', default_value='maze', choices=['maze', 'warehouse']),
        DeclareLaunchArgument('gui', default_value='false', choices=['true', 'false']),
        _include('turtlebot4_slam_nav2', 'ignition.launch.py', {
            'world': world, 'model': model, 'use_sim_time': 'true', 'gui': gui
        }),
        _include('turtlebot4_slam_nav2', 'turtlebot4_spawn.launch.py', {
            'model': model, 'use_sim_time': 'true', 'rviz': rviz, 'world': world,
            'slam': 'true', 'localization': 'false', 'nav2': 'false'
        }),
    ])





