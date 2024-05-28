import numpy as np
import pandas as pd
import os

import warnings

warnings.filterwarnings("ignore")

# Define the values to iterate for each parameter
parameter_values = {
    'T_max_trip_dist': [21000, 25500, 30000, 34500, 39000],
    'T_activity_time_dividing': [0.21, 0.255, 0.3, 0.345, 0.39],
    'T_daily_max_trip_dist': [56000, 68000, 80000, 92000, 104000],
    'T_max_increase_in_daily_travel_time': [3780, 4590, 5400, 6210, 7020]
}

# Initial values for each parameter
initial_values = {
    'T_max_trip_dist': 30000,
    'T_activity_time_dividing': 0.3,
    'T_daily_max_trip_dist': 80000,
    'T_max_increase_in_daily_travel_time': 5400
}



# File handling setup
filepath = r'C:\emobility\dbs\output'
file_list = os.listdir(filepath)

df_routes = []

for file in file_list:
    if file.startswith('file'):
        df_route = pd.read_pickle(os.path.join(filepath, file))
        df_routes.append(df_route)

df_routes = pd.concat(df_routes, ignore_index=True).drop_duplicates(subset=['person', 'act_id'], keep='first')


results = []


# Loop over each parameter
for parameter, values in parameter_values.items():
    for value in values:
        print(f"{parameter} Variable: {value}")

        # Set parameters with one variable and others fixed
        T_max_trip_dist = value if parameter == 'T_max_trip_dist' else initial_values['T_max_trip_dist']
        T_activity_time_dividing = value if parameter == 'T_activity_time_dividing' else initial_values[
            'T_activity_time_dividing']
        T_daily_max_trip_dist = value if parameter == 'T_daily_max_trip_dist' else initial_values[
            'T_daily_max_trip_dist']
        T_max_increase_in_daily_travel_time = value if parameter == 'T_max_increase_in_daily_travel_time' else \
        initial_values['T_max_increase_in_daily_travel_time']

        # Load activity data
        df_act = pd.read_csv(r'C:\emobility\dbs\agents\1_activity_plans.csv')


        print(T_max_trip_dist, T_activity_time_dividing, T_daily_max_trip_dist, T_max_increase_in_daily_travel_time)

        # Example generated values (you would replace this with your actual computations)

        person_tripnumber = df_act.groupby(['person'])['act_id'].max().reset_index()

        for trip_number in range(2, max(person_tripnumber.act_id) + 1):
            person_list = person_tripnumber['person'][person_tripnumber.act_id == trip_number]
            bbb = df_act['act_time'][(df_act.person.isin(person_list)) & (df_act.act_id == 0)]
            df_act['act_time'][(df_act.person.isin(person_list)) & (df_act.act_id == trip_number)] = df_act['act_time'][
                                                                                                         (
                                                                                                             df_act.person.isin(
                                                                                                                 person_list)) & (
                                                                                                                     df_act.act_id == trip_number)] + bbb.values

        df_act = df_act.drop(df_act[df_act.act_id == 0].index, axis=0)

        df_act.sort_values(by=['person', 'act_id'], inplace=True, ascending=True)
        df_act['act_id'] = df_act['act_id'] - 1

        df_act = pd.merge(df_act, df_routes, on=['person', 'act_id'], how='left')

        df_act[df_act['cycling_speed'].isna()]

        df_act['complete'][df_act['complete'].isna()] = 'no'
        df_act['duration'][df_act['duration'].isna()] = 0.0

        max_trip_dist = T_max_trip_dist
        activity_time_dividing = T_activity_time_dividing
        daily_max_trip_dist = T_daily_max_trip_dist
        max_increase_in_daily_travel_time = T_max_increase_in_daily_travel_time

        df_act = df_act[df_act['mode'] == 'car']

        df_act['trip_replacement'] = False
        df_act['duration_change'] = df_act['duration'] - df_act['trav_time_min'] * 60
        df_act['act_time_20percent'] = (df_act['act_time'] * 60) * activity_time_dividing


        def trip_replacement(row):
            if row['complete'] == 'yes':
                if row['total_dist'] <= max_trip_dist:
                    if row['duration_change'] <= row['act_time_20percent']:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False


        df_act['trip_replacement'] = df_act.apply(lambda row: trip_replacement(row), axis=1)

        result1 = df_act['trip_replacement'].value_counts() / len(df_act)

        person_tripnumber.rename(columns={'act_id': 'total_trip_number'}, inplace=True)
        df_act = pd.merge(df_act, person_tripnumber, on=['person'], how='left')

        # tour check-in

        df_act['tour_replacement'] = True
        df_act.sort_values(by=['person', 'act_id'], inplace=True)
        df_act.reset_index(inplace=True)
        df_act.drop(['index'], inplace=True, axis=1)

        for index, row in df_act.iterrows():
            if row['act_id'] == 0:
                index_start = index
                trip_replacement = []
                person = row['person']
            trip_replacement.append(row['trip_replacement'])
            if (row['act_purpose'] == 'home') & (np.prod(trip_replacement) == 0):
                df_act['tour_replacement'].iloc[index_start:(index) + 1] = False
                trip_replacement = []
                index_start = index + 1
            elif (row['act_purpose'] == 'home') & (np.prod(trip_replacement) == 1):
                trip_replacement = []
                index_start = index + 1
            elif (row['act_id'] == row['total_trip_number'] - 1) & (np.prod(trip_replacement) == 0):
                df_act['tour_replacement'].iloc[index_start:(index) + 1] = False
                trip_replacement = []
                index_start = index + 1
            elif (row['act_id'] == row['total_trip_number'] - 1) & (np.prod(trip_replacement) == 1):
                trip_replacement = []
                index_start = index + 1

        result2 = df_act['tour_replacement'].value_counts() / len(df_act)


        # daily_max_trip_dist

        daily_cycling_dist = df_act[df_act.tour_replacement == True].groupby('person')['total_dist'].sum().reset_index()
        daily_cycling_dist.rename(columns={'total_dist': 'daily_cycling_dist'}, inplace=True)

        df_act = pd.merge(df_act, daily_cycling_dist, on='person', how='left')
        df_act['daily_cycling_dist'][df_act['daily_cycling_dist'].isna()] = 0.0
        df_act['tour_replacement'][df_act['daily_cycling_dist'] > daily_max_trip_dist] = False

        # print('daily_max_trip_dist: ', df_act['tour_replacement'].value_counts()/len(df_act))

        # max_increase_in_daily_travel_time

        daily_duration_change = df_act[df_act.tour_replacement == True].groupby('person')[
            'duration_change'].sum().reset_index()
        daily_duration_change.rename(columns={'duration_change': 'daily_duration_change'}, inplace=True)

        df_act = pd.merge(df_act, daily_duration_change, on='person', how='left')
        df_act['daily_duration_change'][df_act['daily_duration_change'].isna()] = 0.0
        df_act['tour_replacement'][df_act['daily_duration_change'] > max_increase_in_daily_travel_time] = False

        df_act.to_pickle(
            f"C:/emobility/dbs/output/sensitivity/replacement_"+ parameter + '_' + str(value) + ".pkl")

        result3 = df_act['tour_replacement'].value_counts() / len(df_act)


        # Append results along with parameter info to the list
        results.append({
            'parameter': parameter,
            'value': value,
            'trip_level_thresholds': result1[1],
            'tour_level_thresholds': result2[1],
            'daily_plan_level_thresholds': result3[1]
        })


        print('Processing completed for', parameter, 'with value', value)

    # results_df = pd.DataFrame(results)

    # Display the DataFrame
    # print(results_df)

    # break

# Assuming the processing logic for `df_act` and other variables is similar to your initial code.
results_df = pd.DataFrame(results)

results_df.to_csv(f"C:/emobility/dbs/output/sensitivity/results_replacement.csv", index=False)


# Display the DataFrame
print(results_df)