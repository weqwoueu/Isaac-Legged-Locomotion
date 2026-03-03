# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


from isaaclab.utils import configclass
from isaaclab.managers import EventTermCfg as EventTerm
import isaaclab_tasks.manager_based.locomotion.velocity.mdp as mdp
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab_tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityRoughEnvCfg
from .rough_env_cfg import AnymalCRoughEnvCfg


@configclass
class AnymalCFlatEnvCfg(AnymalCRoughEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        ##更改相机位置
        self.viewer.eye = (-2.0,3.0,1.5)
        self.viewer.lookat=(0.0,0.0,0.0)
        self.viewer.origin_type = "asset_root" 
        self.viewer.env_index = 0  
        self.viewer.asset_name = "robot"   #跟拍

        """#reward设置
        self.rewards.dof_torques_l2 = RewTerm(func=mdp.joint_torques_l2, weight=-1.0e-4)#扭矩惩罚#e-5
        self.rewards.dof_acc_l2 = RewTerm(func=mdp.joint_acc_l2, weight=-2.5e-7)#加速度惩罚#-2.5e-7
        self.rewards.action_rate_l2 = RewTerm(func=mdp.action_rate_l2, weight=-0.02)#震动惩罚#-0，01
        self.rewards.flat_orientation_l2 = RewTerm(func=mdp.flat_orientation_l2, weight=0.02)#躯干姿态惩罚#0.0
        self.rewards.feet_air_time = RewTerm(#离地时间
        func=mdp.feet_air_time,
        weight=0.5,#0.125
        params={
            "sensor_cfg": SceneEntityCfg("contact_forces", body_names=".*FOOT"),
            "command_name": "base_velocity",
            "threshold": 0.5,
        },)"""
        

        # override rewards
        self.rewards.flat_orientation_l2.weight = -5.0
        self.rewards.dof_torques_l2.weight = -2.5e-5
        self.rewards.feet_air_time.weight = 0.5
        # change terrain to flat
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None
        # no height scan
        self.scene.height_scanner = None
        self.observations.policy.height_scan = None
        # no terrain curriculum
        self.curriculum.terrain_levels = None


class AnymalCFlatEnvCfg_PLAY(AnymalCFlatEnvCfg):
    def __post_init__(self) -> None:
        # post init of parent
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing event
        self.events.base_external_force_torque = None
        self.events.push_robot = None
