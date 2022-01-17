import requests
from bs4 import BeautifulSoup

def get_weather():
    #ページを取得
    get_menu_web_page=requests.get("https://tenki.jp/forecast/7/34/6910/31201/")
    get_weather_web_page=requests.get("https://tenki.jp/forecast/7/34/6910/31201/1hour.html")
    get_amedas_web_page=requests.get("https://tenki.jp/amedas/7/34/69052.html")
    print("Status_Code:",get_menu_web_page.status_code,",",get_weather_web_page.status_code,",",get_amedas_web_page.status_code)
    menu_soup=BeautifulSoup(get_menu_web_page.text,"html5lib")
    weather_soup=BeautifulSoup(get_weather_web_page.text,"html5lib")
    amedas_soup=BeautifulSoup(get_amedas_web_page.text,"html5lib")
    #ページを解析
    today_weather_img=menu_soup.select_one(".weather-icon").find("img").get("src") #今日の天気の画像
    today_weather=menu_soup.select_one(".weather-telop").string #今日の天気
    temperature_1hour_img=weather_soup.select_one(".temp-graph").find("img").get("src") #1時間ごとの気温の画像
    windy_1hour_img=[]
    windy_1hour=[]
    for windy_24 in weather_soup.select_one(".wind-blow").find_all("img"):
        windy_1hour_img.append(windy_24.get("src")) #１時間ごとの風の画像を取得
        windy_1hour.append(windy_24.get("alt")) #1時間ごとの風の方角を取得
    windy_1hour_speed=[]
    for windy_speed_24 in weather_soup.select_one(".wind-speed").find_all("span"):
        windy_1hour_speed.append(windy_speed_24.string) #1時間ごとの風を取得
    amedas_windy_img=amedas_soup.select_one(".amedas-current-list-wind").find("img").get("src") #現在の風の画像
    amedas_windy_speed=amedas_soup.select_one(".amedas-current-list-wind").contents[3] #現在の風を取得
    amedas_windy_speed=amedas_windy_speed.translate(str.maketrans({"\n":""," ":""}))
    print(today_weather_img,"\n",today_weather,"\n",temperature_1hour_img,"\n",[windy_1hour_img],"\n",[windy_1hour],"\n",[windy_1hour_speed],"\n",amedas_windy_img,"\n",amedas_windy_speed)
    #htmlとして結果を出力
    with open("index.html","w",encoding="utf-8") as index_file:
        head="<head><meta charset='utf-8'><title>Weather Hacker</title><link rel='stylesheet' href='main.css'></head>"
        html_index="<p class='index'>Welcome to Weather Hacker!</p>"
        html_today_weather_img="<img src='"+today_weather_img+"'>"
        html_today_weather="<p class='today_weather'>"+today_weather+"</p>"
        html_temperature_1hour_img="<img src='"+temperature_1hour_img+"'><br>"
        count=0
        html_windy_1hour_img=[]
        html_windy_1hour=[]
        html_windy=[]
        html_windy_1hour_speed=[]
        while count<24:
            html_windy_1hour_img.append("<td><img src='"+windy_1hour_img[count]+"' class='wind_img'>")
            html_windy_1hour.append("<p>"+windy_1hour[count]+"</p>")
            html_windy_1hour_speed.append("<p>"+windy_1hour_speed[count]+"</p></td>")
            html_windy.append(html_windy_1hour_img[count]+html_windy_1hour[count]+html_windy_1hour_speed[count])
            count+=1
        html_amedas_windy_img="<img src='"+amedas_windy_img+"' class='amedas_img'>"
        html_amedas_windy_speed="<span class='amedas'>"+amedas_windy_speed+"</span>"
        body="<body>"+html_index+html_today_weather_img+html_today_weather+html_temperature_1hour_img+"<table><tr><th rowspan='1'>風向<br>風速<br>m/s</th>"+"".join(html_windy)+"</tr></table>"+html_amedas_windy_img+"<br>"+html_amedas_windy_speed+"</body>"
        html="<!doctype html><html>"+head+body+"</html>"
        index_file.write(html)

if __name__=="__main__":
    get_weather()