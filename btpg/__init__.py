# from btpg.behavior_tree.behavior_trees import BehaviorTree,ExecBehaviorTree

from btpg.behavior_tree.behavior_trees import BehaviorTree


from btpg.behavior_tree.behavior_libs import ExecBehaviorLibrary

from btpg.utils import ROOT_PATH



def make(env_name):
    from btpg.envs import env_map
    return env_map[env_name]()