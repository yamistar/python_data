# 파이썬 코드만 들어가는 파일
#pip install pandas

import pandas as pd

# 데이터프레임을 CSV 파일에서 불러옴, 유성우, 도시, 별자리, 달의 위상정보
meteorshowers = pd.read_csv(r"..\..\data\meteorshowers.csv") #  r : 뒤에 경로를 문자로 인식하기
cities = pd.read_csv(r"..\..\data\cities.csv")
constellations = pd.read_csv(r"..\..\data\constellations.csv")
moonphases = pd.read_csv(r"..\..\data\moonphases.csv")


###################################################################################################
### 도시의 위도를 조회하는 함수를 정의
###################################################################################################
def predict_best_shower_viewing(city) :
    latitude = cities.loc[cities['city'] == city,'latitude'].iloc[0]
    return latitude

# 함수 호출 'Abu Dhabi' 입력
incity = input('city >>')
print(predict_best_shower_viewing(incity))


###################################################################################################
### 사용자가 입력한 도시에서 볼 수 있는 별자리를 조회하는 함수를 정의
###################################################################################################
# 정의
def predict_best_shower_viewing(city) :

    shower_string = ""
    if city not in cities.values: 
        shower_string = city + " 현재 예측할 수 없습니다."
        return  shower_string
    
    latitude = cities.loc[cities['city'] == city,'latitude'].iloc[0]

    constellations_list = constellations.loc[(constellations['latitudestart'] >= latitude) \
                                            & (constellations['latitudeend'] <= latitude),'constellation'].tolist()

    if not constellations_list :
        shower_string = city + "에서는 볼 수 있는 유성우가 없습니다."
        return  shower_string

    shower_string = city + "에서 유성우를 볼 수 있습니다."

    return shower_string

# 호출 Abu Dhabi 입력
incity = input('city >>')
print(predict_best_shower_viewing(incity))
