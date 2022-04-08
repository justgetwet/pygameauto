ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import pickle
import re
import requests
import time

from pred import pred30

url_oddspark = "https://www.oddspark.com/autorace"

placeCd_d = {'川口': '02', '伊勢崎': '03', '浜松': '04', '飯塚': '05', '山陽': '06'}
placeEn_d = {'川口': 'kawaguchi', '伊勢崎': 'isesaki', '浜松': 'hamamatsu',\
            '飯塚': 'iiduka', '山陽': 'sanyo'}

def get_dfs(url):
    res = requests.get(url, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    dfs = []
    if soup.find("table"):
        dfs = pd.io.html.read_html(soup.prettify())
    else:
        print(f"it's no table! {url}")
    return dfs

def get_meta(dt, place, entry_url):
    dt_s = dt[:4] + "/" + dt[4:6] + "/" + dt[6:]
    meta = [dt_s, place]
    res = requests.get(entry_url, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    tag = soup.select_one("#RCdata1 span")
    r = tag.text
    tag = soup.select_one("#RCdata2 h3")
    dsc = re.sub("\xa0", "", tag.text.strip())
    meta += [r, dsc]
    tags = soup.select("#RCdata2 .RCdst")
    if tags:
        items = tags[0].text.split()
        meta += [item for item in items if item.startswith("天候") or item.startswith("走路状況")]
        start_time = soup.select_one(".RCstm").text
        meta += [start_time]
    else:
        meta += ["", "", ""]

    return meta

def onerace(dt, place, raceNo):

    place_cd = placeCd_d[place]
    race_url = f"raceDy={dt}&placeCd={place_cd}&raceNo={raceNo}"

    entry_url = url_oddspark + "/RaceList.do?" + race_url

    win_place_url = url_oddspark + "/Odds.do?" + race_url + "&betType=1&viewType=0"
    quinella_url = url_oddspark + "/Odds.do?" + race_url + "&betType=6&viewType=1"
    exacta_url = url_oddspark + "/Odds.do?" + race_url + "&betType=5&viewType=1"
    wide_url = url_oddspark + "/Odds.do?" + race_url + "&betType=7&viewType=1"
    trio_url = url_oddspark + "/Odds.do?" + race_url +  "&betType=9&viewType=1" 
    trifecta_url = url_oddspark + "/Odds.do?" + race_url + "&betType=8&viewType=1"
    odds_urls = [win_place_url, quinella_url, exacta_url, wide_url, trio_url, trifecta_url]
    
    result_url = url_oddspark + "/RaceResult.do?" + race_url

    dfs = get_dfs(entry_url)
    if dfs:
        entry_df = dfs[-1]
        # bikes = list(map(lambda x: str(x), range(1, len(entry_df)+1)))
    else:
        print("no entry!")
        return []

    pred = pred30(entry_df)

    meta = get_meta(dt, place, entry_url)

    odds = []
    for url in odds_urls:
        dfs = get_dfs(url)
        odds.append(dfs)
    
    # result_dfs = get_dfs(result_url)

    return [meta, entry_df, odds, pred]


def odds_update(dt, place, raceNo):

    place_cd = placeCd_d[place]
    race_url = f"raceDy={dt}&placeCd={place_cd}&raceNo={raceNo}"

    entry_url = url_oddspark + "/RaceList.do?" + race_url

    win_place_url = url_oddspark + "/Odds.do?" + race_url + "&betType=1&viewType=0"
    quinella_url = url_oddspark + "/Odds.do?" + race_url + "&betType=6&viewType=1"
    exacta_url = url_oddspark + "/Odds.do?" + race_url + "&betType=5&viewType=1"
    wide_url = url_oddspark + "/Odds.do?" + race_url + "&betType=7&viewType=1"
    trio_url = url_oddspark + "/Odds.do?" + race_url +  "&betType=9&viewType=1" 
    trifecta_url = url_oddspark + "/Odds.do?" + race_url + "&betType=8&viewType=1"
    odds_urls = [win_place_url, quinella_url, exacta_url, wide_url, trio_url, trifecta_url]

    dfs = get_dfs(entry_url)
    if dfs:
        entry_df = dfs[-1]
        # bikes = list(map(lambda x: str(x), range(1, len(entry_df)+1)))
    else:
        print("no entry!")
        return []

    odds = []
    for url in odds_urls:
        dfs = get_dfs(url)
        odds.append(dfs)
    print("odds updated.")

    return [entry_df, odds]

if __name__=='__main__':

    # dt = datetime.now().strftime("%Y%m%d")
    dt = "20220408"
    place = "伊勢崎"
    races = []
    for raceNo in [str(n) for n in range(1,13)]:
        time.sleep(3)
        start = time.time()
        race = onerace(dt, place, raceNo)
        races.append(race)
        print(raceNo, time.time()-start, "sec")

    filename = "./data/" + dt + "_" + placeEn_d[place] + "_" + "data.pickle"
    with open(filename, "wb") as f:
        pickle.dump(races, f, pickle.HIGHEST_PROTOCOL)
