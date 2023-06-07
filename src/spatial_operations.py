import geopandas as gpd

import os
import subprocess


def get_repo_root():
    """Get the root directory of the repo."""
    dir_in_repo = os.path.dirname(os.path.abspath('__file__'))  # os.getcwd()
    return subprocess.check_output('git rev-parse --show-toplevel'.split(),
                                   cwd=dir_in_repo,
                                   universal_newlines=True).rstrip()


ROOT_dir = get_repo_root()


#road_network = gpd.read_file(ROOT_dir+f'./dbs/emission/road/5_road_network_with_slope.shp')

#road_network = road_network[['link_id','geometry']]


# DeSO = gpd.read_file(ROOT_dir+f'./dbs/emission/deso_statistik_shp/Fordon_region.shp')
#
# DeSO = DeSO.to_crs(road_network.crs)
#
# road_network_deso = road_network.sjoin(DeSO[['Deso','geometry']], how="left")
#
# road_network_deso.to_file(ROOT_dir+f'./dbs/emission/road_network_deso.shp')

def spatial_join(main_part, join_part ):
    main_part = main_part.sjoin(join_part, how="left")
    return main_part

