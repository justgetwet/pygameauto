ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import re
import requests

def get_dfs(url):
    res = requests.get(url, headers=ua)
    soup = BeautifulSoup(res.content, "html.parser")
    dfs = []
    if soup.find("table"):
        dfs = pd.io.html.read_html(soup.prettify())
    else:
        print(f"it's no table! {url}")
    return dfs

playerdetail = "https://www.oddspark.com/autorace/PlayerDetail.do?playerCd="

p_temp = Path("./photos/")
filenames = [p.name.strip(".jpg") for p in p_temp.iterdir() if p.is_file()]
racercode_d = {f.split("_")[1]: f.split("_")[0] for f in filenames}

def pred30(entry_df):
    
    items = [item.replace("\u3000", " ") for item in entry_df.iloc[:,1].values]
    racers = ["".join(item.split()[:2]) for item in items]
    handis = [float(item.split()[0].strip("m"))/1000 for item in entry_df.iloc[:,3].values]

    time_data = []
    time_last5 = []
    for racer, handi in zip(racers, handis):
        url = playerdetail + racercode_d[racer]
        dfs = get_dfs(url)
        df = [df for df in dfs if len(df.columns) == 12][0]
        times = []
        for row in df.itertuples():
            race_time = 0
            if type(row[7]) == str and row[7][0] == "良" and row[9] != "-":
                if type(row[9]) == str: 
                    race_time = float(re.sub("再| ","", row[9]))
                else:
                    race_time = row[9]
            if race_time:
                times.append(race_time)  
        data = np.array(times) + handi
        time_data.append(data)
        time_last5.append(data[:5])
    
    rens, wins, places = [], [], []
    for _ in range(8000):
        last5_times = [np.random.choice(times) for times in time_last5]
        l = min(last5_times)
        l_indexes = [i+1 for i, x in enumerate(last5_times) if x == l]
        l = np.random.choice(l_indexes)

        race_times = [np.random.choice(times) for times in time_data]
        m = min(race_times)
        w_indexes = [i+1 for i, x in enumerate(race_times) if x == m]
        w = np.random.choice(w_indexes)
        
        race_times[w-1] = 3.9 # dummy
        n = min(race_times)
        p_indexes = [i+1 for i, x in enumerate(race_times) if x == n]
        p = np.random.choice(p_indexes)
        
        rens.append(l)
        wins.append(w)
        places.append(p)
        
    l_hist, _  = np.histogram(rens, bins=range(1, len(time_last5)+2))
    l_rates = 100 * l_hist / l_hist.sum()
    w_hist, _  = np.histogram(wins, bins=range(1, len(time_data)+2))
    w_rates = 100 * w_hist / w_hist.sum()
    p_hist, _  = np.histogram(places, bins=range(1, len(time_data)+2))
    p_rates = 100 * p_hist / p_hist.sum()

    res = []
    for i, (l, w, p) in enumerate(zip(l_rates, w_rates, p_rates)):
        res.append((i+1, l, w, p))
        
    return res

if __name__ == "__main__":

    filename = "data/20220407_isesaki_data.pickle"
    with open(filename, mode="rb") as f:
        races = pickle.load(f)

    entry_df = races[1][1]
    res = pred30(entry_df)
    for tp in res:
        print(tp)