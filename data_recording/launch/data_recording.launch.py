from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config = os.path.join(get_package_share_directory('data_recording'), 'config', 'config.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=config,
            description='Full path to the config file to be loaded'),

        Node(
            package='data_recording',
            executable='data_recording.py',
            name='data_recording',
            output='screen',
            parameters=[LaunchConfiguration('config_file')]
        )
    ])