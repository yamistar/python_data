## pandas 라이브러리를 사용하여 네이버 환율 정보를 가져오는 프로그램 ## 

import pandas as pd
import warnings           
import matplotlib.pyplot as plt
import streamlit as st

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
warnings.filterwarnings('ignore') 

## 통화코드를 사용하여 네이버 환율 데이타를 가져오는 함수
def get_exchange_rate_data(code, currency_name) :
    df = pd.DataFrame()
    for page_num in range(1, 6) :   
        base_url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"  
        temp = pd.read_html(base_url, encoding='cp949', header=1) 

        df = pd.concat([df, temp[0]]) # 기존의 df에 temp[0] 데이터프레임을 이어 붙여

    # 전체 데이터를 화면에 출력하는 함수 호출
    total_rate_data_view(df, code, currency_name) 


### 수집된 전체 환율 데이터를 조회하고, 시각화하는 함수
def total_rate_data_view(df,code, currency_name) :
    # 원하는 열만 선택 
    df_total = df[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]

    # 1.데이터 출력
    # 스트림릿에서는 프린트가 아니라 라이트다.
    # print(f"=========={currency_name[code_in]} - 단위: {code}===============")
    st.subheader(f"{currency_name} : {code}")
    # print(df.head(20))
    st.dataframe(df.head(20)) # 웹앱에 데이타프레임으로 뿌려준다.

    # 2. 원본 카피 및 plot시각화- 차트 생성
    df_total_chart = df_total.copy()
    df_total_chart = df_total_chart.set_index('날짜')
    df_total_chart = df_total_chart[::-1]  # 데이터 역순으로 정렬
    # 매매기준율 시각화 - 챠트 크기를 바꾸기, 제목 넣기
    ax = df_total_chart['매매기준율'].plot(figsize=(15, 6), title='Exchange rate (환율 변동)')
    fig = ax.get_figure() # 도화지를 만든다?
    # plt.show() #  plt.show()를 호출하여 그래프를 실제로 화면에 표시
    st.pyplot(fig) # 도화지를 웹앱에 뿌린다. 

def exchange_main():
    currency_symbols_name = {'미국 달러':'USD','유로':'EUR','엔화':'JPY'} # 딗셔너리
    
    currency_name = st.selectbox("통화 선택", currency_symbols_name.keys())
    code = currency_symbols_name[currency_name]
    clicked = st.button("환율 데이터 가져오기")
    if clicked : 
        get_exchange_rate_data(code, currency_name)

if __name__=="__main__":
    exchange_main()
