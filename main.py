#!/usr/bin/env python3

from sys import exit
from os import getcwd, EX_DATAERR

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sn

from data_processing.religion import transform_religion_data
from data_processing.educational_attainment import transform_educational_attainment_data
from utils import get_list_of_counties, get_religion_data_path, \
    get_educational_attainment_data_path, combine_data_frame


ASSETS_PATH: str = f'{getcwd()}/assets'


def plot_connection_between_changes(df: pd.DataFrame) -> None:
    plt.scatter('percentage_of_religious_population_2011', 'educational_attainment_level_2011', data=df, marker='*')

    plt.ylim(0, 1)

    plt.xlim(0, 1)

    plt.ylabel('Educational attainment level [0; 1]')

    plt.xlabel('Percentage of religious population [0; 1]')

    plt.show()

    sn.heatmap(df[['percentage_of_religious_population_2011', 'educational_attainment_level_2011']].corr(), annot=True)

    plt.show()


def process_data() -> None:
    counties = get_list_of_counties(ASSETS_PATH)

    data_frames: list[pd.DataFrame] = []

    for county in counties:
        ok, file_path = get_religion_data_path(ASSETS_PATH, county)

        religion_df = transform_religion_data(file_path) if ok else exit(EX_DATAERR)

        ok, file_path = get_educational_attainment_data_path(ASSETS_PATH, county)

        educational_df = transform_educational_attainment_data(file_path) if ok else exit(EX_DATAERR)

        ok, combined_df = combine_data_frame(religion_df, educational_df, on='id')

        # combined_df.to_json(f'out/{county}.json', orient='records', index=False)

        data_frames.append(combined_df)

    df = pd.concat(data_frames)

    df.to_csv(f'out/religion_educational_data.csv', index=False)  # orient='records'

    plot_connection_between_changes(df)


def process_religion_data() -> None:
    counties = get_list_of_counties(ASSETS_PATH)

    data_frames: list[pd.DataFrame] = []

    for county in counties:
        ok, file_path = get_religion_data_path(ASSETS_PATH, county)

        religion_df = transform_religion_data(file_path) if ok else exit(EX_DATAERR)

        religion_df.to_json(f'out/religion_{county}.json', orient='records', index=False)

        data_frames.append(religion_df)

    df = pd.concat(data_frames)

    df.to_json('out/religion_country.json', orient='records', index=False)

    plt.scatter('id', 'change_in_religious_population', data=df)

    plt.axline((0, 0), (max(pd.unique(df['id'].values)), 0), color='red')

    plt.xlabel('The id of the districts')

    plt.ylabel('Change')

    plt.title('Change in the number of religious people between 2011 and 2022')

    plt.show()


def process_educational_attainment_data() -> None:
    counties = get_list_of_counties(ASSETS_PATH)

    data_frames: list[pd.DataFrame] = []

    for county in counties:
        ok, file_path = get_educational_attainment_data_path(ASSETS_PATH, county)

        educational_attainment_df = transform_educational_attainment_data(file_path) if ok else exit(EX_DATAERR)

        educational_attainment_df.to_json(f'out/education_{county}.json', orient='records', index=False)

        data_frames.append(educational_attainment_df)

    df = pd.concat(data_frames)

    df.to_json('out/education_country.json', orient='records', index=False)

    plt.scatter('id', 'change_in_educational_attainment_level', data=df)

    plt.axline((0, 0), (max(pd.unique(df['id'].values)), 0), color='red')

    plt.show()


def main() -> None:
    process_data()


if __name__ == '__main__':
    main()
