from consts import *
import geopandas as gpd
import random
from shapely.geometry import Point


def plot_dots_tract(year):
    """Works for 1980 and earlier."""
    # Load the aggregated census race data for the tristate area block groups
    dfn = load_df(f"demo_{year}/race_agg_{year}_tristate_tract")

    crn = Corners()

    # Get unique GISJOIN identifiers for filtered block groups
    gisjoins = unique(dfn.GISJOIN)

    if year == 1980:
        suffix = ""
    else:
        suffix = "_conflated"
    gdf = gpd.read_file(f"data/geo_{year}/US_tract_{year}{suffix}.shp")
    gdf = gdf[gdf.GISJOIN.isin(gisjoins)]

    dfn['B'] = dfn['B'].round(0).astype(int)
    dfn['H'] = dfn['H'].round(0).astype(int)
    dfn['W'] = dfn['W'].round(0).astype(int)

    merged_gdf = gdf.merge(dfn, on='GISJOIN', how='inner')
    if merged_gdf.crs != 'EPSG:4326':
        merged_gdf = merged_gdf.to_crs('EPSG:4326')

    # Calculate number of dots
    for race in RACES:
        dfn[f'{race}_n_dots'] = (dfn[race] / N_PEOPLE_PER_DOT).round().astype(int)

    # Generate random points within polygons
    def random_points_in_polygon(polygon, num_points):
        points = []
        minx, miny, maxx, maxy = polygon.bounds
        while len(points) < num_points:
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if polygon.contains(pnt):
                points.append(pnt)
        return points

    all_dots = []
    for _, row in merged_gdf.iterrows():
        polygon = row.geometry
        for race in RACES:
            dfn_row = dfn[dfn.GISJOIN == row.GISJOIN].iloc[0]
            num_dots = dfn_row[f'{race}_n_dots']
            if num_dots > 0:
                points = random_points_in_polygon(polygon, num_dots)
                for point in points:
                    all_dots.append({'geometry': point, 'race': race})
    dots_gdf = gpd.GeoDataFrame(all_dots, crs=merged_gdf.crs)

    aspect_ratio = (crn.max_lon - crn.min_lon) / (crn.max_lat - crn.min_lat)
    fig_width = IMAGE_WIDTH
    fig_height = fig_width / aspect_ratio

    # Create figure
    fig = plt.figure(dpi=DPI, figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111)
    ax.set_xlim(crn.min_lon, crn.max_lon)
    ax.set_ylim(crn.min_lat, crn.max_lat)
    ax.set_aspect('equal')  # Preserve geographic proportions
    
    for race in RACES:
        race_dots = dots_gdf[dots_gdf.race == race]
        ax.scatter(race_dots.geometry.x, race_dots.geometry.y, 
                   s=DOT_SIZE / 10_000, color=RACE_COLORS[race], alpha=1.0, 
                   edgecolors='none', rasterized=True)  

    ax.set_axis_off()
    
    plt.savefig(f"images/dots_{year}.png", transparent=True, bbox_inches='tight', 
                pad_inches=0, dpi=DPI)
    plt.close()



def plot_dots_blck_grp(year):
    """Works for 1990 and later."""
    # Load the aggregated census race data for the tristate area block groups
    dfn = load_df(f"demo_{year}/race_agg_{year}_tristate_blck_grp")

    if year == 2000:
        dfn["INTPTLAT"] = dfn["INTPTLAT"] / 1000000
        dfn["INTPTLON"] = dfn["INTPLON"] / 1000000
    
    if year == 1990:
        dfn["INTPTLAT"] = dfn["INTPTLAT"] / 1000000
        dfn["INTPTLON"] = dfn["INTPTLNG"] / 1000000
        
    # Filter census blocks within the rectangle
    lat_col, lon_col = "INTPTLAT", "INTPTLON"

    crn = Corners()

    dfn = dfn[(dfn[lon_col] >= crn.min_lon) & (dfn[lon_col] <= crn.max_lon) & 
              (dfn[lat_col] >= crn.min_lat) & (dfn[lat_col] <= crn.max_lat)]
    dfn.reset_index(drop=True, inplace=True)

    # Get unique GISJOIN identifiers for filtered block groups
    gisjoins = unique(dfn.GISJOIN)

    # Load and filter the GeoDataFrame with census block group geometries
    suffix = ""
    if year == 2000:
        suffix = "_tl10"
    if year == 2010:
        suffix = "_tl20"
        
    gdf = gpd.read_file(f"data/geo_{year}/US_blck_grp_{year}{suffix}.shp")
    gdf = gdf[gdf.GISJOIN.isin(gisjoins)]

    # Adjust for undercounting/overcounting
    if year == 2020:
        dfn['B'] /= (1 - BLACK_UNDERCOUNT_2020)
        dfn['H'] /= (1 - HISP_UNDERCOUNT_2020)
        dfn['W'] /= (1 + WHITE_OVERCOUNT_2020)
    if year == 2010:
        dfn['B'] /= (1 - BLACK_UNDERCOUNT_2010)
        dfn['H'] /= (1 - HISP_UNDERCOUNT_2010)
        dfn['W'] /= (1 + WHITE_OVERCOUNT_2010)

    dfn['B'] = dfn['B'].round(0).astype(int)
    dfn['H'] = dfn['H'].round(0).astype(int)
    dfn['W'] = dfn['W'].round(0).astype(int)

    merged_gdf = gdf.merge(dfn, on='GISJOIN', how='inner')
    if merged_gdf.crs != 'EPSG:4326':
        merged_gdf = merged_gdf.to_crs('EPSG:4326')

    # Calculate number of dots
    for race in RACES:
        dfn[f'{race}_n_dots'] = (dfn[race] / N_PEOPLE_PER_DOT).round().astype(int)

    # Generate random points within polygons
    def random_points_in_polygon(polygon, num_points):
        points = []
        minx, miny, maxx, maxy = polygon.bounds
        while len(points) < num_points:
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
            if polygon.contains(pnt):
                points.append(pnt)
        return points

    all_dots = []
    for _, row in merged_gdf.iterrows():
        polygon = row.geometry
        for race in RACES:
            dfn_row = dfn[dfn.GISJOIN == row.GISJOIN].iloc[0]
            num_dots = dfn_row[f'{race}_n_dots']
            if num_dots > 0:
                points = random_points_in_polygon(polygon, num_dots)
                for point in points:
                    all_dots.append({'geometry': point, 'race': race})
    dots_gdf = gpd.GeoDataFrame(all_dots, crs=merged_gdf.crs)

    aspect_ratio = (crn.max_lon - crn.min_lon) / (crn.max_lat - crn.min_lat)
    fig_width = IMAGE_WIDTH
    fig_height = fig_width / aspect_ratio

    # Create figure
    fig = plt.figure(dpi=DPI, figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111)
    ax.set_xlim(crn.min_lon, crn.max_lon)
    ax.set_ylim(crn.min_lat, crn.max_lat)
    ax.set_aspect('equal')  # Preserve geographic proportions
    
    for race in RACES:
        race_dots = dots_gdf[dots_gdf.race == race]
        ax.scatter(race_dots.geometry.x, race_dots.geometry.y, 
                   s=DOT_SIZE / 10_000, color=RACE_COLORS[race], alpha=1.0, 
                   edgecolors='none', rasterized=True)  

    ax.set_axis_off()
    
    plt.savefig(f"images/dots_{year}.png", transparent=True, bbox_inches='tight', 
                pad_inches=0, dpi=DPI)
    plt.close()
