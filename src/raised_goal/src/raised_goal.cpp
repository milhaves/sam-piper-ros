#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/display_robot_state.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>
// #include <moveit_visual_tools/moveit_visual_tools.h>

int main(int argc, char * argv[])
{
  // Initialize ROS and create the Node
  rclcpp::init(argc, argv);
  auto const node = std::make_shared<rclcpp::Node>(
    "raised_goal",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)
  );

  // Create a ROS logger
  auto const logger = rclcpp::get_logger("raised_goal");

  // Create the MoveIt MoveGroup Interface
  // using moveit::planning_interface::MoveGroupInterface;
  // auto move_group_interface = MoveGroupInterface(node, "arm");

  moveit::planning_interface::MoveGroupInterface move_group(node, "arm");

  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

  // Set a target Pose
  // auto const target_pose = []{
  //   geometry_msgs::msg::Pose msg;
  //   msg.orientation.w = 1.0;
  //   msg.position.x = 0;
  //   msg.position.y = 0;
  //   msg.position.z = 0.75;
  //   return msg;
  // }();
  // move_group_interface.setPoseTarget(target_pose);

  // const moveit::core::JointModelGroup* joint_model_group = move_group.getCurrentState()->getJointModelGroup("arm");

  // Create pointer that references the robot's current state
  // moveit::core::RobotStatePtr current_state = move_group.getCurrentState(10);

  // Get the current set of joint values for the group
  // std::vector<double> joint_group_positions;
  // current_state->copyJointGroupPositions(joint_model_group, joint_group_positions);

  // Set new joint goals
  // joint_group_positions[0] = 0.0;
  // joint_group_positions[1] = 1.46;
  // joint_group_positions[2] = -2.967;
  // joint_group_positions[3] = 0.0;
  // joint_group_positions[4] = -0.072;
  // joint_group_positions[5] = 0.0;
  // joint_group_positions[6] = 0.0;

  // Borrowed from poppin-fetch/src/MoveItClient.cpp, alan-sanchez
  // std::vector<std::string> joint_names = {"joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"};
  std::vector<std::string> joint_names = {"joint1", "joint2", "joint3", "joint4", "joint5", "joint6"};

  // const std::vector<double> joint_values = {0.0, 1.46, -2.967, 0.0, -0.072, 0.0, 0.0};
  const std::vector<double> joint_values = {0.0, 1.46, -2.967, 0.0, -0.1, 0.0};

  std::map<std::string, double> joint_targets;
  for (size_t i = 0; i < joint_names.size(); ++i) {
      joint_targets[joint_names[i]] = joint_values[i];
  }

  // bool within_bounds = move_group.setJointValueTarget(joint_group_positions);
  bool within_bounds = move_group.setJointValueTarget(joint_targets);
  if (!within_bounds)
  {
    RCLCPP_WARN(logger, "Target joint position(s) were outside of limits, but we will plan and clamp to the limits ");
  }

  // Set max vel and max accel to 5% of actual max
  // move_group.setMaxVelocityScalingFactor(0.05);
  move_group.setMaxVelocityScalingFactor(1.0);
  move_group.setMaxAccelerationScalingFactor(0.05);

  // Create collision object for the robot to avoid
  // auto const collision_object = [frame_id = move_group_interface.getPlanningFrame()] {
  auto const collision_object = [frame_id = move_group.getPlanningFrame()] {
    moveit_msgs::msg::CollisionObject collision_object;
    collision_object.header.frame_id = frame_id;
    collision_object.id = "payload";
    shape_msgs::msg::SolidPrimitive primitive1;
    shape_msgs::msg::SolidPrimitive primitive2;
    shape_msgs::msg::SolidPrimitive primitive3;

    // Define the size of the box in meters
    // Spot IO and Rajant Antenna
    primitive1.type = primitive1.BOX;
    primitive1.dimensions.resize(3);
    primitive1.dimensions[primitive1.BOX_X] = 0.245;
    primitive1.dimensions[primitive1.BOX_Y] = 0.18;
    primitive1.dimensions[primitive1.BOX_Z] = 0.2;

    // Jetson, Spot GXP, Rajant Antenna, and Cardinal
    primitive2.type = primitive2.BOX;
    primitive2.dimensions.resize(3);
    primitive2.dimensions[primitive2.BOX_X] = 0.285;
    primitive2.dimensions[primitive2.BOX_Y] = 0.192;
    primitive2.dimensions[primitive2.BOX_Z] = 0.08;

    // Insta360
    primitive3.type = primitive3.BOX;
    primitive3.dimensions.resize(3);
    primitive3.dimensions[primitive3.BOX_X] = 0.025;
    primitive3.dimensions[primitive3.BOX_Y] = 0.085;
    primitive3.dimensions[primitive3.BOX_Z] = 0.515;

    // Define the pose of the box (relative to the frame_id)
    geometry_msgs::msg::Pose box_pose1;
    box_pose1.orientation.w = 1.0;
    box_pose1.position.x = 0.2;
    box_pose1.position.y = 0.0;
    box_pose1.position.z = 0.07;

    geometry_msgs::msg::Pose box_pose2;
    box_pose2.orientation.w = 1.0;
    box_pose2.position.x = -0.21;
    box_pose2.position.y = 0.0;
    box_pose2.position.z = 0.015;

    geometry_msgs::msg::Pose box_pose3;
    box_pose3.orientation.w = 1.0;
    box_pose3.position.x = 0.36;
    box_pose3.position.y = 0.0;
    box_pose3.position.z = 0.2225;

    collision_object.primitives.push_back(primitive1);
    collision_object.primitive_poses.push_back(box_pose1);
    collision_object.operation = collision_object.ADD;

    collision_object.primitives.push_back(primitive2);
    collision_object.primitive_poses.push_back(box_pose2);
    collision_object.operation = collision_object.ADD;

    collision_object.primitives.push_back(primitive3);
    collision_object.primitive_poses.push_back(box_pose3);
    collision_object.operation = collision_object.ADD;

    return collision_object;
  }();

  // auto const collision_object = [frame_id = move_group_interface.getPlanningFrame()] {
  //   moveit_msgs::msg::CollisionObject collision_object;
  //   collision_object.header.frame_id = frame_id;
  //   collision_object.id = "box2";
  //   shape_msgs::msg::SolidPrimitive primitive;

  //   // Define the size of the box in meters
  //   primitive.type = primitive.BOX;
  //   primitive.dimensions.resize(3);
  //   primitive.dimensions[primitive.BOX_X] = 0.285;
  //   primitive.dimensions[primitive.BOX_Y] = 0.192;
  //   primitive.dimensions[primitive.BOX_Z] = 0.08;

  //   // Define the pose of the box (relative to the frame_id)
  //   geometry_msgs::msg::Pose box_pose;
  //   box_pose.orientation.w = 1.0;
  //   box_pose.position.x = 0.193;
  //   box_pose.position.y = 0.0;
  //   box_pose.position.z = 0.04;

  //   collision_object.primitives.push_back(primitive);
  //   collision_object.primitive_poses.push_back(box_pose);
  //   collision_object.operation = collision_object.ADD;

  //   return collision_object;
  // }();

  // Add the collision object to the scene
  // moveit::planning_interface::PlanningSceneInterface planning_scene_interface;
  planning_scene_interface.applyCollisionObject(collision_object);
  // planning_scene_interface.applyCollisionObject(collision_object2);

  // Create a plan to that target pose
  // auto const [success, plan] = [&move_group_interface]{
  auto const [success, plan] = [&move_group]{
    moveit::planning_interface::MoveGroupInterface::Plan msg;
    // auto const ok = static_cast<bool>(move_group_interface.plan(msg));
    auto const ok = static_cast<bool>(move_group.plan(msg));
    return std::make_pair(ok, msg);
  }();

  // Execute the plan
  if(success) {
    // move_group_interface.execute(plan);
    move_group.execute(plan);
  } else {
    RCLCPP_ERROR(logger, "Planing failed!");
  }

  // Shutdown ROS
  rclcpp::shutdown();
  return 0;
}