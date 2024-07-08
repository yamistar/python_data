## 네이버 부동산 데이타 읽어오기 및 시각화 ##

import pandas as pd
import warnings
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
warnings.filterwarnings('ignore') 

def collect_data(df_rates):
    # df_rates = pd.DataFrame(df_rates)
    for page_num in range(1, 10):
        base_url = f'https://land.naver.com/news/trendReport.naver?page={page_num}'
        data = pd.read_html(base_url)

        df_ori = data[0]
        df_copy = df_ori.copy()

        df_temp = df_copy['제목'].str.replace('%', '')
        regions = ['전국', '서울', '수도권']
        for region in regions:
            df_temp = df_temp.str.replace(region, "")

        df_temp = df_temp.str.split(']', expand=True)
        df_temp = df_temp[1].str.split(',', expand=True)
        df_temp = df_temp.astype(float)

        df_copy[regions] = df_temp

        df_rate = df_copy[['등록일'] + regions + ['번호']]
        df_rates = pd.concat([df_rates, df_rate])

    # 출력
    df_rates = df_rates[::-1]  # df_rates 데이터프레임의 순서를 역순으로
    # 데이타 출력하기
    print(df_rates)
    # 차트 출력하기 (등록일에 따른 '전국', '서울', '수도권'의 데이터)
    df_rates.head(30).plot(x = '등록일', y = ['전국','서울','수도권'], figsize=(15,8))
    plt.show()
    return df_rates

def mission1(df_rates):
    print('ㅇㅇㅇㅇㅇ')
    print(df_rates)
    df_temp2 = df_rates['등록일'].str.split('.', expand=True)
    df_temp2 = df_temp2.astype(int)

    date=['년','월','일']
    df_rates[date] = df_temp2

    mission1_result = df_rates.groupby('월')[['월', '전국', '서울', '수도권']].mean()
    print(mission1_result)
    mission1_result.head(30).plot(x='월', y=['전국', '서울', '수도권'], figsize=(15, 8))
    plt.show()

def mission2(df_rates):

    mission2_result = df_rates.groupby('년')[['년', '전국', '서울', '수도권']].mean()
    print(mission2_result)
    mission2_result.head(30).plot(x='년', y=['전국', '서울', '수도권'], figsize=(15, 8))
    plt.show()


df_rates = pd.DataFrame()
print("미션 0:")
df_rates = collect_data(df_rates)

print("미션 1: 월별 그룹화 추이 분석")
mission1(df_rates)

print("미션 2: 년도별 추이 분석 (2021년부터 2023년까지 비교)")
mission2(df_rates)
