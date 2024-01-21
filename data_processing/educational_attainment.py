import pandas as pd


def get_value_for_educational_attainment(df: pd.DataFrame, group: int) -> float:
    """
    This function returns the number of the people who practice the religion.
    :param df: The DataFrame that holds the religion data.
    :param group: The identifier code of the religion.
    :return: The number of the people who practice the religion.
    """
    return max(df[df['group'] == group]['value'].values[0], 0)


def calculate_normalized_value(df: pd.DataFrame) -> float:
    weighted_total = sum([value * weight for value, weight in df[['value', 'group']].values])

    total = sum(df['value'].values)

    return round(((weighted_total / total) - 1) / 4, 4)


def transform_educational_attainment_data(file: str) -> pd.DataFrame:
    # defining the columns we would like to use
    cols: list[str] = ['TERUL_GEO5', 'TEL_SZ_ADAT', 'OBS_VALUE', 'TIME_PERIOD']

    # reading religion ksh statistics from csv file
    df: pd.DataFrame = pd.read_csv(file, delimiter=';', usecols=cols)

    # renaming columns
    df.rename(
        inplace=True,
        columns={
            'TERUL_GEO5': 'id',
            'TEL_SZ_ADAT': 'group',
            'OBS_VALUE': 'value',
            'TIME_PERIOD': 'year',
        },
    )

    # mapping the EDUCATIONAL_ATTAINMENT_LEVEL to nominal values
    df['group'] = df['group'].apply(lambda x: int(x[-1]))

    # creating a new DataFrame in order to store the transformed data
    new_df = pd.DataFrame({
        'id': [],
        'educational_attainment_level_2011': [],
        'educational_attainment_level_2022': [],
        'bellow_eight_grade_2011': [],
        'primary_school_2011': [],
        'secondary_school_2011': [],
        'high_school_2011': [],
        'higher_education_2011': [],
        'bellow_eight_grade_2022': [],
        'primary_school_2022': [],
        'secondary_school_2022': [],
        'high_school_2022': [],
        'higher_education_2022': [],
        'change_in_educational_attainment_level': [],
    })

    # we loop trough each identifier and look for the rows which has the same identifier
    for identifier in pd.unique(df['id']):
        records = df[df['id'] == identifier]

        records_2011 = records[records['year'] == 2011]

        records_2022 = records[records['year'] == 2022]

        educational_attainment_level_2011: float = calculate_normalized_value(records_2011)

        educational_attainment_level_2022: float = calculate_normalized_value(records_2022)

        change_in_educational_attainment_level= educational_attainment_level_2022 - educational_attainment_level_2011

        # we append the new row, with the matching data
        new_df.loc[len(new_df)] = {
            'id': identifier,
            'educational_attainment_level_2011': educational_attainment_level_2011,
            'educational_attainment_level_2022': educational_attainment_level_2022,
            'bellow_eight_grade_2011': get_value_for_educational_attainment(records_2011, 1),
            'primary_school_2011': get_value_for_educational_attainment(records_2011, 2),
            'secondary_school_2011': get_value_for_educational_attainment(records_2011, 3),
            'high_school_2011': get_value_for_educational_attainment(records_2011, 4),
            'higher_education_2011': get_value_for_educational_attainment(records_2022, 5),
            'bellow_eight_grade_2022': get_value_for_educational_attainment(records_2022, 1),
            'primary_school_2022': get_value_for_educational_attainment(records_2022, 2),
            'secondary_school_2022': get_value_for_educational_attainment(records_2022, 3),
            'high_school_2022': get_value_for_educational_attainment(records_2022, 4),
            'higher_education_2022': get_value_for_educational_attainment(records_2022, 5),
            'change_in_educational_attainment_level': change_in_educational_attainment_level,
        }

    return new_df
