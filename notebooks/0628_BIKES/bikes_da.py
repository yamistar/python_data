# 20240701  전처리
# 모듈안에 펑션 외부에서 호출

def bikes_da() : 
    import streamlit as st
    import pandas as pd
    import seaborn as sns
    import folium
    import matplotlib.pyplot as plt
    plt.rc('font',family='Malgun Gothic')
    import streamlit.components.v1 as components

    @st.cache_data
    def data_preprocessing():
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

    bikes = data_preprocessing()

    tab1, tab2, tab3 = st.tabs(['데이터보기','시간적 분석','인기대여소'])
    with tab1 :
        # st. write("tab1")
        st.dataframe(bikes.head(30))

    with tab2 :
        # st. write("tab2")    
        chart_name = ['요일','일자','대여시간대']

        for i in chart_name :
            #요일별
            fig, ax = plt.subplots(figsize=(15,4))
            ax = sns.countplot(data=bikes, x=i)
            ax.set_title(f"{i} 별 이용건수")
            st.pyplot(fig)

        st.markdown(''' 
                    1. 요일 별 분석
                    * 평일보다 주말에 따릉이 이용건수가 많고
                    * 주말에 있기 있는 대여소 근처에

                    2. 일자 별 분석
                    * 6일
                    * 일회원

                    3. 시간대 별 분석
                    * 출퇴근
                    * 출퇴근
                    ''')
        
        hourly_dayofweek_ride = bikes.pivot_table(index='대여시간대', columns='요일', values='자전거번호', aggfunc='count')
        fig, ax = plt.subplots(figsize=(15, 10))
        ax = sns.heatmap(data=hourly_dayofweek_ride, annot=True, fmt='d')
        st.pyplot(fig)

    with tab3 :
        # st. write("tab3")
        rent_bike = bikes.pivot_table(index=['대여 대여소명','대여점위도','대여점경도'],
                                columns=['주말구분'],
                                values='자전거번호',
                                aggfunc='count')
        weekend_house50 = rent_bike.nlargest(50,'주말')[['주말']].reset_index()

        # 지도의 중심위치를 정한다.
        lat = bikes['대여점위도'].mean()
        lon = bikes['대여점경도'].mean()
        center = [lat, lon]
        map1 = folium.Map(location=center, zoom_start=11)


        for i in weekend_house50.index :
            sub_lat = weekend_house50.loc[i,'대여점위도']
            sub_lon = weekend_house50.loc[i,'대여점경도']
            name = weekend_house50.loc[i,'대여 대여소명']

            folium.Marker(location=[sub_lat,sub_lon],
                        popup=name).add_to(map1)
        st.subheader("주말 인기 대여소 탑50")
        st.caption("주말 인기 있는 대여소 50위를 표시항 것으로 한경변 호수다 공원 근처이다.")

        # 지도 시각화
        components.html(map1._repr_html_(), height=400)

if __name__=="__main__":
    bikes_da()