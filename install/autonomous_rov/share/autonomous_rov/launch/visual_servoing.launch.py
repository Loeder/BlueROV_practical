import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource, AnyLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Arguments
    namespace = LaunchConfiguration('namespace')
    run_tracker = LaunchConfiguration('run_image_processing_tracker')

    return LaunchDescription([
        DeclareLaunchArgument(
            'namespace', default_value='bluerov2',
            description='Namespace for nodes'
        ),
        DeclareLaunchArgument(
            'run_image_processing_tracker', default_value='off',
            description='Flag to run image processing tracker'
        ),

        # Include modular launch files (XML and Python)
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('autonomous_rov'),
                    'launch', 'run_gamepad.launch'
                )
            )
        ),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('autonomous_rov'),
                    'launch', 'run_listener_MIR_joy.launch'
                )
            )
        ),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('autonomous_rov'),
                    'launch', 'run_mavros.launch'
                )
            )
        ),

        # Launch video node
        Node(
            package='autonomous_rov',
            executable='video',
            name='video',
            output='screen'
        ),

        # Conditionally launch image processing tracker
        Node(
            package='autonomous_rov',
            executable='image_processing_tracker',
            name='image_processing_tracker',
            output='screen'
        )
    ])
