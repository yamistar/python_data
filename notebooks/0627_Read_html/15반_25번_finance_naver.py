## pandas 라이브러리를 사용하여 네이버 환율 정보를 가져오는 프로그램 ## crawlling0627.ipynb

import pandas as pd
import warnings           
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
warnings.filterwarnings('ignore') 

# 통화코드를 사용하여 네이버 환율 데이타를 가져오는 함수
def get_exchange_rate_data(code) :
    df = pd.DataFrame()
    for page_num in range(1, 11) :   
        base_url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"  
        temp = pd.read_html(base_url, encoding='cp949', header=1) 
        df = pd.concat([df, temp[0]]) 

    # 전체 데이터를 화면에 출력하는 함수 호출
    total_rate_data_view(df) 

# 수집된 전체 환율 데이터를 시각화하고 데이터를 조회
def total_rate_data_view(df) :
    # 원하는 열만 선택 
    df_total = df[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]
    # 데이터 표시
    print(f"=========={currency_name[code_in]} - 단위: {code}===============")
    print(df.head(20))

    # 차트 작성  - 원본 카피
    df_total_chart = df_total.copy()
    df_total_chart = df_total_chart.set_index('날짜')
    # 매매기준율의 정열 순서 바꾸기
    df_total_chart = df_total_chart[::-1] 
    # 챠트 크기를 바꾸기, 제목 넣기, 한글인식
    df_total_chart['매매기준율'].plot(figsize=(15, 6), title='Exchange rate')
    plt.show()
    month_rate_data_view(df)

# 월별 데이터를 조회하고 시각화하는 함수
def month_rate_data_view(df_total) :
    # 날짜 열을 datetime 형식으로 변환하고 인덱스로 설정
    df_total['날짜'] = df_total['날짜'].str.replace(".","").astype('datetime64[ms]')
    df_total['월'] = df_total['날짜'].dt.month
    # 임의월 입력 받기
    month_in = int(input("검색할 월 입력>>>"))
    month_df = df_total.loc[df_total['월']==month_in, ['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]
    month_df = month_df.reset_index(drop=True)

    print(f"=========={currency_name[code_in]} - 단위: {code}===============")
    print(month_df.head(20))

    # 복사 해두기
    month_df_chart = month_df.copy()
    month_df_chart = month_df_chart.set_index('날짜')
    month_df_chart['매매기준율'].plot(figsize=(15, 6))
    plt.show()

# 사용자 입력으로 통화 유형을 입력 받음
code_in = int(input("통화 유형 선택하라 (0:USD, 1:EUR, 2:JPY)"))
currency_symbols = ['USD','EUR','JPY'] 
currency_name = ['미달러','유로','엔화'] 
code = currency_symbols[code_in]
get_exchange_rate_data(code)

