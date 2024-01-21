from pandas import DataFrame


def combine_data_frame(df_1: DataFrame, df_2: DataFrame, on: str = 'ID') -> tuple[bool, DataFrame]:

    """
    Combines two dataframes based on a column. As default the function
    uses ID as the name of the column we want to combine the DataFrames based on.
    :param df_1: The first DataFrame we want to combine with the second one.
    :param df_2: The second DataFrame we want to combine with the first one.
    :param on: The name of the column we want to combine the two DataFrames based on.
    :return: Returns with a Tuple[bool, DataFrame] where the first argument represents
    if the two DataFrames combined successfully, and the second parameter is the
    combined DataFrame.
    """

    False, DataFrame({}) if on not in df_1.columns else None

    False, DataFrame({}) if on not in df_2.columns else None

    combined_df = df_1.join(df_2, rsuffix='_RIGHT')

    del combined_df[f'{on}_RIGHT']

    return True, combined_df
