# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass
from isaaclab.managers import EventTermCfg as EventTerm
import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import RewardTermCfg as RewTerm
from .rough_env_cfg import UnitreeGo1RoughEnvCfg


@configclass
class UnitreeGo1FlatEnvCfg(UnitreeGo1RoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # override rewards
        self.rewards.flat_orientation_l2.weight = -2.5
        self.rewards.feet_air_time.weight = 0.25

        ##更改相机位置
        self.viewer.eye = (-2.0,3.0,1.5)
        self.viewer.lookat=(0.0,0.0,0.0)
        self.viewer.origin_type = "asset_root" 
        self.viewer.env_index = 0  
        self.viewer.asset_name = "robot"   #跟拍
        #固定奔跑方向
        self.commands.base_velocity.ranges.lin_vel_x = (1.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (0.0, 0.0)

        #加速度和扭矩惩罚
        self.rewards.dof_torques_l2 = RewTerm(func=mdp.joint_torques_l2, weight=-1.0e-4)#扭矩惩罚#-5
        self.rewards.dof_acc_l2 = RewTerm(func=mdp.joint_acc_l2, weight=-5e-7)#加速度惩罚#-2.5e-7
        self.rewards.action_rate_l2 = RewTerm(func=mdp.action_rate_l2, weight=-0.01)#震动#-0.01

        #摩擦力
        self.events.physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=".*"),
            "static_friction_range": (0.3, 0.4),#改过原来是（0.8, 0.8）#(0.3, 0.4)
            "dynamic_friction_range": (0.1, 0.2),#改过原来是（0.6, 0.6）#(0.1, 0.2)
            "restitution_range": (0.0, 0.0),
            "num_buckets": 64,
        },
    )  
        #随机频率随机速度
        self.events.push_robot = EventTerm(
        func=mdp.push_by_setting_velocity,
        mode="interval",
        interval_range_s=(2.0, 3.0),#(10.0,15.0)
        
        params={"velocity_range": {"x": (-2.0, 2.0), "y": (-2.0, 2.0)}},#改过原来都是(-0.5, 0.5)
    )
        

        # change terrain to flat
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None
        # no height scan
        self.scene.height_scanner = None
        self.observations.policy.height_scan = None
        # no terrain curriculum
        self.curriculum.terrain_levels = None


class UnitreeGo1FlatEnvCfg_PLAY(UnitreeGo1FlatEnvCfg):
    def __post_init__(self) -> None:
        # post init of parent
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        """##更改相机位置
        self.viewer.eye = (-2.0,3.0,1.5)
        self.viewer.lookat=(0.0,0.0,0.0)
        self.viewer.origin_type = "asset_root" 
        self.viewer.env_index = 0  
        self.viewer.asset_name = "robot"   #跟拍
        self.commands.base_velocity.ranges.lin_vel_x = (1.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (0.0, 0.0)
        
        #录像时增加推力和干扰
        # disable randomization for play
        self.observations.policy.enable_corruption = True
        # remove random pushing event
        
        self.events.base_external_force_torque = None
        self.events.push_robot = None"""
        
