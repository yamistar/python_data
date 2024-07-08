import streamlit as st
import pandas as pd

def preprocessing_meteor():
    # 데이터셋 불러오기
    path = '../data/' # 공통 경로
    meteor_showers = pd.read_csv(path + 'meteorshowers.csv')
    moon_phases = pd.read_csv(path + 'moonphases.csv')
    constellations = pd.read_csv(path + 'constellations.csv')
    cities = pd.read_csv(path + 'cities.csv')
    
    # 바꾸고 싶은 월명 딕셔너리 생성
    months = {
    'january' : 1, 'february' : 2, 'march' : 3, 'april' : 4,
    'may' : 5, 'june' : 6, 'july' : 7, 'august' : 8,
    'september' : 9, 'october' : 10, 'november' : 11, 'december' : 12}
    
    # 월명 매핑
    meteor_showers['startmonth'] = meteor_showers['startmonth'].map(months)
    meteor_showers['bestmonth'] = meteor_showers['bestmonth'].map(months)
    meteor_showers['endmonth'] = meteor_showers['endmonth'].map(months)
    
    # 다른 df도 변환
    moon_phases['month'] = moon_phases['month'].map(months)
    constellations['bestmonth'] = constellations['bestmonth'].map(months)

    # startdate 컬럼 추가    
    meteor_showers['startdate'] = pd.to_datetime(2020 * 10000 + 
                                            meteor_showers['startmonth'] * 100 + 
                                            meteor_showers['startday'],
                                            format = '%Y%m%d')
    
    # enddate 컬럼 추가
    meteor_showers['enddate'] = pd.to_datetime(2020 * 10000 + 
                                                meteor_showers['endmonth'] * 100 + 
                                                meteor_showers['endday'],
                                                format = '%Y%m%d')
    
    # date 컬럼 추가
    moon_phases['date'] = pd.to_datetime(2020 * 10000 + 
                                                moon_phases['month'] * 100 + 
                                                moon_phases['day'],
                                                format = '%Y%m%d')
    
    # 달의 위상 백분율로 바꾸기
    phases = {'new moon' : 0, 'first quarter' : 0.5, 'third quarter' : 0.5, 'full moon' : 1}
    moon_phases['percentage'] = moon_phases['moonphase'].map(phases)
    
    # 불필요한 컬럼 삭제
    meteor_showers = meteor_showers.drop(['startmonth', 'startday', 'endmonth', 'endday', 'hemisphere'], axis = 1)
    moon_phases = moon_phases.drop(['month', 'day', 'moonphase', 'specialevent'], axis = 1)
    constellations = constellations.drop('besttime', axis = 1)
    
    # 달의 위상 누락값 처리
    lastphase = 0
    for index, row in moon_phases.iterrows():
        if pd.isnull(row['percentage']):
            moon_phases.at[index, 'percentage'] = lastphase
        else:
            lastphase = row['percentage']

    return meteor_showers, moon_phases, constellations, cities
    
# 도시명을 입력히면 위도를 반환하는 함수
def predict_best_meteor_shower_viewing(city):
    # 전처리가 끝난 데이터 불러오기
    meteor_showers,moon_phases,constellations,cities = [preprocessing_meteor()[i] for i in range(4)]
    # 안내 메시지 초기화
    meteor_shower_string = ''

    # 입력한 도시 정보가 존재하지 않으면 오류 메시지
    if city not in cities.values:
        meteor_shower_string = "아쉽지만 " + city + "에서는 현재 유성우 예측이 어렵습니다."
        return meteor_shower_string
    
    # 도시의 위도 정보를 불러오기
    latitude = cities.loc[cities['city'] == city, 'latitude'].iloc[0]

    # 해당 도시의 위도에서 관측 가능한 별자리 조회
    constellations_list = constellations.loc[(constellations['latitudestart'] >= latitude)&(constellations['latitudeend'] <= latitude), 'constellation'].tolist()


    # 볼 수 있는 별자리가 존재하지 않으면 오류 메시지
    if not constellations_list:
        meteor_shower_string = "아쉽지만 " + city + "에서는 볼 수 있는 별자리가 없습니다."
        return meteor_shower_string
    
    # 별자리 관측 가능 안내 메시지
    meteor_shower_string = city + "에서는 별자리 관측이 가능합니다: \n\n"
    
    # 도시별 관찰 가능한 별자리 iterate
    for constellation in constellations_list:
        # 별자리와 가장 가까운 유성우 조회
        meteor_shower = meteor_showers.loc[meteor_showers['radiant'] == constellation, 'name'].iloc[0]

        # 유성우 관측이 가능한 시작일과 종료일
        meteor_showers_startdate = meteor_showers.loc[meteor_showers['radiant'] == constellation,'startdate'].iloc[0]
        meteor_showers_enddate = meteor_showers.loc[meteor_showers['radiant'] == constellation,'enddate'].iloc[0]

        # 유성우가 보일 때의 달의 위상 조회
        moon_phase_list = moon_phases.loc[(moon_phases['date'] >= meteor_showers_startdate) & (moon_phases['date'] <= meteor_showers_enddate)]

        # 달이 눈에 보이는 첫 날 조회
        best_moon_date = moon_phase_list.loc[moon_phase_list['percentage'].idxmin()]['date']

        # 사용자에게 정보전달
        meteor_shower_string += '\n' + meteor_shower + '를 잘 보려면 ' + constellation + '자리 위치를 향하여 ' + best_moon_date.to_pydatetime().strftime('%B %d, %Y') + '보면 됩니다.\n' 


    return meteor_shower_string

def meteor_main():
    incity = st.text_input('City Input >> ')
    if incity:
        st.write(predict_best_meteor_shower_viewing(incity))
        
if __name__ == '__main__':
    meteor_main()