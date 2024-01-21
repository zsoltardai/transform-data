import pandas as pd

from data_processing.counties import get_counties


def get_value_for_religion(df: pd.DataFrame, group: str) -> float:
    """
    This function returns the number of the people who practice the religion.
    :param df: The DataFrame that holds the religion data.
    :param group: The identifier code of the religion.
    :return: The number of the people who practice the religion.
    """
    return max(df[df['group'] == group]['value'].values[0], 0)


def transform_religion_data(file: str) -> pd.DataFrame:
    """
    This function transforms the bare data into a DataFrame with two columns. The two
    columns are: ID: int, PERCENTAGE_OF_RELIGIOUS_PEOPLE: float.
    :param file: The path to the file, which holds the religion data.
    :return: A DataFrame which contains the percentage of the religious population
    by district.
    """

    # defining the columns we would like to use
    cols: list[str] = ['TERUL_GEO5', 'TEL_SZ_ADAT', 'OBS_VALUE', 'TIME_PERIOD']

    # reading religion ksh statistics from csv file
    df: pd.DataFrame = pd.read_csv(file, delimiter=';', usecols=cols, na_values='null')

    # renaming columns
    df.rename(
        inplace=True,
        columns={
            'TERUL_GEO5': 'id',
            'OBS_VALUE': 'value',
            'TEL_SZ_ADAT': 'group',
            'TIME_PERIOD': 'year',
        },
    )

    # saving the religion
    religion_column = df['group']

    # transforming religion column into boolean value
    df['flag'] = religion_column.map(lambda religion: religion != 'RE_NOT')

    # removing the null values
    df['value'] = df['value'].fillna(0)

    # creating a new DataFrame with the newly calculated values
    new_df = pd.DataFrame({
        'id': [],
        'roman_catholic_2011': [],
        'greek_catholic_2011': [],
        'calvinist_2011': [],
        'lutheran_2011': [],
        'orthodox_christian_2011': [],
        'other_christian_2011': [],
        'jewish_2011': [],
        'atheist_2011': [],
        'other_2011': [],
        'percentage_of_religious_population_2011': [],
        'roman_catholic_2022': [],
        'greek_catholic_2022': [],
        'calvinist_2022': [],
        'lutheran_2022': [],
        'orthodox_christian_2022': [],
        'other_christian_2022': [],
        'jewish_2022': [],
        'atheist_2022': [],
        'other_2022': [],
        'percentage_of_religious_population_2022': [],
        'change_in_the_number_of_religious_population': [],
    })

    # looping through the ids of all districts
    for district_id in pd.unique(df['id']):
        records = df[df['id'] == district_id]

        record_2011 = records[records['year'] == 2011]

        record_2022 = records[records['year'] == 2022]

        # getting the number of people who were part of any religion in 2011
        number_of_religious_people_2011: float = sum(record_2011[record_2011['flag'] == True]['value'].values)

        # getting the number of people who do not participate any religions in 2011
        number_of_non_religious_people_2011: float = sum(record_2011[record_2011['flag'] == False]['value'].values)

        # calculating the percentage of religious population in 2011
        percentage_of_religious_population_2011: float = number_of_religious_people_2011 /\
                                                         (number_of_non_religious_people_2011
                                                          + number_of_religious_people_2011)

        # getting the number of people who were part of any religion in 2022
        number_of_religious_people_2022: float = sum(record_2022[record_2022['flag'] == True]['value'].values)

        # getting the number of people who do not participate any religions in 2022
        number_of_non_religious_people_2022: float = sum(record_2022[record_2022['flag'] == False]['value'].values)

        # calculating the percentage of religious population in 2022
        percentage_of_religious_population_2022: float = number_of_religious_people_2022 /\
                                                         (number_of_non_religious_people_2022
                                                          + number_of_religious_people_2022)

        # calculating the change in the number of religious people between 2011 and 2022
        difference: float = number_of_religious_people_2022 - number_of_religious_people_2011

        # calculating the change in percentages
        change: float = difference / number_of_religious_people_2011

        # we append the new row, with the matching data
        new_df.loc[len(new_df)] = {
            'id': district_id,
            'roman_catholic_2011': get_value_for_religion(record_2011, 'RE_RC'),
            'greek_catholic_2011': get_value_for_religion(record_2011, 'RE_GC'),
            'calvinist_2011': get_value_for_religion(record_2011, 'RE_CA'),
            'lutheran_2011': get_value_for_religion(record_2011, 'RE_LU'),
            'orthodox_christian_2011': get_value_for_religion(record_2011, 'RE_OC'),
            'other_christian_2011': get_value_for_religion(record_2011, 'RE_CD'),
            'jewish_2011': get_value_for_religion(record_2011, 'RE_J'),
            'atheist_2011': get_value_for_religion(record_2011, 'RE_NOT'),
            'other_2011': get_value_for_religion(record_2011, 'RE_OCD'),
            'percentage_of_religious_population_2011': round(percentage_of_religious_population_2011, 4),
            'roman_catholic_2022': get_value_for_religion(record_2022, 'RE_RC'),
            'greek_catholic_2022': get_value_for_religion(record_2022, 'RE_GC'),
            'calvinist_2022': get_value_for_religion(record_2022, 'RE_CA'),
            'lutheran_2022': get_value_for_religion(record_2022, 'RE_LU'),
            'orthodox_christian_2022': get_value_for_religion(record_2022, 'RE_OC'),
            'other_christian_2022': get_value_for_religion(record_2022, 'RE_CD'),
            'jewish_2022': get_value_for_religion(record_2022, 'RE_J'),
            'atheist_2022': get_value_for_religion(record_2022, 'RE_NOT'),
            'other_2022': get_value_for_religion(record_2022, 'RE_OCD'),
            'percentage_of_religious_population_2022': round(percentage_of_religious_population_2022, 4),
            'change_in_the_number_of_religious_population': round(change, 4),
        }

    return new_df


def get_number_of_people_by_religion(year: int) -> None:
    counties: list[dict[str, any]] = get_counties()

    df = pd.read_csv()


if __name__ == '__main__':
    get_number_of_people_by_religion(2011)
