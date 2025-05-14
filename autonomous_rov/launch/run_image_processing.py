import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    return LaunchDescription([
        DeclareLaunchArgument('ns', default_value='br4', description='Namespace'),
        DeclareLaunchArgument('image_topic', default_value='raspicam_node/image/compressed', description='Image topic'),

        # Group to apply namespace
        launch.actions.PushRosNamespace(LaunchConfiguration('ns')),

        # Launch the node (without the .py extension)
        Node(
            package='autonomous_rov',  # The package name
            executable='image_processing_mir',  # Node executable name (without .py extension)
            name='image_processing_mir',
            output='screen',
            parameters=[{
                'cam_name': LaunchConfiguration('image_topic'),  # Set the parameter value for the image topic
            }]
        ),
    ])
