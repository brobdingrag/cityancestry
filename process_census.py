from consts import *


def get_race_agg_2020():
    df = load_df("demo_2020/race_2020_blck_grp")
    census_races = ['W', 'B', 'AI', 'A', 'NH', 'O']  # White, Black, American Indian, Asian, Native Hawaiian, Some Other Race

    # Step 1: Define racial category columns and their race combinations
    single_race_cols = [f'U7B{i:03d}' for i in range(3, 9)]  # U7B003 to U7B008
    single_race_sets = [{census_races[i-3]} for i in range(3, 9)]  # Single race sets: W, B, AI, A, NH, O

    two_race_cols = [f'U7B{i:03d}' for i in range(11, 26)]  # U7B011 to U7B025
    two_race_sets = [set(combo) for combo in combinations(census_races, 2)]

    three_race_cols = [f'U7B{i:03d}' for i in range(27, 47)]  # U7B027 to U7B046
    three_race_sets = [set(combo) for combo in combinations(census_races, 3)]

    four_race_cols = [f'U7B{i:03d}' for i in range(48, 63)]  # U7B048 to U7B062
    four_race_sets = [set(combo) for combo in combinations(census_races, 4)]

    five_race_cols = [f'U7B{i:03d}' for i in range(64, 70)]  # U7B064 to U7B069
    five_race_sets = [set(combo) for combo in combinations(census_races, 5)]

    six_race_col = ['U7B071']  # U7B071
    six_race_set = [set(census_races)]

    # Combine all racial category columns and sets
    race_category_cols = single_race_cols + two_race_cols + three_race_cols + four_race_cols + five_race_cols + six_race_col
    race_category_sets = single_race_sets + two_race_sets + three_race_sets + four_race_sets + five_race_sets + six_race_set
    race_combinations = dict(zip(race_category_cols, race_category_sets))

    # Step 2: Define summary categories
    summary_categories = [
        'H', 'B', 'W',
        'AI', 'NH', 'A', 'O'
    ]

    # Initialize summary columns in the DataFrame
    for cat in summary_categories:
        df[cat] = 0

    # Step 3: Function to determine summary category based on race set and Hispanic origin
    def get_summary_category(race_set, is_hispanic):
        if 'B' in race_set:
            return 'B'
        if is_hispanic:
            return 'H'
        if race_set == {'W'}:
            return 'W'
        if 'AI' in race_set:
            return 'AI'
        if 'NH' in race_set:
            return 'NH'
        if 'A' in race_set:
            return 'A'
        if 'O' in race_set:
            return 'O'
        raise ValueError(f"Invalid race set: {race_set}")

    # Step 4: Process each racial category and assign counts
    for col in race_category_cols:
        # Extract the numeric index from the P1 column (e.g., 'U7B003' -> 3)
        i = int(col[3:])
        # Corresponding Not Hispanic column in P2 (e.g., U7B003 -> U7C005)
        not_hisp_col = f'U7C{i+2:03d}'
        
        # Calculate counts
        hisp_count = df[col] - df[not_hisp_col]  # Hispanic = Total - Not Hispanic
        not_hisp_count = df[not_hisp_col]       # Not Hispanic count directly from P2
        
        # Get the race set for this column
        race_set = race_combinations[col]
        
        # Determine summary categories
        hisp_category = get_summary_category(race_set, True)
        not_hisp_category = get_summary_category(race_set, False)
        
        # Add counts to summary columns
        df[hisp_category] += hisp_count
        df[not_hisp_category] += not_hisp_count

    save_df(df, "demo_2020/race_agg_2020_blck_grp")
    # Create a filter for the tristate counties using STATE and COUNTY fields
    tristate_filter = (
        # New York counties
        ((df.STUSAB == 'NY') & df.COUNTY.isin(['Bronx County', 'Kings County', 'New York County', 'Queens County', 
                                               'Richmond County', 'Nassau County', 'Suffolk County', 'Westchester County', 'Rockland County',
                                               'Orange County', 'Putnam County', 'Sullivan County', 'Ulster County', 'Dutchess County'])) |
        # New Jersey counties
        ((df.STUSAB == 'NJ') & df.COUNTY.isin(['Bergen County', 'Hudson County', 'Passaic County', 'Essex County', 'Union County', 
                                               'Morris County', 'Middlesex County', 'Monmouth County', 'Somerset County', 'Mercer County',
                                               'Hunterdon County', 'Warren County', 'Sussex County'])) |
        # Connecticut counties
        ((df.STUSAB == 'CT') & df.COUNTY.isin(['Fairfield County', 'New Haven County', 'Middlesex County', 'New London County']))
    )
    dfn = df[tristate_filter]
    save_df(dfn, "demo_2020/race_agg_2020_tristate_blck_grp")


