## 다음(Daum) 웹사이트에서 특정 지역의 날씨 정보를 가져오는 함수와 이를 활용하는 예제

import requests
from bs4 import BeautifulSoup

# 다음(Daum) 웹사이트에서 특정 지역의 날씨 정보를 가져오는 함수
# location (str): 날씨 정보를 조회할 지역 이름
def get_weather_daum(location) :

    search_query = location + " 날씨"
    base_url = "https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q="
    url = base_url + search_query

    html_weather = requests.get(url).text
    soup_weather = BeautifulSoup(html_weather,'lxml')

    txt_temp = soup_weather.select_one('strong.txt_temp').text
    txt_weather = soup_weather.select_one('span.txt_weather').text
    dl_weather = soup_weather.select('dl.dl_weather dd') # dl_weather는 파싱된 HTML에서 추출한 <dd> 요소들의 리스트
    [wind_speed, humidity, pm10] = [x.text for x in dl_weather] # 리스트 컴프리헨션은 [] 안에 반복문과 조건문을 넣어 리스트의 각 요소를 생성

    return txt_temp, txt_weather, wind_speed, humidity, pm10  # 함수의 리턴 값 5개

# location = '한남동'  # 특정 지역을 직접 설정할 수도 있음
location = input("조회할 동입력>>")
xt_temp, txt_weather, wind_speed, humidity, pm10 = get_weather_daum(location) # 함수의 리턴 값 5개와 동일하게 호춣야 함
print("---- 오늘의 날씨 정보 -----")
print(f'설정 지역 : {location}')
print(f'현재 기온 : {xt_temp}')
print(f'기상 상태 : {txt_weather}')
print(f'현재 풍속 : {wind_speed}, 현재 습도 : {humidity}, 미세먼지 농도 : {pm10}')