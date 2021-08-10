import pandas as pd
import numpy as np
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from SearchCrawler import coin_list, upbit_reader
from gspread_dataframe import set_with_dataframe
from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup

data = {
  # paste your credentials.json file here
    }

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/176H2IPAMJWXS_QWMnb7OaNSXTShLj4ZD4LtIkqKLp1c/edit#gid=0'

def fetch_upbit_data():
    searchvolume_df = pd.DataFrame()
    searchchanges_df = pd.DataFrame()
    change_15_df = pd.DataFrame()

    for coin in coin_list:
      import datetime
      count = 30
      coin_name = coin['english_name']


      coin_df = upbit_reader(coin['market'], count)

      coin_change_df = upbit_reader(coin['market'], 2, False, 15) # 5분전 대비 상승 비교

      # plt.figure(figsize=(20,8))
      # coin_df['Close'].plot()

      start_date = datetime.datetime.strftime(coin_df['date'][count-1],'%Y-%m-%d')
      end_date = datetime.datetime.strftime(coin_df['date'][0],'%Y-%m-%d')
      date_list = coin_df['date']

      pytrends = TrendReq(hl = 'en-US', tz = 540)
      kw_list = [coin_name]
      pytrends.build_payload(kw_list, timeframe = '{} {}'.format(start_date, end_date), geo = 'US')
      trend_df = pytrends.interest_over_time().reset_index()

      tmp_change_df = pd.DataFrame()

      tmp_change_df['coin'] = [coin_name]
      tmp_change_df['15분봉 상승률'] = [(coin_change_df['trade_price'][0] - coin_change_df['trade_price'][1])/ (coin_change_df['trade_price'][1] + 0.01) *100]
      tmp_change_df['거래량'] = coin_change_df['candle_acc_trade_volume'][0]

      if len(change_15_df) == 0:
          change_15_df = tmp_change_df
      else:
          change_15_df = pd.concat([change_15_df, tmp_change_df])

      if coin_name in list(trend_df.columns):
        merged_df = pd.merge(coin_df, trend_df, how = 'outer')
        # merged_df = pd.merge(coin_df, trend_df)

        tmp_df = pd.DataFrame()
        tmp_df['date'] = merged_df['date']
        tmp_df['coin'] = coin_name
        tmp_df['검색량'] = merged_df[coin_name]
        tmp_df['거래가격'] = merged_df['trade_price']
        tmp_df['거래량'] = merged_df['candle_acc_trade_volume']


        new_df = tmp_df.dropna()[:-1]
        tmp_df_na = tmp_df.dropna()

        tmp_df = tmp_df.fillna('#N/A')

        new_df['검색량 변화'] = np.round((np.array(tmp_df_na['검색량'][:-1]) - np.array(tmp_df_na['검색량'][1:]))/(np.array(tmp_df_na['검색량'][1:])+0.01) * 100, 2)
        new_df['거래가격 변화'] = np.round((np.array(tmp_df_na['거래가격'][:-1]) - np.array(tmp_df_na['거래가격'][1:]))/(np.array(tmp_df_na['거래가격'][1:])+0.01) * 100, 2)
        new_df['거래량 변화'] = np.round((np.array(tmp_df_na['거래량'][:-1]) - np.array(tmp_df_na['거래량'][1:]))/(np.array(tmp_df_na['거래량'][1:])+0.01) * 100, 2)

        if len(searchvolume_df) == 0:
            searchvolume_df = tmp_df
        else:
            searchvolume_df = pd.concat([searchvolume_df, tmp_df])
        if len(searchchanges_df) == 0:
            searchchanges_df = new_df
        else:
            searchchanges_df =  pd.concat([searchchanges_df, new_df])
    return searchvolume_df, searchchanges_df, change_15_df, tmp_df

def fetch_naver_news(tmp_df):
    newsvolume_df = pd.DataFrame()
    for date in tmp_df['date']:
      og_date = date
      date = str(date)[:10]
      date = '.'.join(date.split('-'))

      url = 'https://search.naver.com/search.naver?where=news&query=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&cluster_rank=32&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from19900101to20210810,a:all&start=4000'.format(date,date)
      response = requests.get(url, headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')

      news_count = soup.select('#main_pack > div.api_sc_page_wrap > div > div > a')[-1].text

      tmp_news = pd.DataFrame()

      tmp_news['날짜'] = [og_date]
      tmp_news['뉴스기사 수'] = [news_count]
      if len(newsvolume_df) == 0:
        newsvolume_df = tmp_news
      else:
        newsvolume_df = pd.concat([newsvolume_df, tmp_news])
    return newsvolume_df

def insert_to_spreadsheet(worksheet_name, dataFrame):
    #권한 인증
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(data,scope)
    gc = gspread.authorize(credentials)

    doc = gc.open_by_url(spreadsheet_url)
    #시트 선택
    worksheet = doc.worksheet(worksheet_name)
    doc.values_clear("'"worksheet_name"'")
    set_with_dataframe(worksheet, dataFrame)


def main():
    # upbit 정보 크롤링
    searchvolume_df, searchchanges_df, change_15_df, tmp_df = fetch_upbit_data()
    # 뉴스 정보 크롤링 tmp_df 는 날짜 정보 받아오는 용도
    newsvolume_df = fetch_naver_news(tmp_df)

    # 각각의 시트에 알맞은 정보 삽입

    worksheet_list = ['searchvolume','searchchanges','change_15','newsvolume']
    dataFrame_list = [searchvolume_df, searchchanges_df, change_15_df, newsvolume_df]
    for worksheet_name, dataFrame in zip(worksheet_list, dataFrame_list):
        insert_to_spreadsheet(worksheet_name, dataFrame)