def get_race_agg_2010():
    # Load the 2010 block group data
    df = load_df("demo_2010/2010_blck_grp")
    
    # Define the census race codes
    census_races = ['W', 'B', 'AI', 'A', 'NH', 'O']  # White, Black, American Indian, Asian, Native Hawaiian, Some Other Race

    # Step 1: Define racial category columns and their race combinations
    single_race_cols = [f'H7Q{i:03d}' for i in range(3, 9)]  # H7Q003 to H7Q008
    single_race_sets = [{census_races[i-3]} for i in range(3, 9)]  # Single race sets: W, B, AI, A, NH, O

    two_race_cols = [f'H7Q{i:03d}' for i in range(11, 26)]  # H7Q011 to H7Q025
    two_race_sets = [set(combo) for combo in combinations(census_races, 2)]

    three_race_cols = [f'H7Q{i:03d}' for i in range(27, 47)]  # H7Q027 to H7Q046
    three_race_sets = [set(combo) for combo in combinations(census_races, 3)]

    four_race_cols = [f'H7Q{i:03d}' for i in range(48, 63)]  # H7Q048 to H7Q062
    four_race_sets = [set(combo) for combo in combinations(census_races, 4)]

    five_race_cols = [f'H7Q{i:03d}' for i in range(64, 70)]  # H7Q064 to H7Q069
    five_race_sets = [set(combo) for combo in combinations(census_races, 5)]

    six_race_col = ['H7Q071']  # H7Q071
    six_race_set = [set(census_races)]

    # Combine all racial category columns and sets
    race_category_cols = single_race_cols + two_race_cols + three_race_cols + four_race_cols + five_race_cols + six_race_col
    race_category_sets = single_race_sets + two_race_sets + three_race_sets + four_race_sets + five_race_sets + six_race_set
    race_combinations = dict(zip(race_category_cols, race_category_sets))

    # Step 2: Define summary categories
    summary_categories = ['H', 'B', 'W', 'AI', 'NH', 'A', 'O']  # Hispanic, Black, White, American Indian, Native Hawaiian, Asian, Other

    # Initialize summary columns in the DataFrame
    for cat in summary_categories:
        df[cat] = 0

    # Step 3: Function to determine summary category based on race set and Hispanic origin
    def get_summary_category(race_set, is_hispanic):
        if 'B' in race_set:
            return 'B'
        if is_hispanic:
            return 'H'
        if race_set == {'W'}:
            return 'W'
        if 'AI' in race_set:
            return 'AI'
        if 'NH' in race_set:
            return 'NH'
        if 'A' in race_set:
            return 'A'
        if 'O' in race_set:
            return 'O'
        raise ValueError(f"Invalid race set: {race_set}")

    # Step 4: Process each racial category and assign counts
    for col in race_category_cols:
        # Extract the numeric index from the P1 column (e.g., 'H7Q003' -> 3)
        i = int(col[3:])
        # Corresponding Not Hispanic column in P2 (e.g., 'H7Q003' -> 'H7R005')
        not_hisp_col = f'H7R{i+2:03d}'
        
        # Calculate counts
        hisp_count = df[col] - df[not_hisp_col]  # Hispanic = Total - Not Hispanic
        not_hisp_count = df[not_hisp_col]       # Not Hispanic count directly from P2
        
        # Get the race set for this column
        race_set = race_combinations[col]
        
        # Determine summary categories
        hisp_category = get_summary_category(race_set, True)
        not_hisp_category = get_summary_category(race_set, False)
        
        # Add counts to summary columns
        df[hisp_category] += hisp_count
        df[not_hisp_category] += not_hisp_count

    # Save the aggregated data
    save_df(df, "demo_2010/race_agg_2010_blck_grp")
    
    # Create a filter for the tristate counties (NY, NJ, CT)
    tristate_filter = (
        # New York counties
        ((df.STUSAB == 'NY') & df.COUNTY.isin(['Bronx County', 'Kings County', 'New York County', 'Queens County', 
                                               'Richmond County', 'Nassau County', 'Suffolk County', 'Westchester County', 'Rockland County',
                                               'Orange County', 'Putnam County', 'Sullivan County', 'Ulster County', 'Dutchess County'])) |
        # New Jersey counties
        ((df.STUSAB == 'NJ') & df.COUNTY.isin(['Bergen County', 'Hudson County', 'Passaic County', 'Essex County', 'Union County', 
                                               'Morris County', 'Middlesex County', 'Monmouth County', 'Somerset County', 'Mercer County',
                                               'Hunterdon County', 'Warren County', 'Sussex County'])) |
        # Connecticut counties
        ((df.STUSAB == 'CT') & df.COUNTY.isin(['Fairfield County', 'New Haven County', 'Middlesex County', 'New London County']))
    )
    
    # Apply the filter and save the tristate subset
    dfn = df[tristate_filter]
    save_df(dfn, "demo_2010/race_agg_2010_tristate_blck_grp")


