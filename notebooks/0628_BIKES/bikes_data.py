# 20240701 
# 서울의 공공자전거 대여 데이터를 전처리하는 함수를 정의하고 실행하는 파이썬 스크립트
# 데이타를 전처리하고 모듈안에 펑션을 외부(aischoolmain.py)에서 호출함

def data_preprocessing():
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.rc('font',family='Malgun Gothic')

    # 데이터 불러와서 합치기
    bikes=pd.DataFrame()
    for i in range(3):
        bikes_temp = pd.read_csv(f'data\서울특별시 공공자전거 대여정보_201906_{i+1}.csv', encoding='cp949')
        bikes=pd.concat([bikes,bikes_temp])
    bikes.isnull().sum()  
    bikes['대여일시']=bikes['대여일시'].astype('datetime64[ms]')  

    #파생변수 '요일', '일자', '대여시간대', '주말구분'
    요일 = ['월', '화', '수', '목', '금', '토', '일']
    bikes['요일'] = bikes['대여일시'].dt.day_of_week.apply(lambda x : 요일[x])
    bikes['일자'] = bikes['대여일시'].dt.date
    bikes['일자'] = bikes['대여일시'].dt.day
    bikes['대여시간대'] = bikes['대여일시'].dt.hour # 대여일시에서 시간을 가져와서 대여시일시로 만들겠다
    bikes['주말구분'] = bikes['대여일시'].dt.day_of_week.apply(lambda x : '평일' if x < 5 else '주말')

    #위도, 경도 파일 merge
    bike_shop = pd.read_csv('data\공공자전거 대여소 정보_23_06.csv', encoding='cp949')
    bike_gu = bike_shop[['자치구','대여소번호','보관소(대여소)명','위도','경도']]
    bike_gu = bike_gu.rename(columns={'보관소(대여소)명' : '대여소명'})
    bikes = pd.merge(bikes,bike_gu, left_on='대여 대여소번호', right_on='대여소번호')
    bikes = bikes.drop(['대여소번호','대여소명'],axis=1)
    bikes = bikes.rename(columns={'자치구' : '대여구','위도' : '대여점위도','경도' : '대여점경도'})

    return bikes # bikes 데이타프레임 리턴


# 내가 나를 부를때만 실행된다.
if __name__=='__main__':
    
    # data_preprocessing() # 내 파일에서 부를떄 실행하겠다.
    print(  data_preprocessing() )