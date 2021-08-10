import requests
import pandas as pd

def upbit_reader(market, count, days = True, minutes = 5):
  import datetime
  if days:
      url = "https://api.upbit.com/v1/candles/days"
  else:
      url = "https://api.upbit.com/v1/candles/minutes/{}".format(minutes)

  querystring = {"market": market,"count":count}

  headers = {"Accept": "application/json"}

  response = requests.request("GET", url, headers=headers, params=querystring)

  upbit_df = pd.DataFrame(response.json())
  upbit_df['date'] = upbit_df['candle_date_time_utc'].apply(lambda x : datetime.datetime.strptime(str(x).split('T')[0],'%Y-%m-%d'))


  return upbit_df

coin_list = [{'english_name': 'Bitcoin', 'korean_name': '비트코인', 'market': 'KRW-BTC'},
 {'english_name': 'Ethereum', 'korean_name': '이더리움', 'market': 'KRW-ETH'},
 {'english_name': 'Ethereum Classic',
  'korean_name': '이더리움클래식',
  'market': 'KRW-ETC'},
 {'english_name': 'Waves', 'korean_name': '웨이브', 'market': 'KRW-WAVES'},
 {'english_name': 'Qtum', 'korean_name': '퀀텀', 'market': 'KRW-QTUM'},
 {'english_name': 'Lisk', 'korean_name': '리스크', 'market': 'KRW-LSK'},
 {'english_name': 'Lumen', 'korean_name': '스텔라루멘', 'market': 'KRW-XLM'},
 {'english_name': 'Ada', 'korean_name': '에이다', 'market': 'KRW-ADA'},
 {'english_name': 'EOS', 'korean_name': '이오스', 'market': 'KRW-EOS'},
 {'english_name': 'TRON', 'korean_name': '트론', 'market': 'KRW-TRX'},
 {'english_name': 'Siacoin', 'korean_name': '시아코인', 'market': 'KRW-SC'},
 {'english_name': 'Ontology', 'korean_name': '온톨로지', 'market': 'KRW-ONT'},
 {'english_name': 'Zilliqa', 'korean_name': '질리카', 'market': 'KRW-ZIL'},
 {'english_name': 'Polymath', 'korean_name': '폴리매쓰', 'market': 'KRW-POLY'},
 {'english_name': 'Bitcoin Cash',
  'korean_name': '비트코인캐시',
  'market': 'KRW-BCH'},
 {'english_name': 'Basic Attention Token',
  'korean_name': '베이직어텐션토큰',
  'market': 'KRW-BAT'},
 {'english_name': 'Civic', 'korean_name': '시빅', 'market': 'KRW-CVC'},
 {'english_name': 'GAS', 'korean_name': '가스', 'market': 'KRW-GAS'},
 {'english_name': 'Bitcoin SV',
  'korean_name': '비트코인에스브이',
  'market': 'KRW-BSV'},
 {'english_name': 'BitTorrent', 'korean_name': '비트토렌트', 'market': 'KRW-BTT'},
 {'english_name': 'Decentraland',
  'korean_name': '디센트럴랜드',
  'market': 'KRW-MANA'},
 {'english_name': 'Ankr', 'korean_name': '앵커', 'market': 'KRW-ANKR'},
 {'english_name': 'Cosmos', 'korean_name': '코스모스', 'market': 'KRW-ATOM'},
 {'english_name': 'Hedera Hashgraph',
  'korean_name': '헤데라해시그래프',
  'market': 'KRW-HBAR'},
 {'english_name': 'VeChain', 'korean_name': '비체인', 'market': 'KRW-VET'},
 {'english_name': 'Chainlink', 'korean_name': '체인링크', 'market': 'KRW-LINK'},
 {'english_name': 'Tezos', 'korean_name': '테조스', 'market': 'KRW-XTZ'},
 {'english_name': 'JUST', 'korean_name': '저스트', 'market': 'KRW-JST'},
 {'english_name': 'Crypto.com Chain',
  'korean_name': '크립토닷컴체인',
  'market': 'KRW-CRO'},
 {'english_name': 'Swipe', 'korean_name': '스와이프', 'market': 'KRW-SXP'},
 {'english_name': 'Polkadot', 'korean_name': '폴카닷', 'market': 'KRW-DOT'},
 {'english_name': 'Bitcoin Cash ABC',
  'korean_name': '비트코인캐시에이비씨',
  'market': 'KRW-BCHA'},
 {'english_name': 'Dogecoin', 'korean_name': '도지코인', 'market': 'KRW-DOGE'},
 {'english_name': 'Flow', 'korean_name': '플로우', 'market': 'KRW-FLOW'}]