def get_race_agg_2000():
    # Load the 2000 block group data
    df = load_df("demo_2000/2000_blck_grp")
    
    # Define the census race codes
    census_races = ['W', 'B', 'AI', 'A', 'NH', 'O']  # White, Black, Am. Indian, Asian, Native Hawaiian, Other

    # Single-race columns
    single_race_cols = [f'FXW{i:03d}' for i in range(1, 7)]  # FXW001 to FXW006
    not_hisp_single_race_cols = [f'FX1{i:03d}' for i in range(1, 7)]  # FX1001 to FX1006
    single_race_sets = [{'W'}, {'B'}, {'AI'}, {'A'}, {'NH'}, {'O'}]

    # Multi-race columns
    multi_race_cols = [f'FXY{i:03d}' for i in range(1, 58)]  # FXY001 to FXY057
    not_hisp_multi_race_cols = [f'FX3{i:03d}' for i in range(1, 58)]  # FX3001 to FX3057

    # Generate multi-race sets
    two_race_sets = [set(combo) for combo in combinations(census_races, 2)]  # 15 combinations
    three_race_sets = [set(combo) for combo in combinations(census_races, 3)]  # 20 combinations
    four_race_sets = [set(combo) for combo in combinations(census_races, 4)]  # 15 combinations
    five_race_sets = [set(combo) for combo in combinations(census_races, 5)]  # 6 combinations
    six_race_set = [set(census_races)]  # 1 combination
    multi_race_sets = two_race_sets + three_race_sets + four_race_sets + five_race_sets + six_race_set
    race_combinations = dict(zip(multi_race_cols, multi_race_sets))

    # Summary categories
    summary_categories = ['H', 'B', 'W', 'AI', 'NH', 'A', 'O']
    for cat in summary_categories:
        df[cat] = 0

    # Define the summary category assignment function
    def get_summary_category(race_set, is_hispanic):
        if 'B' in race_set:
            return 'B'
        if is_hispanic:
            return 'H'
        if race_set == {'W'}:
            return 'W'
        if 'AI' in race_set:
            return 'AI'
        if 'NH' in race_set:
            return 'NH'
        if 'A' in race_set:
            return 'A'
        if 'O' in race_set:
            return 'O'
        raise ValueError(f"Invalid race set: {race_set}")

    # Process single races
    for total_col, not_hisp_col, race_set in zip(single_race_cols, not_hisp_single_race_cols, single_race_sets):
        hisp_count = df[total_col] - df[not_hisp_col]
        not_hisp_count = df[not_hisp_col]
        hisp_category = get_summary_category(race_set, True)
        not_hisp_category = get_summary_category(race_set, False)
        df[hisp_category] += hisp_count
        df[not_hisp_category] += not_hisp_count

    # Process multi-races
    for total_col, not_hisp_col in zip(multi_race_cols, not_hisp_multi_race_cols):
        hisp_count = df[total_col] - df[not_hisp_col]
        not_hisp_count = df[not_hisp_col]
        race_set = race_combinations[total_col]
        hisp_category = get_summary_category(race_set, True)
        not_hisp_category = get_summary_category(race_set, False)
        df[hisp_category] += hisp_count
        df[not_hisp_category] += not_hisp_count

    # Save aggregated data
    save_df(df, "demo_2000/race_agg_2000_blck_grp")

    # Tristate filter (NY, NJ, CT)
    tristate_filter = (
        # New York counties
        ((df['STUSAB'] == 'NY') & df['COUNTY'].isin([
            'Bronx', 'Kings', 'New York', 'Queens', 'Richmond',
            'Nassau', 'Suffolk', 'Westchester', 'Rockland',
            'Orange', 'Putnam', 'Sullivan', 'Ulster', 'Dutchess'
        ])) |
        # New Jersey counties
        ((df['STUSAB'] == 'NJ') & df['COUNTY'].isin([
            'Bergen', 'Hudson', 'Passaic', 'Essex', 'Union',
            'Morris', 'Middlesex', 'Monmouth', 'Somerset', 'Mercer',
            'Hunterdon', 'Warren', 'Sussex'
        ])) |
        # Connecticut counties
        ((df['STUSAB'] == 'CT') & df['COUNTY'].isin([
            'Fairfield', 'New Haven', 'Middlesex', 'New London'
        ]))
    )

    # Apply filter and save tristate subset
    df_tristate = df[tristate_filter]
    save_df(df_tristate, "demo_2000/race_agg_2000_tristate_blck_grp")


