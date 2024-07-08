## 네이버 부동산 데이타 읽어오기 및 시각화 ## 강사님 풀이

import pandas as pd
import warnings           
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
warnings.filterwarnings('ignore') 

def get_data() :
    
    df_rates = pd.DataFrame() # df_rates는 여러 페이지에서 수집된 데이터를 통합하여 하나의 데이터프레임으로 만드는 역할
    for page_num in range(1, 10) :
        base_url =f'https://land.naver.com/news/trendReport.naver?page={page_num}'
        data = pd.read_html(base_url)

        df_ori = data[0] # 첫 번째 테이블을 df 데이터프레임에 저장
        df_copy = df_ori.copy() # df_ori의 사본 생성

        # '제목' 데이타 전처리
        df_temp = df_copy['제목'].str.replace('%','') #  '%' 문자 제거

        regions=['전국','서울','수도권'] 
        for region in regions :
            df_temp = df_temp.str.replace(region,"") # ‘전국’, ‘서울’, ‘수도권’을 찾아 제거
        
        df_temp = df_temp.str.split(']', expand=True) # ']'로 분리
        df_temp = df_temp[1].str.split(',', expand=True) # 다시 df_temp[1] 열 ','로 분리
        df_temp = df_temp.astype(float) # 모든 열 float 타입으로 변환 ; 데이터 분석과 시각화를 위해

        df_copy[regions] = df_temp # [‘전국’, ‘서울’, ‘수도권’] list 추가

        # 새로운 데이터프레임에 - 등록일, 전국, 서울, 수도권, 번호 추가
        df_rate = df_copy[['등록일'] + regions + ['번호'] ]
        df_rates = pd.concat([df_rates,df_rate]) # df_rate를 df_rates에 추가

        return df_rates

def total_chart():
    df_rates = get_data
    # 출력
    df_rates = df_rates[::-1]  # df_rates 데이터프레임의 순서를 역순으로
    # 데이타 출력하기
    print(df_rates)
    # 차트 출력하기 (등록일에 따른 '전국', '서울', '수도권'의 데이터)
    df_rates.head(30).plot(x = '등록일', y = ['전국','서울','수도권'], figsize=(15,8))
    plt.show()


# 미션 1 : 월별 그룹화 추이 분석 ?
# 미션 2 : 년도별 추이 분석 - 2021년부터 2023년까지 비교
# .py 사용자 정의 함수로 작성하기 ?

def year_month_chart() :
    df_rates = get_data()
    # 년도를 입력을 받아서 평균을 구해서 데이타 프레임을 만들고 챠트만들기
    df_rates['일자'] = df_rates['일자'].str.replace('-', '').astype('datetime64[ns]')
    
    # df_rates['일자'] = 
    df_rates['월'] = df_rates['일자'].dt.month
    df_rates['년도'] = df_rates['일자'].dt.year

    year_in = int(input("년도 입력>> "))
    df_rates_avg = (df_rates.loc[df_rates["년도"] == year_in].groupby(["년도", "월"])["금리"].mean())
    print(df_rates_avg)

    df_rates_avg.plot(figsize=(15,8), title=('year in Graph'))
    plt.show()


# main
menu = int(input("조회 방법 입력 (1: 전체, 2: 년도/월)>> "))
if menu == 1:
    total_chart()
elif menu == 2:
    year_month_chart()
