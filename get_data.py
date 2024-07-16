import requests
import json
import logging
from datetime import datetime

log_path = './logs/extract_logs.log'
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
urls = [
{'url':'https://api.nasdaq.com/api/calendar/earnings','path':'calendar'}, 
{'url':'https://api.nasdaq.com/api/ipo/calendar','path':'ipo'}
]

headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.8',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
def get_data(url, path_info):
    data_path = f'./data/{path_info}_data.jl'
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        logging.info(f'Successful request to {url} at {datetime.now()}')
        with open(data_path,'a') as f:
            json.dump(r.text,f)
            f.write('\n')
            logging.info(f'Wrote to file at {datetime.now()}')
    except requests.RequestException as e:
        logging.error(f'Request to {url} failed at {datetime.datetime.now()}, {str(e)}')
    except Exception as e:
        logging.error(f'Unspecified error {str(e)}')

if __name__ == '__main__':
    for url in urls:
        get_data(url['url'], path_info=url['path'])