def get_race_agg_1990():
    # Load the 1990 block group data
    df = load_df("demo_1990/1990_blck_grp")
    
    # Define summary categories for 1990 (no 'NH' due to data structure)
    summary_categories = ['H', 'B', 'W', 'AI', 'A', 'O']
    
    # Initialize summary columns
    for cat in summary_categories:
        df[cat] = 0
    
    # Apply aggregation logic
    df['B'] = df['ET2002'] + df['ET2007']  # All Black individuals
    df['H'] = df['ET2006'] + df['ET2008'] + df['ET2009'] + df['ET2010']  # Hispanic, non-Black
    df['W'] = df['ET2001']  # Not Hispanic, White
    df['AI'] = df['ET2003']  # Not Hispanic, American Indian, Eskimo, or Aleut
    df['A'] = df['ET2004']  # Not Hispanic, Asian or Pacific Islander
    df['O'] = df['ET2005']  # Not Hispanic, Other race
    
    # Save the aggregated data
    save_df(df, "demo_1990/race_agg_1990_blck_grp")
    
    # Define tristate filter with short county names
    tristate_filter = (
        # New York counties
        ((df['STUSAB'] == 'NY') & df['COUNTY'].isin([
            'Bronx', 'Kings', 'New York', 'Queens', 'Richmond',
            'Nassau', 'Suffolk', 'Westchester', 'Rockland',
            'Orange', 'Putnam', 'Sullivan', 'Ulster', 'Dutchess'
        ])) |
        # New Jersey counties
        ((df['STUSAB'] == 'NJ') & df['COUNTY'].isin([
            'Bergen', 'Hudson', 'Passaic', 'Essex', 'Union',
            'Morris', 'Middlesex', 'Monmouth', 'Somerset', 'Mercer',
            'Hunterdon', 'Warren', 'Sussex'
        ])) |
        # Connecticut counties
        ((df['STUSAB'] == 'CT') & df['COUNTY'].isin([
            'Fairfield', 'New Haven', 'Middlesex', 'New London'
        ]))
    )
    
    # Apply filter and save tristate subset
    df_tristate = df[tristate_filter]
    save_df(df_tristate, "demo_1990/race_agg_1990_tristate_blck_grp")


