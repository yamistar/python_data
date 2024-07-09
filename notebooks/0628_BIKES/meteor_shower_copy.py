# 데이타를 전처리하고 모듈안에 펑션을 외부(aischoolmain.py)에서 호출함

#pip install pandas

import pandas as pd
import streamlit as st

# 데이터프레임을 CSV 파일에서 불러옴, 유성우, 도시, 별자리, 달의 위상정보
meteorshowers = pd.read_csv(r"data\meteorshowers.csv") #  r : 뒤에 경로를 문자로 인식하기
cities = pd.read_csv(r"data\cities.csv")
constellations = pd.read_csv(r"data\constellations.csv")
moonphases = pd.read_csv(r"data\moonphases.csv")


###################################################################################################
### 사용자가 입력한 도시에서 볼 수 있는 유성우 함수를 정의
###################################################################################################
# 정의
def predict_best_shower_viewing(city) :

    shower_string = ""
    if city not in cities.values: 
        shower_string = city + " 현재 예측할 수 없습니다."
        
        return st.write(shower_string)
    
    latitude = cities.loc[cities['city'] == city,'latitude'].iloc[0]

    constellations_list = constellations.loc[(constellations['latitudestart'] >= latitude) \
                                            & (constellations['latitudeend'] <= latitude),'constellation'].tolist()

    if not constellations_list :
        shower_string = city + "에서는 볼 수 있는 유성우가 없습니다."
        st.write(shower_string)
        return

    shower_string = city + "에서 유성우를 볼 수 있습니다."
    st.write(shower_string)
    return

# 호출 Abu Dhabi 입력
def shower_viewing_main():
    city = st.text_input("도시 이름 입력") # 도시 이름 입력받기
    clicked = st.button("유성우 예측하기")
    if clicked and city: 
        result = predict_best_shower_viewing(city)
        st.write(result)

if __name__=="__main__":
    shower_viewing_main()
