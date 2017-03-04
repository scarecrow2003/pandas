import pandas as pd
import datetime


def daily_job():
    companies = read_config()
    records = read_data(companies)
    print(records)


def read_data(companies):
    records = []
    for company, file in companies.items():
        config = pd.read_csv('input-'+company+'/config.csv')
        one = pd.read_csv('input-'+company+'/'+file, parse_dates=['Date'])
        for index, row in config.iterrows():
            one.rename(columns={row['custom']: row['standard']}, inplace=True)
        records.append(one)
    return records


def read_config():
    config = pd.read_csv(CONFIG_FILE)
    result = {}
    for index, row in config.iterrows():
        date_format = row['date_format']
        today = datetime.datetime.today().strftime(date_format)
        result[row['company']] = row['format'].replace('date', today)
    return result

CONFIG_FILE = 'config.csv'
daily_job()