def get_race_agg_1980():
    # Load datasets
    ds1 = load_df("demo_1980/ds1_1980_tract")  # Hispanic data
    ds2 = load_df("demo_1980/ds2_1980_tract")  # Total population data
    
    # Merge on GISJOIN with outer join
    df = ds2.merge(ds1, on="GISJOIN", how="outer", suffixes=("", "_1"))
    
    # Fill NaN in Hispanic columns with 0
    for col in ['C9G001', 'C9G002', 'C9G003', 'C9G004']:
        df[col] = df[col].fillna(0)
    
    # Calculate summary categories based on dominance rules
    df['B'] = df['C6X002']  # Total Black (Black > Hispanic)
    df['H'] = df['C9G001'] + df['C9G003'] + df['C9G004']  # Hispanic non-Black
    df['W'] = df['C6X001'] - df['C9G001']  # Non-Hispanic White
    df['AI'] = df['C6X003'] - df['C9G003']  # Non-Hispanic American Indian
    df['A'] = df['C6X004']  # Non-Hispanic Asian (assuming no Hispanic Asians)
    df['O'] = df['C6X005'] - df['C9G004']  # Non-Hispanic Other
    
    # Calculate intersection of Hispanic ethnicity and Black race
    df['BH'] = df['C9G002']  # Hispanic Black
    
    # Calculate intersection of Hispanic ethnicity and Other race
    df['OH'] = df['C9G004']  # Hispanic Other
    
    # Ensure no negative values
    for col in ['W', 'AI', 'O']:
        df[col] = df[col].clip(lower=0)
    
    df = df.loc[:, ~df.columns.str.endswith('_1')]  # Drop ds1 columns with "_1" suffix
    
    # Save aggregated data for all tracts
    save_df(df, "demo_1980/race_agg_1980_tract")
    
    # Apply tristate filter (NY, NJ, CT)
    tristate_filter = (
        ((df['STATEA'] == 36) & df['COUNTY'].isin([
            'Bronx', 'Kings', 'New York', 'Queens', 'Richmond',
            'Nassau', 'Suffolk', 'Westchester', 'Rockland', 'Orange',
            'Putnam', 'Sullivan', 'Ulster', 'Dutchess'
        ])) |
        ((df['STATEA'] == 34) & df['COUNTY'].isin([
            'Bergen', 'Hudson', 'Passaic', 'Essex', 'Union', 'Morris',
            'Middlesex', 'Monmouth', 'Somerset', 'Mercer', 'Hunterdon',
            'Warren', 'Sussex'
        ])) |
        ((df['STATEA'] == 9) & df['COUNTY'].isin([
            'Fairfield', 'New Haven', 'Middlesex', 'New London'
        ]))
    )
    df_tristate = df[tristate_filter]
    
    # Save tristate subset
    save_df(df_tristate, "demo_1980/race_agg_1980_tristate_tract")


def get_race_agg_1970():
    # Assumptions
    percent_other_hispanic = 0.1
    percent_other_asian = PERCENT_OTHER_ASIAN  # Assumption: 60% of 'other' race people are Asian
    
    # Load the datasets
    df1 = load_df("demo_1970/1_1970_tract")  # Race data
    df2 = load_df("demo_1970/2_1970_tract")  # Spanish Indicator data

    # Merge on GISJOIN with an outer join
    df = df1.merge(df2, on="GISJOIN", how="outer", suffixes=("", "_2"))

    # Fill missing C11001 values with 0 (for GISJOINs in df1 but not df2)
    df['C11001'] = df['C11001'].fillna(0)

    # Calculate aggregated race categories
    df['B'] = df['C0X002']  # Black (Negro), all non-Hispanic
    df['H'] = df['C11001'] + (df['C0X003'] * percent_other_hispanic) # Hispanic, total Hispanic population
    df['W'] = (df['C0X001'] -  df['C11001']).clip(lower=0)  # Non-Hispanic White
    
    # Split 'Other' into Asian and Other based on assumption
    other = df['C0X003']
    df['A'] = other * percent_other_asian  # Asian portion of Other
    df['O'] = other * (1 - percent_other_asian - percent_other_hispanic)  # Remaining Other

    df = df.loc[:, ~df.columns.str.endswith('_2')]        # Remove df2 columns with "_2" suffix

    # Save the full aggregated dataset
    save_df(df, "demo_1970/race_agg_1970_tract")

    # Apply tristate filter (NY, NJ, CT) for a subset
    tristate_filter = (
        ((df['STATEA'] == 36.0) & df['COUNTY'].isin([
            'Bronx', 'Kings', 'New York', 'Queens', 'Richmond',
            'Nassau', 'Suffolk', 'Westchester', 'Rockland', 'Orange',
            'Putnam', 'Sullivan', 'Ulster', 'Dutchess'
        ])) |
        ((df['STATEA'] == 34.0) & df['COUNTY'].isin([
            'Bergen', 'Hudson', 'Passaic', 'Essex', 'Union', 'Morris',
            'Middlesex', 'Monmouth', 'Somerset', 'Mercer', 'Hunterdon',
            'Warren', 'Sussex'
        ])) |
        ((df['STATEA'] == 9.0) & df['COUNTY'].isin([
            'Fairfield', 'New Haven', 'Middlesex', 'New London'
        ]))
    )
    df_tristate = df[tristate_filter]

    # Save the tristate subset
    save_df(df_tristate, "demo_1970/race_agg_1970_tristate_tract")


