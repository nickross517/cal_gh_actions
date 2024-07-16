import json 
import pandas as pd
import sqlite3
import logging
from datetime import datetime 
from funcs import currency_convert


file = './data/calendar_data.jl'
log_path = './logs/transformation_logs.log'
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Started transformations for calendar data')

data=[]
with open(file) as f:
    for line in f:
        data.append(json.loads(line))

result = pd.DataFrame()
for json_row in data:
    daily_row = json.loads(json_row)
    created_date = daily_row['data']['asOf']
    df = pd.DataFrame(daily_row['data']['rows'])
    df['created_date'] = created_date
    result = pd.concat([result, df], ignore_index=True)


# reformatting and dropping dupes 
new_col_names = ['last_yr_rpt_date','last_yr_eps','time','ticker','name','market_cap','fiscal_quarter_end','eps_forecast','num_ests','created_date']
result.columns = new_col_names
result = result.drop_duplicates()
result['last_yr_rpt_date'] = pd.to_datetime(result['last_yr_rpt_date'], errors='coerce')
result['created_date'] = pd.to_datetime(result['created_date'], format='%a, %b %d, %Y')

result['last_yr_eps'] = currency_convert(result['last_yr_eps'])
result['market_cap'] = currency_convert(result['market_cap'])
result['eps_forecast'] = currency_convert(result['eps_forecast'])
result['fiscal_quarter_end'] = pd.to_datetime(result['fiscal_quarter_end'], format='%b/%Y') + pd.offsets.MonthEnd(0)
result['pk'] = result['ticker'] + '_' + result['created_date'].astype(str)
logging.info('Transformations successful')

# Upload new data only to table
logging.info('Starting upload to db')
conn = sqlite3.connect('./data/finance.db')
existing_data = pd.read_sql('select pk from fact_earnings_cal', con=conn)
result = result[~result['pk'].isin(existing_data['pk'])]
try:
    if result.empty:
        print('no new records')
        logging.info('No new records uploaded')
    else:
        result.to_sql('fact_earnings_cal', if_exists='append', con=conn, index=False)
    conn.close()
except Exception as e:
    conn.close()
    logging.error(f'Unspecified error {e}')
