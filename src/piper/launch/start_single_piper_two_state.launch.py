from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Declare the launch arguments
    can_port_arg = DeclareLaunchArgument(
        'can_port',
        default_value='can0',
        description='CAN port to be used by the Piper node.'
    )
    auto_enable_arg = DeclareLaunchArgument(
        'auto_enable',
        default_value='true',
        description='Automatically enable the Piper node.'
    )

    rviz_ctrl_flag_arg = DeclareLaunchArgument(
        'rviz_ctrl_flag',
        default_value='false',
        description='Start rviz flag.'
    )

    gripper_exist_arg = DeclareLaunchArgument(
        'gripper_exist',
        default_value='true',
        description='gripper'
    )

    gripper_val_multiple_arg = DeclareLaunchArgument(
        'gripper_val_multiple',
        default_value='1',
        description='gripper'
    )

    # Define the node (previous piper node from "start_single_piper.launch.py")
    # piper_node = Node(
    #     package='piper',
    #     executable='piper_single_ctrl',
    #     name='piper_ctrl_single_node',
    #     output='screen',
    #     parameters=[{
    #         'can_port': LaunchConfiguration('can_port'),
    #         'auto_enable': LaunchConfiguration('auto_enable'),
    #         'gripper_val_mutiple': LaunchConfiguration('gripper_val_mutiple'),
    #         'gripper_exist': LaunchConfiguration('gripper_exist'),
    #     }],
    #     remappings=[
    #         ('joint_ctrl_single', '/joint_states'),
    #     ]
    # )

    # Node definition
    piper_node = Node(
        package='piper',
        executable='piper_single_ctrl_two_state',
        name='piper_ctrl_single_two_state_node',
        output='screen',
        parameters=[{
            'can_port': LaunchConfiguration('can_port'),
            'auto_enable': LaunchConfiguration('auto_enable'),
            'gripper_val_multiple': LaunchConfiguration('gripper_val_multiple'),
            'gripper_exist': LaunchConfiguration('gripper_exist'),
        }],
        remappings=[
            ('joint_ctrl_single', '/joint_states')
        ]
    )

    # Return the LaunchDescription
    return LaunchDescription([
        can_port_arg,
        auto_enable_arg,
        gripper_exist_arg,
        gripper_val_multiple_arg,
        piper_node
    ])