def get_race_agg_1960():
    # Assumptions
    percent_other_hispanic = 0.1
    percent_other_asian = PERCENT_OTHER_ASIAN      # Fraction of remaining non-Hispanic 'Other' that is Asian
    
    # Load the dataframe
    df = load_df("demo_1960/1960_tract")
    
    # Fill missing CA7001 with 0
    df['CA7001'] = df['CA7001'].fillna(0)
    
    # Calculate Hispanic population from 'Other'
    H_from_other = percent_other_hispanic * df['B7B003']
    
    # Total Hispanic population is CA7001
    df['H'] = H_from_other + df['CA7001']
    
    # 'Other' 
    O_total = df['B7B003']
    
    # Split 'Other' into Asian and Other
    df['A'] = percent_other_asian * O_total           # Non-Hispanic Asian
    df['O'] = (1 - percent_other_asian - percent_other_hispanic) * O_total     # Non-Hispanic Other
    
    # Adjust White population for any Hispanic population
    df['W'] = (df['B7B001'] - df['CA7001']).clip(lower=0)  # Non-Hispanic White
    
    # Black population (all non-Hispanic)
    df['B'] = df['B7B002']
    
    # Fill any NaN values with 0 in the race columns
    race_cols = ['B', 'H', 'W', 'A', 'O']
    df[race_cols] = df[race_cols].fillna(0)
    
    # Save the full aggregated dataset
    save_df(df, "demo_1960/race_agg_1960_tract")
    
    # Apply tristate filter (NY, NJ, CT)
    tristate_filter = (
        ((df['STATEA'] == 36.0) & df['COUNTY'].isin([
            'Bronx', 'Kings', 'New York', 'Queens', 'Richmond',
            'Nassau', 'Suffolk', 'Westchester', 'Rockland', 'Orange',
            'Putnam', 'Sullivan', 'Ulster', 'Dutchess'
        ])) |
        ((df['STATEA'] == 34.0) & df['COUNTY'].isin([
            'Bergen', 'Hudson', 'Passaic', 'Essex', 'Union', 'Morris',
            'Middlesex', 'Monmouth', 'Somerset', 'Mercer', 'Hunterdon',
            'Warren', 'Sussex'
        ])) |
        ((df['STATEA'] == 9.0) & df['COUNTY'].isin([
            'Fairfield', 'New Haven', 'Middlesex', 'New London'
        ]))
    )
    df_tristate = df[tristate_filter]
    
    # Save the tristate subset
    save_df(df_tristate, "demo_1960/race_agg_1960_tristate_tract")


