import numpy as np
import pandas as pd
import os, sys
import warnings
import geopandas as gpd

warnings.filterwarnings("ignore")

filepath = r'C:\emobility\dbs\output\sensitivity'
file_list = os.listdir(filepath)

print(file_list)

Reduction_results= []

ReductionVG_results= []


count=0

for file in file_list:
    count += 1
    print(count)

    replacement_bybike = pd.read_pickle(f"C:/emobility/dbs/output/sensitivity/"+file)
    #
    #
    #
    emission_bylink = pd.read_pickle(f'C:/emobility/dbs/output/emission_bylink.pkl')
    # #
    # #
    replacement_bybike['changed_act_id'] = replacement_bybike.groupby('person').cumcount()
    # #
    emission_bylink = pd.merge(emission_bylink, replacement_bybike[["person",'changed_act_id','tour_replacement']], left_on= ["person",'act_id'], right_on= ["person",'changed_act_id'], how="left")
    # #
    # # #reduction from all cars
    emission_bylink_bike = emission_bylink[emission_bylink.tour_replacement==True]

    reduction = emission_bylink_bike['link_emission'].sum()
    total = emission_bylink['link_emission'].sum()
    print('reduction share_'+file, reduction/total)
    Reduction = reduction/total
    Reduction_results.append(Reduction)
    # #
    # #
    emission_bylink['num_Deso']= emission_bylink['Deso'].str.len()
    # # #%%
    emission_bylink['link_emission']= emission_bylink['link_emission'].div(emission_bylink['num_Deso'])
    # # #%%
    emission_bylink= emission_bylink.loc[emission_bylink.index.repeat(emission_bylink.num_Deso)]
    # # #%%
    emission_bylink['num_Deso']= emission_bylink.groupby(['person','seq']).cumcount()
    # #
    def link_todeso(row):
        if len(row['Deso']) == 1:
            Deso = row['Deso'][0]
        else:
            Deso = row['Deso'][row['num_Deso']]
        return Deso
    # #
    # #
    emission_bylink['Deso'] = emission_bylink.apply(lambda row: link_todeso(row), axis=1)
    # # # %%
    emission_bydeso = emission_bylink.groupby(['Deso'])['link_emission'].sum().reset_index()
    # #


    DeSO = gpd.read_file(f'C:/emobility/dbs/emission/deso_statistik_shp/Fordon_region.shp')
    DeSO = DeSO[['Deso','geometry']]
    # # #%%
    gdf=DeSO.merge(emission_bydeso,on="Deso")
    gdf= gdf[gdf['Deso'].str[:2]=='14']
    # #
    # # #%%
    #print('the total emission within VG: ', gdf.link_emission.sum())
    emission_bylink_reduction = emission_bylink[emission_bylink.tour_replacement==True]
    emission_bylink_reduction = emission_bylink_reduction.groupby(['Deso'])['link_emission'].sum().reset_index()
    # #
    # #
    # # #%%
    gdf_reduction = DeSO.merge(emission_bylink_reduction, on="Deso")
    gdf_reduction = gdf_reduction[gdf_reduction['Deso'].str[:2] == '14']
    # #
    # #
    #print('the reduction in emission within VG: ', gdf_reduction.link_emission.sum())
    # #
    # # #reduction from all cars

    reduction = gdf_reduction.link_emission.sum()
    total =gdf.link_emission.sum()
    print('reduction share within_'+file,reduction/total)
    Reduction = reduction/total
    ReductionVG_results.append(Reduction)



print(file_list)

print('all reduction share', Reduction_results)
#
print('all reduction share within', ReductionVG_results)
