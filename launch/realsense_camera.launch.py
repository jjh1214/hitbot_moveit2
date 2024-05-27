from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

local_parameters = [
                    {'name': 'camera_name', 'default': 'camera', 'description': 'camera unique name'},
                    {'name': 'camera_name2', 'default': 'camera_2', 'description': 'camera unique name'},
                    {'name': 'serial_no1', 'default': '_150622071179', 'description': 'serial id number'},
                    {'name': 'pointcloud.enable1', 'default': 'true', 'description': ''},
                    {'name': 'align_depth.enable1', 'default': 'true', 'description': ''},
                    ]

def declare_configurable_parameters(parameters):
    return [DeclareLaunchArgument(param['name'], default_value=param['default'], description=param['description']) for param in parameters]

def set_configurable_parameters(parameters):
    return dict([(param['name'], LaunchConfiguration(param['name'])) for param in parameters])

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('camera_name', default_value='camera', description='camera unique name for camera 1'),
        DeclareLaunchArgument('serial_no1', default_value='_150622071179', description='serial id number for camera 1'),
        DeclareLaunchArgument('align_depth.enable1', default_value='true', description=''),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([FindPackageShare('realsense2_camera'), '/launch/rs_launch.py']),
            launch_arguments=[
                ('camera_name', LaunchConfiguration('camera_name')),
                ('serial_no', LaunchConfiguration('serial_no1')),
                ('depth_module.profile', '640x480x30'),
                ('pointcloud.enable', 'true'),
                ('rgb_camera.profile', '640x480x30'),
            ],
        ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([FindPackageShare('realsense2_camera'), '/launch/rs_launch.py']),
        #     launch_arguments=[
        #         ('camera_name', LaunchConfiguration('camera_name2')),
        #         ('serial_no', LaunchConfiguration('serial_no2')),
        #         ('depth_module.profile', '640x480x30'),
        #         ('pointcloud.enable', 'true'),
        #         ('rgb_camera.profile', '640x480x30'),
        #     ],
        # ),

##카메라 실제 위치 조정. 메인은 객체를 찍고 처리하는 카메라 기준. 그러니까 yolob8에서 구독하고 있는 이미지를 발행하는 카메라가 기준.
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='camera_with_robot_tf',
            arguments=['0.38', '0.23', '0', '0', '0', '0', 'camera_link', 'world'
                       
                       ],
            output='screen',
        ),
    ])