def get_race_agg_1950():
    """Uses nativity (mexico, other amierica and asia)"""
    percent_other_asian = PERCENT_OTHER_ASIAN
    # Load the dataframe
    df = load_df("demo_1950/1950_tract")
    
    # Calculate Hispanic population from nativity data
    df['H'] = df['B1L026'] + df['B1L027']  # Mexico + Other America
    
    # Calculate Asian foreign-born whites
    Asian_foreign_born_white = df['B1L023']
    
    # Calculate aggregated race categories
    df['B'] = df['B0J002']  # Black (Negro)
    df['W'] = (df['B0J001'] - df['H'] - Asian_foreign_born_white).clip(lower=0)  # White, subtracting Hispanic and Asian foreign-born whites
    df['A'] = Asian_foreign_born_white + (percent_other_asian * df['B0J003'])  # Asian: B1L023 + 60% of 'Other nonwhite'
    df['O'] = (1 - percent_other_asian) * df['B0J003']  # Other: 40% of 'Other nonwhite'
    
    # Fill any NaN values with 0 in the race columns
    race_cols = ['B', 'H', 'W', 'A', 'O']
    df[race_cols] = df[race_cols].fillna(0)
    
    # Save the full aggregated dataset
    save_df(df, "demo_1950/race_agg_1950_tract")
    save_df(df, "demo_1950/race_agg_1950_tristate_tract")



def get_race_agg_1940():
    """Uses nativity x sex data (mexico, cuba, central america, other america and asia)"""

    percent_other_asian = PERCENT_OTHER_ASIAN

    # Load the dataframe
    df = load_df("demo_1940/1940_tract")
    
    # Calculate Hispanic population (foreign-born whites from Mexico, Cuba, Central America)
    H = df['BUG030'] + df['BUG063'] + df['BUG031'] + df['BUG064'] + df['BUG032'] + df['BUG065']
    
    # Calculate Asian foreign-born white population (from Asia)
    Asian_foreign_born_white = df['BUG026'] + df['BUG059']
    
    # Calculate "nonwhite that remains" after subtracting Negro from Nonwhite
    Other_nonwhite = (df['BUQ002'] - df['BVG001']).clip(lower=0)
    
    # Define aggregated race categories
    df['H'] = H  # Hispanic
    df['W'] = (df['BUQ001'] - H - Asian_foreign_born_white).clip(lower=0)  # White, adjusted
    df['B'] = df['BVG001']  # Black (Negro)
    df['A'] = Asian_foreign_born_white + (percent_other_asian * Other_nonwhite)  # Asian
    df['O'] = (1 - percent_other_asian) * Other_nonwhite  # Other
    
    # Fill any NaN values with 0 in the race columns
    race_cols = ['B', 'H', 'W', 'A', 'O']
    df[race_cols] = df[race_cols].fillna(0)
    
    # Save the aggregated dataset
    save_df(df, "demo_1940/race_agg_1940_tract")
    save_df(df, "demo_1940/race_agg_1940_tristate_tract")



def get_race_agg_1930():
    """
    Aggregates 1930 Census tract data into race categories: Hispanic (H), White (W),
    Black (B), Asian (A), and Other (O). Uses Cuban and Mexican ancestry for Hispanic
    in NYC (df2), estimates Hispanic elsewhere, and allocates PERCENT_OTHER_ASIAN of
    'Other' race as Asian. Only Westchester County is used from df3.
    """
    # Set the percentage of 'Other' race to classify as Asian
    percent_other_asian = PERCENT_OTHER_ASIAN

    # Load NYC data (df2) to calculate Hispanic proportion
    df2 = load_df("demo_1930/66_1930_tract")

    # Process NYC tracts (df2)
    df2_agg = df2.copy()
    df2_agg['H'] = df2['BOB006'] + df2['BOB018']  # Hispanic from ancestry
    df2_agg['W'] = ((df2['BOC001'] + df2['BOC002'] + df2['BOC003'] + 
                    df2['BOC006'] + df2['BOC007'] + df2['BOC008']) - df2_agg['H']).clip(lower=0)  # Non-Hispanic White
    df2_agg['B'] = df2['BOC004'] + df2['BOC009']  # Black
    O_total = df2['BOC005'] + df2['BOC010']  # Total 'Other' races
    df2_agg['A'] = percent_other_asian * O_total  # Asian
    df2_agg['O'] = (1 - percent_other_asian) * O_total  # Remaining Other

    # Load df3 and filter to Westchester County (New York, STATEA = 36, COUNTYA = 119)
    df3 = load_df("demo_1930/67_1930_tract")
    df3_westchester = df3[(df3['STATEA'] == 36) & (df3['COUNTYA'] == 119)].copy()
    W_total = df3_westchester['BOK001'] + df3_westchester['BOK002'] + df3_westchester['BOK003']
    df3_westchester['H'] = 0 
    df3_westchester['W'] = W_total 
    df3_westchester['B'] = df3_westchester['BOK004']  # Black
    O_total = df3_westchester['BOK005']  # Total 'Other' races
    df3_westchester['A'] = percent_other_asian * O_total  # Asian
    df3_westchester['O'] = (1 - percent_other_asian) * O_total  # Remaining Other

    # Define common columns for concatenation
    context_cols = ['GISJOIN', 'YEAR', 'STATE', 'STATEA', 'COUNTY', 'COUNTYA', 
                    'TRACTA', 'AREANAME']
    race_cols = ['H', 'W', 'B', 'A', 'O']

    # Ensure all dataframes have the required columns
    df2_agg = df2_agg[context_cols + race_cols]
    df3_westchester = df3_westchester[context_cols + race_cols]

    # Concatenate the aggregated dataframes
    df_agg = pd.concat([df2_agg, df3_westchester], ignore_index=True)

    # Ensure non-negative values and fill NaNs with 0
    df_agg[race_cols] = df_agg[race_cols].clip(lower=0).fillna(0)

    # Save the aggregated dataset
    save_df(df_agg, "demo_1930/race_agg_1930_tract")
    save_df(df_agg, "demo_1930/race_agg_1930_tristate_tract")



