from process_census import *
from plot_dots import *

def main():
    get_race_agg_2020()
    get_race_agg_2010()
    get_race_agg_2000()
    get_race_agg_1990()
    get_race_agg_1980()
    get_race_agg_1970()
    get_race_agg_1960()
    get_race_agg_1950()
    get_race_agg_1940()
    get_race_agg_1930()
    get_race_agg_1920()
    get_race_agg_1910()

    plot_dots_blck_grp(2020)
    plot_dots_blck_grp(2010)
    plot_dots_blck_grp(2000)
    plot_dots_blck_grp(1990)
    plot_dots_tract(1980)
    plot_dots_tract(1970)
    plot_dots_tract(1960)
    plot_dots_tract(1950)
    plot_dots_tract(1940)
    plot_dots_tract(1930)
    plot_dots_tract(1920)
    plot_dots_tract(1910)


if __name__ == "__main__":
    main()


