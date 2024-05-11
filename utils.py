import pandas as pd


def generate_features(df):
    # Generate features
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].apply(lambda x: x.year)
    df['month'] = df['date'].apply(lambda x: x.month)
    df['day'] = df['date'].apply(lambda x: x.day)
    df['day_of_year'] = df['date'].dt.dayofyear
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].apply(lambda x: True if x in [6, 7] else False)

    # encode categories
    df_categories = pd.get_dummies(df['category_id'])
    df_categories.columns = ['category_1', 'category_2', 'category_3']
    df = pd.concat([df, df_categories], axis=1).drop('category_id', axis=1)

    # calculate growing sums
    df['growing_sum_sales_price'] = df.groupby('sku_id')['sales_price'].cumsum()

    return df


def define_holidays(df):
    dates = pd.date_range(start='2017-01-01', end='2021-12-31')

    # Create a pandas Series with dates
    date_series = pd.Series(dates)

    # Define a list of holidays
    years = [2017, 2018, 2019, 2020, 2021]
    ukrainian_holidays = []
    for year in years:
        ukrainian_holidays.extend([
            f'{year}-01-01',  # New Year's Day
            f'{year}-01-07',  # Orthodox Christmas Day
            f'{year}-03-08',  # International Women's Day
            f'{year}-04-17',  # Orthodox Easter Sunday
            f'{year}-04-18',  # Orthodox Easter Monday
            f'{year}-05-01',  # International Workers' Day
            f'{year}-05-09',  # Victory Day over Nazism in World War II
            f'{year}-06-19',  # Trinity Sunday
            f'{year}-06-28',  # Constitution Day
            f'{year}-08-24',  # Independence Day
            f'{year}-10-14',  # Defender of Ukraine Day
            f'{year}-12-25'  # Christmas Day
            ])
    # Create holiday indicators
    holiday_indicators = pd.Series(0, index=date_series.index, name='holidays')
    for holiday in ukrainian_holidays:
        holiday_indicators.loc[date_series.dt.strftime('%Y-%m-%d') == holiday] = 1

    df = pd.merge(holiday_indicators.reset_index(), df, left_on='index', right_on='day_of_year')
    df = df.drop('index', axis=1)
    return df