def get_race_agg_1920():
    """
    Aggregates 1920 Census tract data into race categories: Hispanic (H), White (W),
    Black (B), Asian (A), and Other (O). Hispanic is set to 0, and PERCENT_OTHER_ASIAN
    of the 'Other' race is classified as Asian.
    """
    # Set the percentage of 'Other' race to classify as Asian
    percent_other_asian = PERCENT_OTHER_ASIAN
    
    # Load the dataframe
    df = load_df("demo_1920/1920_tract")
    
    # Calculate aggregated race categories
    df['H'] = 0  # Hispanic set to 0
    df['W'] = df['BCG001'] + df['BCG002'] + df['BCG003'] + df['BCG004']  # White
    df['B'] = df['BCG005']  # Black
    df['A'] = percent_other_asian * df['BCG006']  # Asian from 'Other'
    df['O'] = (1 - percent_other_asian) * df['BCG006']  # Remaining 'Other'
    
    # Fill any NaN values with 0 in the race columns
    race_cols = ['H', 'W', 'B', 'A', 'O']
    df[race_cols] = df[race_cols].fillna(0)
    
    # Save the aggregated dataset
    save_df(df, "demo_1920/race_agg_1920_tract")
    save_df(df, "demo_1920/race_agg_1920_tristate_tract")



def get_race_agg_1910():
    """
    Aggregates 1910 Census tract data into race categories: Hispanic (H), White (W),
    Black (B), Asian (A), and Other (O). Hispanic is set to 0, and PERCENT_OTHER_ASIAN
    of the 'Other' race is classified as Asian.
    """
    # Set the percentage of 'Other' race to classify as Asian
    percent_other_asian = PERCENT_OTHER_ASIAN
    
    # Load the dataframe
    df = load_df("demo_1910/1910_tract")
    
    # Calculate aggregated race categories
    df['H'] = 0  # Hispanic set to 0
    df['W'] = df['A60001'] + df['A60002'] + df['A60003'] + df['A60004'] + df['A60005']  # White
    df['B'] = df['A60006']  # Black
    df['A'] = percent_other_asian * df['A60007']  # Asian from 'Other'
    df['O'] = (1 - percent_other_asian) * df['A60007']  # Remaining 'Other'
    
    # Fill any NaN values with 0 in the race columns
    race_cols = ['H', 'W', 'B', 'A', 'O']
    df[race_cols] = df[race_cols].fillna(0)
    
    # Save the aggregated dataset
    save_df(df, "demo_1910/race_agg_1910_tract")
    save_df(df, "demo_1910/race_agg_1910_tristate_tract")



