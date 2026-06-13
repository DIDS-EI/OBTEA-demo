"""VirtualHome experiment - EASY goal.

Goal: put bananas into the fridge and keep the fridge closed.

    python test_exp/main_VH_easy.py
"""

import time

from btpg import BehaviorTree
from btpg.algos.bt_planning.main_interface import BTExpInterface
from btpg.algos.llm_client.tools import goal_transfer_str
from btpg.utils.path import get_output_path
from btpg.utils.tools import setup_environment

SCENE = "VH"
OUTPUT_NAME = "behavior_tree_vh_easy"

goal_str = "IsIn_bananas_fridge & IsClose_fridge"
key_objects = ["bananas", "fridge"]
key_predicates = ["Walk", "RightGrab", "Open", "PutIn", "Close"]
priority_act_ls = [
    "Walk_bananas",
    "RightGrab_bananas",
    "Walk_fridge",
    "Open_fridge",
    "RightPutIn_bananas_fridge",
    "Close_fridge",
]


def main():
    env, cur_cond_set = setup_environment(SCENE)

    print("goal_str:", goal_str)
    algo = BTExpInterface(env.behavior_lib, cur_cond_set=cur_cond_set,
                          priority_act_ls=priority_act_ls,
                          key_predicates=key_predicates,
                          key_objects=key_objects,
                          selected_algorithm="hobtea",
                          mode="small-predicate-objs",
                          act_tree_verbose=False, time_limit=15,
                          heuristic_choice=0, output_just_best=True)

    goal_set = goal_transfer_str(goal_str)

    start_time = time.time()
    algo.process(goal_set)
    planning_time_total = time.time() - start_time

    time_limit_exceeded = algo.algo.time_limit_exceeded
    ptml_string, cost, expanded_num = algo.post_process()
    error, state, act_num, current_cost, record_act_ls, ticks = \
        algo.execute_bt(goal_set[0], cur_cond_set, verbose=False)

    print(f"\x1b[32m Goal:{goal_str} \n Executed {act_num} action steps\x1b[0m",
          "\x1b[31mERROR\x1b[0m" if error else "",
          "\x1b[31mTIMEOUT\x1b[0m" if time_limit_exceeded else "")
    print("current_cost:", current_cost,
          "expanded_num:", expanded_num,
          "planning_time_total:", planning_time_total)

    # Visualization: write all artifacts into the unified output directory.
    output_dir = get_output_path()
    btml_path = f"{output_dir}/{OUTPUT_NAME}.btml"
    with open(btml_path, "w") as file:
        file.write(ptml_string)

    bt = BehaviorTree(btml_path, env.behavior_lib)
    bt.draw(file_name=OUTPUT_NAME, target_directory=output_dir)
    print(f"BT artifacts saved to: {output_dir}")

    goal = goal_set[0]
    print(f"goal: {goal}")
    algo.execute_bt(goal_set[0], cur_cond_set, verbose=True)


if __name__ == "__main__":
    main()
