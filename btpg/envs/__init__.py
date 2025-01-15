
env_map = {}

from btpg.envs.VirtualHome.envs.vh_env import VHEnvTest



vh_env_map = {
    "VH": VHEnvTest,
}

env_map.update(vh_env_map)