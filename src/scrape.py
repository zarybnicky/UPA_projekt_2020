import csv
from datetime import date, datetime
import os
import time

from dateutil.relativedelta import relativedelta
import requests

DEBUG = False

def scrape(base_url, output_dir, start_date, end_date):
    for ordinal in range(start_date.toordinal(), end_date.toordinal()):
        url = base_url + date.fromordinal(ordinal).strftime('%d.%m.%Y')
        path = date.fromordinal(ordinal).strftime('%Y-%m-%d') + '.txt'
        filename = os.path.join(output_dir, path)
        if os.path.isfile(filename):
            continue
        print("Requesting %s..." % url, end='')
        try:
            request = requests.get(url)
            if not request.text:
                print(' Empty!')
                continue
            print(' OK')
            with open(filename, 'w') as handle:
                handle.write(request.text)
            time.sleep(0.3)
        except Exception as ex:
            print(' %s' % ex)
            continue


def parse(input_dir):
    for name in os.listdir(input_dir):
        path = os.path.join(input_dir, name)
        if not os.path.isfile(path):
            continue
        yield from parse_file(path)


def parse_file(path):
    day = None
    with open(path, 'r') as handle:
        for line in csv.reader(handle, delimiter="|"):
            if len(line) == 1:
                day = datetime.strptime(line[0].split(' ')[0], "%d.%m.%Y")
            elif line != ['země', 'měna', 'množství', 'kód', 'kurz']:
                yield {
                    'date': day,
                    'currency': {
                        'country': line[0],
                        'name': line[1],
                        'code': line[3],
                    },
                    'lotSize': line[2],
                    'price': line[4],
                }


if __name__ == '__main__':
    scrape_dir = 'scraped/'
    if not os.path.isdir(scrape_dir):
        os.mkdir(scrape_dir)

    scrape(
        base_url='https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date=',
        start_date=datetime.today() - relativedelta(months=4),
        end_date=datetime.today(),
        output_dir=scrape_dir,
    )

    
    for data in parse(scrape_dir):
        if DEBUG:
            print(data)
