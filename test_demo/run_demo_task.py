"""Minimal example: generate a behavior tree for a custom task.

This is the recommended starting point for building a BT for your own task:
just provide the path to an ``exec_lib`` (action / condition library), the goal
and the current condition set, then plan, render and execute the tree.

    python test_demo/run_demo_task.py
"""

import time

from btpg import BehaviorTree
from btpg.algos.bt_planning.main_interface import BTExpInterface
from btpg.algos.llm_client.tools import goal_transfer_str
from btpg.behavior_tree.behavior_libs import ExecBehaviorLibrary
from btpg.utils.path import get_output_path
from btpg.utils.tools import ROOT_PATH

OUTPUT_NAME = "demo_behavior_tree"


def main():
    behavior_lib_path = f"{ROOT_PATH}/envs/DemoEasy/exec_lib"
    behavior_lib = ExecBehaviorLibrary(behavior_lib_path)

    goal_str = "IsHolding_apple"
    cur_cond_set = {"IsHandEmpty()"}

    print("\n=========== Run Optimal Behavior for BT ============")
    algo = BTExpInterface(behavior_lib, cur_cond_set=cur_cond_set,
                          selected_algorithm="obtea")

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
    print("============ End  Optimal Behavior for BT ============\n")

    # Visualization: write all artifacts into the unified output directory.
    print("\n=========== BT Visualization ============")
    output_dir = get_output_path()
    btml_path = f"{output_dir}/{OUTPUT_NAME}.btml"
    with open(btml_path, "w") as file:
        file.write(ptml_string)

    bt = BehaviorTree(btml_path, behavior_lib)
    bt.print()
    bt.draw(file_name=OUTPUT_NAME, target_directory=output_dir)
    print(f"BT artifacts saved to: {output_dir}")
    print("============ End BT Visualization ============\n")

    goal = goal_set[0]
    print(f"\ngoal: {goal}")
    algo.execute_bt(goal_set[0], cur_cond_set, verbose=True)


if __name__ == "__main__":
    main()
