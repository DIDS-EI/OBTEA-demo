
We have uploaded the slim version at `https://github.com/DIDS-EI/OBTEA-demo`. If you want to generate a BT file for a custom task, you can refer to `OBTEA-demo/test_demo/run_demo_task.py`.
1. First, create your own environment under `OBTEA-demo\btpg\envs`, such as `DemoEasy`. The key is to establish the action classes and condition classes in `exec_lib`. Pay attention to the preconditions (`pre`), additions (`add`), deletions (`del`), and their optional parameters for each action.
2. In the main function `run_demo_task.py`, provide the path to `exec_lib` to import `behavior_lib`.
3. Before running the BT algorithm, specify the goal and the current state `cur_cond_set`.
4. To draw the BT, you need the `.btml` file and the imported `behavior_lib`.
We will continue to update and maintain this project, so stay tuned!



我们上传了精简版的  https://github.com/DIDS-EI/OBTEA-demo ，如果想 generating BT file for custom task，你可以参考 `OBTEA-demo/test_demo/run_demo_task.py` 。
1. 首先在 `OBTEA-demo\btpg\envs` 下建立自己的环境，如 `DemoEasy`，其中的关键是建立 `exec_lib` 中的 动作类和条件类，动作类需要关注每个动作的 pre, add, del 以及它们的可选参数。
2. 在主函数 `run_demo_task.py` 需要给出 `exec_lib` 的路径来导入 `behavior_lib`
3. 跑 BT 算法前，需要给定 `goal` 和 当前状态 `cur_cond_set`
4. 画出 BT，需要 `btml` 以及 导入的` behavior_lib`

我们还会持续更新和维护，敬请期待！