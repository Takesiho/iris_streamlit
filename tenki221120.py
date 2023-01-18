import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import requests
from bs4 import BeautifulSoup

# タイトルとテキストを記入
st.title('地域の天気を表示します！')
st.write('ゆくゆくは天気と自分の予定から行動予定をレコメンドしたいです')


urls = {
    "東京都小平市": "https://tenki.jp/forecast/3/16/4410/13211/",
    "大阪市住吉区": "https://tenki.jp/forecast/6/30/6200/27120/",
    "富山市": "https://tenki.jp/forecast/4/19/5510/16201/",
    "東京都世田谷区": "https://tenki.jp/forecast/3/16/4410/13112/",
}

def get_weather(url) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    result = {}
    tomorrow_weather_section = soup.select("section.tomorrow-weather")[0]
    result["weather"] = tomorrow_weather_section.select("p.weather-telop")[0].text
    result["high_temp"] = tomorrow_weather_section.select("dd.high-temp > .value")[
        0
    ].text
    result["low_temp"] = tomorrow_weather_section.select(("dd.low-temp > .value"))[
        0
    ].text
    rain_probability = tomorrow_weather_section.select("tr.rain-probability > td")
    result["rain_probability_0006"] = rain_probability[0].text
    result["rain_probability_0612"] = rain_probability[1].text
    result["rain_probability_1218"] = rain_probability[2].text
    result["rain_probability_1824"] = rain_probability[3].text

    return result

areas = ["東京都小平市", "大阪市住吉区", "富山市", "東京都世田谷区"]
select_areas = st.sidebar.selectbox("好きな地域を選んでください", areas)

url = urls.get(select_areas)
result = get_weather(url)

st.write('明日の天気は。。。')
result["weather"]
# result["weather"] = '晴'
# result["weather"] = '雨'
# result["weather"] = '曇'
    
if '晴' in result["weather"]:
    # st.write('晴れやん！！')
    img = Image.open('tennki-illust1.png')
    st.image(img, caption= '晴れ', use_column_width=True)


if '雨' in result["weather"]:
    # st.write('雨でんがな！！')
    img = Image.open('tennki-illust7.png')
    st.image(img, caption= '雨', use_column_width=True)


if '曇' in result["weather"]:
    # st.write('くもり！！')
    img = Image.open('tennki-illust5.png')
    st.image(img, caption= 'くもり', use_column_width=True)
