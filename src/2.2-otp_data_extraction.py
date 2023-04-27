import pandas as pd
import json
import os, sys
import multiprocessing
import time
import numpy as np
import pickle
from trip_duration_calculator import duration_calculator_bygradient



os.chdir(r'C:\emobility')

filepath = r'.\dbs\output'


def data_extractor(file, count ):
    routes_list = []

    if file.endswith(".json"):
        fname = os.path.join(filepath, file)
        for line in open(fname):
            record = json.loads(line)
            if record["duration"] != 0:
                legElevation = record['legs'][0]['legElevation'].split(',')
                run =[float(x) - float(legElevation[i - 2]) for i, x in enumerate(legElevation)][2::2]
                rise = [round(float(x) - float(legElevation[i - 2]), 2) for i, x in enumerate(legElevation)][3::2]
                percentSlope = [ (x[0]/ x[1] )* 100 if (x[0] != 0) and (x[1] > 0) else 0  for x in zip(rise, run)]
                cycling_duration = duration_calculator_bygradient(record['cycling_speed'], percentSlope, run)

                routes_list.append((record['person'], record['act_id'], 'yes', record['walkDistance'], record['duration'], record['cycling_speed'], cycling_duration ))

            else:
                routes_list.append((record['person'], record['act_id'], 'no', 0, 0, 0, 0))


        df_routes = pd.DataFrame(routes_list, columns=['person', 'act_id', 'complete', 'total_dist', 'OTP_duration', 'cycling_speed', 'duration'])
        df_routes.to_pickle(r'C:\emobility\dbs\output\file_'+str(count)+'.pkl')

        print(count)

        #break


if __name__ == "__main__":
    start_time = time.time()
    folder_list = os.listdir(filepath)
    pool = multiprocessing.Pool()
    processes = [pool.apply_async(data_extractor, args=(folder_list[i], i)) for i in range(0, len(folder_list))]
    [p.get() for p in processes]

    finish_time = time.perf_counter()

    print("--- %s seconds ---" % (time.time() - start_time))




