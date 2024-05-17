from PyQt5 import QtGui
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup, PageElement, ResultSet
from requests import request
import requests
import re


DATE_FORMAT = {
    'января': '01',
    'марта': '03',
    'мая': '05',
    'июля': '07',
    'ноября': '11',
    'декабря': '12',
}

def config_font(fonts_size: int) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setFamily('AngelicaC')
    font.setPointSize(fonts_size)
    return font

def parse_holidays() -> dict[str, str]:
    try:
        page = request('GET', 'https://pravo.by/gosudarstvo-i-pravo/gosudarstvennye-prazdniki/').text
    except requests.exceptions.ConnectionError:
        return {}
    soup = BeautifulSoup(page, 'html.parser')
    unwork_days_header: PageElement = soup.find_all('h2')[-1]
    unwork_days_div = unwork_days_header.find_next_sibling('div')
    
    unwork_days: ResultSet[PageElement] = unwork_days_div.find_all('tr')
    
    years = [(datetime.now() + relativedelta(years=i)).year for i in range(-5, 6)]
    
    output_dates = {}
    
    for dates in unwork_days:
        date = dates.find_next('td')
        cleared_date = date.text.strip()
        what = date.find_next_sibling().text.strip()
        
        days = [f'0{value}' if len(value) == 1 else value for value in re.findall(r'\d+', cleared_date)]
        if days:
            month = DATE_FORMAT[cleared_date.split()[-1]]
        else:
            days = ['14']
            month = '05'
        
        for day in days:
            for year in years:
                output_date = datetime(year, int(month), int(day))
                output_dates.update({output_date.strftime('%Y-%m-%d'): what})
    
    return output_dates


def count_weekends(start_date: datetime, end_date: datetime):
    current_date: datetime = start_date
    day_count = 0

    while current_date <= end_date:
        if current_date.weekday() in (5, 6):
            day_count -= 1
        current_date += timedelta(days=1)
        day_count += 1

    return day_count