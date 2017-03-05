import pandas as pd
import numpy as np
import datetime


def daily_job():
    companies = read_config()
    records = read_data(companies)
    print(records)


def read_data(companies):
    records = []
    fields = pd.read_csv(FIELDS_FILE, index_col='company')
    mapping = pd.read_csv(MAPPING_FILE)
    for company, config in companies.items():
        one_row = fields.loc[company]
        date_name = one_row['Date']
        one = pd.read_csv('input-'+company+'/'+config['file'], parse_dates=[date_name], date_parser=lambda x:pd.datetime.strptime(x, config['date']))
        for name, value in one_row.iteritems():
            if name != value:
                one.rename(columns={value: name}, inplace=True)
            if name not in one.columns:
                one[name] = np.nan
        for index, row in one.iterrows():
            if row.name in mapping.index:
                mapping_row = mapping.loc[row.name]
                one.set_value(row.name, 'Security', mapping_row['Label'])
        records.append(one[['Security', 'Date', 'Price', 'Quantity', 'Beta']])
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
FIELDS_FILE = 'fields.csv'
MAPPING_FILE = 'mapping.csv'
daily_job()
