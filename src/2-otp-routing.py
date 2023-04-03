import os, sys
import subprocess
import pandas as pd
import multiprocessing as mp
from p_tqdm import p_map
import time


def get_repo_root():
    """Get the root directory of the repo."""
    dir_in_repo = os.path.dirname(os.path.abspath('__file__'))  # os.getcwd()
    return subprocess.check_output('git rev-parse --show-toplevel'.split(),
                                   cwd=dir_in_repo,
                                   universal_newlines=True).rstrip()


ROOT_dir = get_repo_root()
sys.path.append(ROOT_dir)
sys.path.insert(0, ROOT_dir + '/lib')

import lib.routing as routing


if __name__ == "__main__":
    region = 'vg'
    # Parallelize the routing requests
    print('Parallelize the routing requests...')
    df_od = pd.read_csv(ROOT_dir + f'/example/od_pairs_{region}.csv')
    def parallel_process(x):
        folder2save = ROOT_dir + f'/example/output_1000/'
        mode = "BICYCLE,WALK"
        walkdistance = 300
        region = 'vg_1000'
        bikeSpeed = 7
        routing.requesting_origin_batch(data=x, walkdistance=walkdistance,
                                        folder2save=folder2save, region=region, mode=mode, bikeSpeed=bikeSpeed)
    p_map(parallel_process, [x for _, x in df_od.groupby("origin")])





