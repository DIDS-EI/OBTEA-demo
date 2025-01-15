import time

from btpg.behavior_tree.behavior_libs import ExecBehaviorLibrary
from btpg.algos.llm_client.tools import goal_transfer_str
from btpg.algos.bt_planning.main_interface import BTExpInterface
from btpg.utils.tools import ROOT_PATH



behavior_lib_path = f"{ROOT_PATH}/envs/DemoEasy/exec_lib"
behavior_lib = ExecBehaviorLibrary(behavior_lib_path)

goal_str = "IsHolding_apple"
cur_cond_set = {'IsHandEmpty()'}


print("\n=========== Run Optimal Behavior for BT ============")
algo = BTExpInterface(behavior_lib, cur_cond_set=cur_cond_set,
                      selected_algorithm="obtea")

goal_set = goal_transfer_str(goal_str)

start_time = time.time()
algo.process(goal_set)
end_time = time.time()
planning_time_total = end_time - start_time

time_limit_exceeded = algo.algo.time_limit_exceeded

ptml_string, cost, expanded_num = algo.post_process()
error, state, act_num, current_cost, record_act_ls,ticks = algo.execute_bt(goal_set[0], cur_cond_set, verbose=False)

print(f"\x1b[32m Goal:{goal_str} \n Executed {act_num} action steps\x1b[0m",
      "\x1b[31mERROR\x1b[0m" if error else "",
      "\x1b[31mTIMEOUT\x1b[0m" if time_limit_exceeded else "")
print("current_cost:", current_cost, "expanded_num:", expanded_num, "planning_time_total:", planning_time_total)
print("============ End  Optimal Behavior for BT ============\n")

# visualization
print("\n=========== BT Visualization ============")
file_name = "tree"
file_path = f'./{file_name}.btml'
with open(file_path, 'w') as file:
    file.write(ptml_string)
# read and execute
from btpg import BehaviorTree
bt = BehaviorTree(file_name + ".btml", behavior_lib)
bt.print()
bt.draw()
print("============ End BT Visualization ============\n")

goal = goal_transfer_str(goal_str)[0]
print(f"\ngoal: {goal}")
error, state, act_num, current_cost, record_act_ls,ticks = algo.execute_bt(goal_set[0], cur_cond_set, verbose=True)

