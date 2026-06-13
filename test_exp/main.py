"""Interactive demo for LLM-OBTEA behavior tree planning (VirtualHome).

Run from the repository root or from ``test_exp/``::

    python test_exp/main.py

The script lets you pick a task (easy / medium / hard), plans an optimal
behavior tree with the HOBTEA algorithm, prints it, renders the tree to the
unified ``output/`` directory and then simulates the execution.
"""

import time

from btpg import BehaviorTree
from btpg.algos.bt_planning.main_interface import BTExpInterface
from btpg.algos.llm_client.tools import goal_transfer_str
from btpg.utils.path import get_output_path
from btpg.utils.tools import setup_environment


def build_easy_task():
    """Put bananas into the fridge and keep the fridge closed."""
    goal_str = "IsIn_bananas_fridge & IsClose_fridge"
    key_predicates = ["Walk", "RightGrab", "Open", "PutIn", "Close"]
    key_objects = ["bananas", "fridge"]
    priority_act_ls = [
        "Walk_bananas",
        "RightGrab_bananas",
        "Walk_fridge",
        "Open_fridge",
        "RightPutIn_bananas_fridge",
        "Close_fridge",
    ]
    return goal_str, key_objects, key_predicates, priority_act_ls


def build_medium_task():
    """Put chicken and pound cake into the stove, then close and switch it on."""
    goal_str = ("IsIn_chicken_stove & IsIn_poundcake_stove "
                "& IsClose_stove & IsSwitchedOn_stove")
    key_objects = ["chicken", "poundcake", "stove"]
    key_predicates = ["Walk", "RightGrab", "RightPutIn", "LeftGrab",
                      "LeftPutIn", "SwitchOn", "Close", "Open"]
    priority_act_ls = [
        "Walk(chicken)",
        "RightGrab(chicken)",
        "Walk(stove)",
        "RightPutIn(chicken, stove)",
        "Walk(poundcake)",
        "LeftGrab(poundcake)",
        "Walk(stove)",
        "LeftPutIn(poundcake, stove)",
        "Walk(stove)",
        "Close(stove)",
        "SwitchOn(stove)",
    ]
    return goal_str, key_objects, key_predicates, priority_act_ls


def build_hard_task():
    """Tidy up: clothes on the bed, book on the desk, shaker in the cabinet."""
    goal_str = ("IsOn_clothespile_bed & IsOn_book_desk "
                "& IsIn_condimentshaker_kitchencabinet & IsClose_kitchencabinet")
    key_objects = ["clothespile", "bed", "book", "desk",
                   "condimentshaker", "kitchencabinet"]
    key_predicates = ["Walk", "LeftGrab", "LeftPut", "RightGrab",
                      "RightPut", "Open", "Close"]
    priority_act_ls = [
        "Walk(clothespile)",
        "LeftGrab(clothespile)",
        "Walk(bed)",
        "LeftPut(clothespile,bed)",
        "Walk(book)",
        "RightGrab(book)",
        "Walk(desk)",
        "RightPut(book,desk)",
        "Walk(condimentshaker)",
        "RightGrab(condimentshaker)",
        "Walk(kitchencabinet)",
        "Open(kitchencabinet)",
        "RightPutIn(condimentshaker,kitchencabinet)",
        "Close(kitchencabinet)",
    ]
    return goal_str, key_objects, key_predicates, priority_act_ls


DEMOS = {
    1: {
        "name": "Easy demo",
        "description": "Simple task planning demo.",
        "task": "请将香蕉放入冰箱，并确保冰箱门关闭",
        "builder": build_easy_task,
    },
    2: {
        "name": "Medium demo",
        "description": "Medium difficulty task planning demo.",
        "task": "将鸡肉和磅蛋糕放入烤箱，并确保烤炉门关闭以及烤炉开启",
        "builder": build_medium_task,
    },
    3: {
        "name": "Hard demo",
        "description": "Hard task planning demo.",
        "task": "请将衣物堆叠在床上，将书籍放在桌子上，将调料瓶放入厨房橱柜中，并确保橱柜门关闭",
        "builder": build_hard_task,
    },
}


def select_demo():
    """Prompt the user to choose a demo and return its task definition."""
    print("请选择一个演示：")
    for key, value in DEMOS.items():
        print(f"{key}. {value['name']} - {value['description']} - {value['task']}.")

    try:
        demo_number = int(input("请输入演示编号："))
    except (ValueError, EOFError):
        demo_number = 1
    print("\n")

    if demo_number not in DEMOS:
        print("无效的演示编号。为您选择了 1-easy。")
        demo_number = 1
    return DEMOS[demo_number]["builder"]()


def main():
    scene = "VH"
    env, cur_cond_set = setup_environment(scene)

    goal_str, key_objects, key_predicates, priority_act_ls = select_demo()
    print("调用大语言模型理解指令...")
    print(f"在数据中找到已调用的解析结果! "
          f"\n Goal: {goal_str}"
          f"\n Key Objects: {key_objects}"
          f"\n Key Predicates: {key_predicates}"
          f"\n Priority Actions: {priority_act_ls}")

    print("\n=========== Run Optimal Behavior for BT ============")
    algo = BTExpInterface(env.behavior_lib, cur_cond_set=cur_cond_set,
                          priority_act_ls=priority_act_ls,
                          key_predicates=key_predicates,
                          key_objects=key_objects,
                          selected_algorithm="hobtea",
                          mode="small-predicate-objs",
                          act_tree_verbose=False, time_limit=10,
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
    print("============ End  Optimal Behavior for BT ============\n")

    # Visualization: write all artifacts into the unified output directory.
    print("\n=========== BT Visualization ============")
    output_dir = get_output_path()
    btml_path = f"{output_dir}/tree.btml"
    with open(btml_path, "w") as file:
        file.write(ptml_string)

    bt = BehaviorTree(btml_path, env.behavior_lib)
    bt.print()
    bt.draw(target_directory=output_dir)
    print(f"BT artifacts saved to: {output_dir}")
    print("============ End BT Visualization ============\n")

    goal = goal_set[0]
    print(f"\ngoal: {goal}")
    algo.execute_bt(goal_set[0], cur_cond_set, verbose=True)


if __name__ == "__main__":
    main()
