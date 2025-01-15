from btpg.envs.DemoEasy.exec_lib._base.DemoAction import DemoAction

class Walk(DemoAction):
    can_be_expanded = True
    num_args = 1
    valid_args = DemoAction.AllObject

    def __init__(self, *args):
        super().__init__(*args)
        self.target_obj = self.args[0]

    @classmethod
    def get_info(cls,*arg):
        info = {}
        info["pre"]=set()
        info["add"]={f"IsNear({arg[0]})"}
        info["del_set"] = {f'IsNear({place})' for place in cls.valid_args if place != arg[0]}
        info["cost"] = 15
        return info

    def change_condition_set(self):
        self.agent.condition_set |= (self.info["add"]) #self.agent.condition_set.update(self.info["add"])
        self.agent.condition_set -= self.info["del_set"] #self.agent.condition_set.difference_update(self.info["del_set"])
