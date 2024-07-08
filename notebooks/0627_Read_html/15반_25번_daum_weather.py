# 다음 페이지에서 날씨 가져오기

import requests
from bs4 import BeautifulSoup


def get_weather_daum(location) :
    search_query = location + " 날씨"
    base_url = "https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q="
    url = base_url + search_query
 
    html_weather = requests.get(url).text
    soup_weather = BeautifulSoup(html_weather,'lxml')

    txt_temp = soup_weather.select_one('strong.txt_temp').text
    txt_weather = soup_weather.select_one('span.txt_weather').text
    dl_weather = soup_weather.select('dl.dl_weather dd')
    [wind_speed, humidity, pm10] = [x.text for x in dl_weather]

    return txt_temp, txt_weather, wind_speed, humidity, pm10  # 함수의 리턴 값 5개

#location = '한남동'
location = input("조회할 동입력>>")
xt_temp, txt_weather, wind_speed, humidity, pm10 = get_weather_daum(location) # 함수의 리턴 값 5개와 동일하게 호춣야 함
print("---- 오늘의 날씨정보 -----")
print(f'설정 지역 : {location}')
print(f'현재 기온 : {xt_temp}')
print(f'기상 상태 : {txt_weather}')
print(f'현재풍속 : {wind_speed}, 현재습도 : {humidity}, 미세먼지 : {pm10}')