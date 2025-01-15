from btpg.behavior_tree.base_nodes import Action
from btpg.behavior_tree import Status
from btpg.behavior_tree.behavior_trees import BehaviorTree

class DemoAction(Action):
    can_be_expanded = True
    num_args = 1

    CanGrasp = {"apple", 'wine'}
    CanWalkTo = {"table"}

    AllObject = CanGrasp | CanWalkTo

    @property
    def action_class_name(self):
        return self.__class__.__name__

    def change_condition_set(self):
        pass

    def update(self) -> Status:
        return Status.RUNNING
