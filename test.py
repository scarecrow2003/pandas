import pandas as pd
import datetime


def daily_job():
    companies = read_config()
    records = read_data(companies)
    print(records)


def read_data(companies):
    records = []
    fields = pd.read_csv('fields.csv', index_col='company')
    for company, config in companies.items():
        one = pd.read_csv('input-'+company+'/'+config['file'], parse_dates=['Date'], index_col='Date', date_parser=lambda x:pd.datetime.strptime(x, config['date']))
        one_row = fields.loc[company]
        for name, value in one_row.iteritems():
            if name != value:
                one.rename(columns={value: name}, inplace=True)
        # for column in one_fields:
        #     print(column)
        # for index, row in config.iterrows():
        #     one.rename(columns={row['custom']: row['standard']}, inplace=True)
        records.append(one)
    return records


def read_config():
    config = pd.read_csv(CONFIG_FILE)
    result = {}
    for index, row in config.iterrows():
        date_format = row['date_format']
        today = datetime.datetime.today().strftime(date_format)
        result[row['company']] = {'file': row['format'].replace('date', today), 'date': row['field_date']}
    return result

CONFIG_FILE = 'config.csv'
daily_job()
