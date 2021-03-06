# coding: UTF-8
# pySerialのInstallが必要
import serial
import datetime
import urllib
import urllib.request
import requests
# COM5を開く windows用
s = serial.Serial("COM5", 115200)

# Mac用
#s = serial.Serial("/dev/tty.usbserial-MW1IQ8BN", 115200)

# センサーの閾値
sensor = 1000

room1DiviceId = "10e27d0"
room1CurrentStatus = False
room1BeforeStatus = False

while 1:
    # 1行読み取る
    data = s.readline()
    # 「;」で分割する
    m = str(data).split(";")
    if (len(m) == 13):
        if m[5] == "10e27d0":
            if int(m[9]) < sensor:
                room1CurrentStatus = False
                if room1BeforeStatus != room1CurrentStatus:
                    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S ")
                    print(timestamp + " " + m[5] + ": is opened !")
                    # 取得した値を変数に格納
                    comp_id = 1  # ここをusbから取得した値にしたい
                    status = 'N'  # ここをusbから取得した値にしたい
                    wc_status = {'g_id': comp_id, 'g_status': status}
                    # httpプロトコルでpost通信
                    response = requests.post(
                        'http://localhost/wc_get.php', params=wc_status)
                    print(response.text)  # レスポンスのHTMLを文字列で取得
                    room1BeforeStatus = room1CurrentStatus
            elif int(m[9]) > sensor:
                room1CurrentStatus = True
                if room1BeforeStatus != room1CurrentStatus:
                    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S")
                    print(timestamp + " " + m[5] + ": is closed !")
                    # 取得した値を変数に格納
                    comp_id = 1  # ここをusbから取得した値にしたい
                    status = 'Y'  # ここをusbから取得した値にしたい
                    wc_status = {'g_id': comp_id, 'g_status': status}
                    # httpプロトコルでpost通信
                    response = requests.post(
                        'http://localhost/wc_get.php', params=wc_status)
                    print(response.text)  # レスポンスのHTMLを文字列で取得
                    room1BeforeStatus = room1CurrentStatus
        #print ("送信元シリアル番号："+m[5]+" / 送信元電源電圧："+m[6]+" / センサー電流："+m[9])
s.close()
