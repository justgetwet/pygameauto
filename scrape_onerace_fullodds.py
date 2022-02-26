import time
import requests
import re
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
ua = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}

url_oddspark = "https://www.oddspark.com/autorace"

placeCd_d = {'川口': '02', '伊勢崎': '03', '浜松': '04', '飯塚': '05', '山陽': '06'}
placeEn_d = {'川口': 'kawaguchi', '伊勢崎': 'isesaki', '浜松': 'hamamatsu',
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
    items = tags[0].text.split()
    meta += [item for item in items if item.startswith(
        "天候") or item.startswith("走路状況")]

    return meta


def onerace(dt, place, raceNo):

    place_cd = placeCd_d[place]
    race_url = f"raceDy={dt}&placeCd={place_cd}&raceNo={raceNo}"

    entry_url = url_oddspark + "/RaceList.do?" + race_url

    win_place_url = url_oddspark + "/Odds.do?" + race_url + "&betType=1&viewType=0"
    quinella_url = url_oddspark + "/Odds.do?" + race_url + "&betType=6&viewType=0"
    exacta_url = url_oddspark + "/Odds.do?" + race_url + "&betType=5&viewType=0"
    wide_url = url_oddspark + "/Odds.do?" + race_url + "&betType=7&viewType=0"
    trio_url = url_oddspark + "/Odds.do?" + race_url + "&betType=9&viewType=0"
    odds_urls = [win_place_url, quinella_url, exacta_url, wide_url, trio_url]

    trifecta_url = url_oddspark + "/Odds.do?" + race_url + "&viewType=0&betType=8"

    dfs = get_dfs(entry_url)
    if dfs:
        entry_df = dfs[-1]
        bikes = [str(n) for n in range(1, len(entry_df)+1)]
    else:
        print("no entry!")
        return []

    meta = get_meta(dt, place, entry_url)

    odds = []
    for url in odds_urls:
        dfs = get_dfs(url)
        odds.append(dfs)

    # raceNo=7&viewType=0&betType=8&bikeNo=1&jikuNo=1
    trifectas = []
    for bike in bikes:
        trifecta_bike_url = trifecta_url + f"&bikeNo={bike}&jikuNo=1"
        dfs = get_dfs(trifecta_bike_url)
        trifectas.append(dfs)

    return [meta, entry_df, odds, trifectas]


def odds_d(race):
    win_df = race[2][0][0]
    quin_df = race[2][1][-1]
    exac_df = race[2][2][-1]
    wide_df = race[2][3][-1]
    d = {}
    for row in win_df.values:
        d[str(row[0]) + "w"] = row[2]
    for row in win_df.values:
        d[str(row[0]) + "p1"] = float(row[3].split()[0])
        d[str(row[0]) + "p2"] = float(row[3].split()[2])
    for i, row in enumerate(quin_df.iloc[:, 1::2].values):
        for j, value in enumerate(row):
            if not np.isnan(value):
                key = str(j+1) + "-" + str(i+2)
                d[key] = value
    for i, row in enumerate(exac_df.values[2:, 2:]):
        for j, value in enumerate(row):
            k = str(j+1) + ">" + str(i+1)
            d[k] = float(value)
    for i, row in enumerate(wide_df.values):
        for j, value in enumerate(row[1::2]):
            if type(value) == str:
                key = str(j+1) + "=" + str(i+2)
                d[key] = float(value.split()[0])

    return d


def oddswin(race):
    d = odds_d(race)
    w = [itm[1] for itm in d.items() if itm[0][1] == "w"]
    idx = range(1, len(w)+1)
    sr_w = pd.Series(w, index=idx, name="win")
    p1 = [itm[1] for itm in d.items() if itm[0][1:] == "p1"]
    sr_p1 = pd.Series(p1, index=idx, name="p1")
    p2 = [itm[1] for itm in d.items() if itm[0][1:] == "p2"]
    sr_p2 = pd.Series(p2, index=idx, name="p2")
    srs = []
    for i in idx:
        keys = [str(j) + ">" + str(i) for j in idx]
        vals = [d[key] for key in keys]
        sr = pd.Series(vals, index=idx, name="exa" + str(i))
        srs.append(sr)
    df = pd.DataFrame(srs)
    syn, syn2, syn3, syn4 = [], [], [], []
    for i in range(len(idx)):
        arr = df.iloc[i, :].values
        a = arr[~np.isnan(arr)]
        a2 = np.array(sorted(a)[:2])
        a3 = np.array(sorted(a)[:3])
        a4 = np.array(sorted(a)[:4])
        o = 1/(1/a).sum()
        o2 = 1/(1/a2).sum()
        o3 = 1/(1/a3).sum()
        o4 = 1/(1/a4).sum()
        syn.append(round(o, 1))
        syn2.append(round(o2, 1))
        syn3.append(round(o3, 1))
        syn4.append(round(o4, 1))

    sr_syn = pd.Series(syn, index=idx, name="syna")
    sr_syn2 = pd.Series(syn2, index=idx, name="syn2")
    sr_syn3 = pd.Series(syn3, index=idx, name="syn3")
    sr_syn4 = pd.Series(syn4, index=idx, name="syn4")
    data = [sr_w, sr_p1, sr_p2] + [sr_syn2, sr_syn3, sr_syn4, sr_syn] + srs
    df = pd.concat(data, axis=1)

    return df


if __name__ == '__main__':

    # dt = datetime.now().strftime("%Y%m%d")
    dt = "20220224"
    place = "浜松"
    raceNo = "8"
    race = onerace(dt, place, raceNo)
    df = oddswin(race)
    print(df)

    # filename = "./odds/" + dt + "_" + placeEn_d[place] + "_" + raceNo + "_full_odds.pickle"
    # with open(filename, "wb") as f:
    #     pickle.dump(race, f, pickle.HIGHEST_PROTOCOL)
