## 네이버 부동산 데이타 읽어오기 및 시각화 ##

import pandas as pd
import warnings           
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')
warnings.filterwarnings('ignore') 

# df_rates는 여러 페이지에서 수집된 데이터를 통합하여 하나의 데이터프레임으로 만드는 역할
df_rates = pd.DataFrame()
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

# 출력
df_rates = df_rates[::-1]  # df_rates 데이터프레임의 순서를 역순으로
# 데이타 출력하기
print(df_rates)
# 차트 출력하기 (등록일에 따른 '전국', '서울', '수도권'의 데이터)
df_rates.head(30).plot(x = '등록일', y = ['전국','서울','수도권'], figsize=(15,8))
plt.show()


# 미션 1 : 월별 그룹화 추이 분석 
# 미션 2 : 년도별 추이 분석 - 2021년부터 2023년까지 비교
# .py 사용자 정의 함수로 작성하기 

# expand=True 옵션을 사용하면 분리된 문자열들이 새로운 데이터프레임으로 반환
df_temp2 = df_rates['등록일'].str.split('.', expand=True)
df_temp2 = df_temp2.astype(int)

date=['년','월','일']
df_rates[date] = df_temp2

# mission1
mission1 = df_rates.groupby('월')[['월','전국', '서울', '수도권']].mean()
print(mission1)
mission1.head(30).plot(x='월', y=['전국', '서울', '수도권'], figsize=(15, 8))
plt.show()

# mission2
mission2 = df_rates.groupby('년')[['년','전국', '서울', '수도권']].mean()
print(mission2)
mission2.head(30).plot(x='년', y=['전국', '서울', '수도권'], figsize=(15, 8))
plt.show()
