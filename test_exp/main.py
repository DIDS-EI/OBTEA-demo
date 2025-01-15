import time

from btpg.algos.llm_client.tools import goal_transfer_str
from btpg.algos.bt_planning.main_interface import BTExpInterface
from btpg.utils.tools import *



def run_easy_demo():
    print("运行 Easy 版本演示...")
    # 在这里添加 Easy 版本的代码逻辑
    goal_str = 'IsIn_bananas_fridge & IsClose_fridge'
    key_predicates = ["Walk", "RightGrab", "Open", "PutIn", "Close"]
    key_objects = ["bananas", "fridge"]
    priority_act_ls = [
        "Walk_bananas",
        "RightGrab_bananas",
        "Walk_fridge",
        "Open_fridge",
        "RightPutIn_bananas_fridge",
        "Close_fridge"
    ]
    # 演示 Easy 版本的逻辑
    return goal_str, key_objects, key_predicates, priority_act_ls

def run_medium_demo():
    print("运行 Medium 版本演示...")
    # 在这里添加 Medium 版本的代码逻辑
    goal_str = 'IsIn_chicken_stove & IsIn_poundcake_stove & IsClose_stove & IsSwitchedOn_stove'
    key_objects = ["chicken", "poundcake", "stove"]
    key_predicates = ["Walk", "RightGrab", "RightPutIn", "LeftGrab", "LeftPutIn", "SwitchOn", "Close", "Open"]
    priority_act_ls = [
        "Walk(chicken)",
        "RightGrab(chicken)",
        "Walk(stove)",
        "RightPutIn(chicken, stove)",
        "Walk(poundcake)",
        "LeftGrab(poundcake)",
        "Walk(stove)",
        "LeftPutIn(poundcake, stove)",
        "Walk(clothespile)",
        "RightGrab(clothespile)",
        "Walk(bathroomcounter)",
        "RightPutOn(clothespile, bathroomcounter)",
        "Walk(stove)",
        "Close(stove)",
        "SwitchOn(stove)"
    ]
    # 演示 Medium 版本的逻辑
    return goal_str, key_objects, key_predicates, priority_act_ls

def run_hard_demo():
    print("运行 Hard 版本演示...")
    # 在这里添加 Hard 版本的代码逻辑
    goal_str = "(IsOn_clothespile_bed & IsOn_book_desk & IsIn_condimentshaker_kitchencabinet & IsClose_kitchencabinet )"
    key_objects = ["clothespile", "bed", "book", "desk", "condimentshaker", "kitchencabinet"]
    key_predicates = ["Walk", "LeftGrab", "LeftPut", "RightGrab", "RightPut", "Open", "Close"]
    priority_act_ls = [
        'Walk(clothespile)',
        'LeftGrab(clothespile)',
        'Walk(bed)',
        'LeftPut(clothespile,bed)',

        'Walk(book)',
        'RightGrab(book)',
        'Walk(desk)',
        'RightPut(book,desk)',

        'Walk(condimentshaker)',
        'RightGrab(condimentshaker)',
        'Walk(kitchencabinet)',
        "Open(kitchencabinet)"
        'RightPutIn(condimentshaker,kitchencabinet)',
        "Close(kitchencabinet)"
    ]
    # 演示 Hard 版本的逻辑
    return goal_str, key_objects, key_predicates, priority_act_ls

# 定义演示字典
demos = {
    1: {
        'name': 'Easy test_demo',
        'description': '简单的任务规划演示。',
        "tasks": "请将香蕉放入冰箱，并确保冰箱门关闭" ,
        'Goal': 'IsIn_bananas_fridge & IsClose_fridge',
        'function': run_easy_demo
    },
    2: {
        'name': 'Medium test_demo',
        'description': '中等难度的任务规划演示。',
        'tasks': '将鸡肉和磅蛋糕放入烤箱，并确保烤炉门关闭以及烤炉开启' ,
        'Goal': 'IsIn_chicken_stove & IsIn_poundcake_stove & IsClose_stove & IsSwitchedOn_stove',
        'function': run_medium_demo
    },
    3: {
        'name': 'Hard test_demo',
        'description': '困难的任务规划演示。',
        'tasks': '请将衣物堆叠在床上，将书籍放在桌子上，将调料瓶放入厨房橱柜中，并确保橱柜门关闭',
        'Goal': '(IsOn_clothespile_bed & IsOn_book_desk & IsIn_condimentshaker_kitchencabinet & IsClose_kitchencabinet)',
        'function': run_hard_demo
    }
}


scene = "VH"
env, cur_cond_set = setup_environment(scene)

# 用户选择 test_demo
print("请选择一个演示：")
for key, value in demos.items():
    print(f"{key}. {value['name']} - {value['description']} - {value['tasks']}.")

demo_number = int(input("请输入演示编号："))
print("\n")
if demo_number in demos:
    goal_str, key_objects, key_predicates, priority_act_ls = demos[demo_number]['function']()
    print("调用大语言模型理解指令...")
    print(f"在数据中找到已调用的解析结果! "
          f"\n Goal: {goal_str}"
          f"\n Key Objects: {key_objects}"
          f"\n Key Predicates: {key_predicates}",
          f"\n Priority Actions: {priority_act_ls}")
else:
    print("无效的演示编号。为您选择了 1-easy。")
    goal_str, key_objects, key_predicates, priority_act_ls = demos[1]['function']()


print("\n=========== Run Optimal Behavior for BT ============")
algo = BTExpInterface(env.behavior_lib, cur_cond_set=cur_cond_set,
                      priority_act_ls=priority_act_ls, key_predicates=key_predicates,
                      key_objects=key_objects,
                      selected_algorithm="hobtea", mode="small-predicate-objs",
                      act_tree_verbose=False, time_limit=10,
                      heuristic_choice=0,output_just_best=True)

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
bt = BehaviorTree(file_name + ".btml", env.behavior_lib)
bt.print()
bt.draw()
print("============ End BT Visualization ============\n")

goal = goal_transfer_str(goal_str)[0]
print(f"\ngoal: {goal}")
error, state, act_num, current_cost, record_act_ls,ticks = algo.execute_bt(goal_set[0], cur_cond_set, verbose=True)

'''
# 用户选择是否进行仿真演示
print("请选择一个演示：")
print("1. 运行仿真演示")
print("2. 不运行仿真演示")
user_choice = input("请输入您的选择（1 或 2）：")


if user_choice == '1':
    try:
        print("尝试启动仿真器...")
        env.launch_simulator()
        env.agents[0].bind_bt(bt)
        env.reset()
        is_finished = False
        while not is_finished:
            is_finished = env.step()
            if goal <= env.agents[0].condition_set:
                is_finished = True
        env.close()
    except Exception as e:
        print("暂时无法打开仿真器。")
        print("错误信息：", e)
else:
    print("不运行仿真演示。")
'''
