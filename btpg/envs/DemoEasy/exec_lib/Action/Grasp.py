from btpg.envs.DemoEasy.exec_lib._base.DemoAction import DemoAction

class Grasp(DemoAction):
    can_be_expanded = True
    num_args = 1
    valid_args = DemoAction.CanGrasp

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def get_info(cls,*arg):
        info = {}
        info["pre"]={"IsHandEmpty()",f"IsNear({arg[0]})"} # 至少有一只手是空闲的
        info["add"]={f"IsHolding({arg[0]})"}

        info["del_set"] = {f"IsHandEmpty()"}
        info["cost"] = 5
        return info


    def change_condition_set(self):
        self.agent.condition_set |= (self.info["add"])
        self.agent.condition_set -= self.info["del_set"]
