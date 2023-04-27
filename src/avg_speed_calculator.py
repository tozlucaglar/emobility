# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:31:34 2023

@author: aglar
"""

import numpy as np
import pandas as pd
import os
import subprocess


def get_repo_root():
    """Get the root directory of the repo."""
    dir_in_repo = os.path.dirname(os.path.abspath('__file__'))  # os.getcwd()
    return subprocess.check_output('git rev-parse --show-toplevel'.split(),
                                   cwd=dir_in_repo,
                                   universal_newlines=True).rstrip()


ROOT_dir = get_repo_root()


#speed_table = pd.read_csv(ROOT_dir + f'./dbs/speed/speed_table.csv', delimiter=";", dtype={"mean": float, "sd": float})

mean_less40 = 20.5
mean_40_65 = 17.5
mean_more65 = 14.8
sd_less40 = 5.2
sd_40_65 = 4.0
sd_more65 = 1.9

#gender
b_male = 0.0491
b_female = 0.0

# activity
b_activity = 0.0
b_work = 0.1071

# gradient
b_neg_grad_1 = np.exp(0.0196)
b_neg_grad_2 = np.exp(0.0312)
b_neg_grad_3 = np.exp(0.0779)
b_neg_grad_4 = np.exp(0.1196)
b_neg_grad_5 = np.exp(0.1488)
b_neg_grad_6 = np.exp(0.1861)
b_neg_grad_7 = np.exp(0.1228)
b_neg_grad_9 = np.exp(0.0617)
b_neg_grad_9_plus = np.exp(0.0518)

b_pos_grad_1 = np.exp(0.0)
b_pos_grad_2 = np.exp(-0.0376)
b_pos_grad_3 = np.exp(-0.1299)
b_pos_grad_4 = np.exp(-0.1951)
b_pos_grad_5 = np.exp(-0.2669)
b_pos_grad_6 = np.exp(-0.3034)
b_pos_grad_7 = np.exp(-0.3854)
b_pos_grad_9 = np.exp(-0.3949)
b_pos_grad_9_plus = np.exp(-0.4267)



def age_condition(row):
    if row["Age"] <= 40:
        return np.random.normal(mean_less40, sd_less40, 1)
    elif row["Age"] >= 65:
        return np.random.normal(mean_more65, sd_more65, 1)
    else:
        return np.random.normal(mean_40_65, sd_40_65, 1)


def main(df_OTP):
    df_person = pd.read_csv(ROOT_dir+f'./dbs/agents/person.csv')
    df_od_pairs_vg = pd.merge(df_OTP, df_person[["PId", "Age", "Gender"]], left_on="person", right_on="PId", how="left")
    df_od_pairs_vg.drop('PId', axis=1, inplace=True)
    # df_OTP_personal_characteristics.to_csv(f'./dbs/agents/od_pairs_vg_all_attributes.csv', index=False)


    df_person_cycling_speed = df_od_pairs_vg[["person", "Age", "Gender"]].groupby(["person", "Age", "Gender"]).first()
    df_person_cycling_speed.reset_index(inplace=True)

    #initialize average cycling speed for person
    df_person_cycling_speed["cycling_speed"] = 0

    # for each agent, draw a speed value from the normal distribution by age
    df_person_cycling_speed["cycling_speed"] = df_person_cycling_speed.apply(lambda row: age_condition(row)[0], axis=1)

    # multiply the speed by the gender constraint
    df_person_cycling_speed["cycling_speed"] = df_person_cycling_speed.apply(
        lambda row: row["cycling_speed"] * np.exp(b_male) if row["Gender"] == "Male" else row["cycling_speed"], axis=1)

    df_person_cycling_speed = pd.merge(df_od_pairs_vg, df_person_cycling_speed[["person", "cycling_speed"]],
                                       on="person", how="left")

    df_person_cycling_speed = df_person_cycling_speed[["person", "act_purpose", "cycling_speed"]].groupby(
        ["person", "act_purpose"]).first()
    df_person_cycling_speed.reset_index(inplace=True)


    # multiply the speed by the purpose constraint
    df_person_cycling_speed["cycling_speed"] = df_person_cycling_speed.apply(
        lambda row: row["cycling_speed"] * np.exp(b_work) if row["act_purpose"] == "work" else row["cycling_speed"],
        axis=1)

    df_od_pairs_vg = pd.merge(df_od_pairs_vg, df_person_cycling_speed[["person", "cycling_speed", "act_purpose"]],
                               on=["person", "act_purpose"], how="left")


    # truncate tails by min and max values

    df_od_pairs_vg["cycling_speed"][(df_od_pairs_vg["cycling_speed"] > 31) & (df_od_pairs_vg["Age"] <= 40)] = 31
    df_od_pairs_vg["cycling_speed"][(df_od_pairs_vg["cycling_speed"] < 12.9) & (df_od_pairs_vg["Age"] <= 40)] = 12.9

    df_od_pairs_vg["cycling_speed"][
        (df_od_pairs_vg["cycling_speed"] > 25.3) & (df_od_pairs_vg["Age"] < 65) & (df_od_pairs_vg["Age"] > 40)] = 25.3
    df_od_pairs_vg["cycling_speed"][
        (df_od_pairs_vg["cycling_speed"] < 12.2) & (df_od_pairs_vg["Age"] < 65) & (df_od_pairs_vg["Age"] > 40)] = 12.2

    df_od_pairs_vg["cycling_speed"][(df_od_pairs_vg["cycling_speed"] > 18.6) & (df_od_pairs_vg["Age"] >= 65)] = 18.6
    df_od_pairs_vg["cycling_speed"][(df_od_pairs_vg["cycling_speed"] < 12.2) & (df_od_pairs_vg["Age"] >= 65)] = 12.2



    return df_od_pairs_vg




