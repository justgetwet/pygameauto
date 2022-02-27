import numpy as np
import pandas as pd
import warnings
warnings.simplefilter('ignore', category=RuntimeWarning)

from scrape_onerace_fullodds import onerace

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
        arr = df.iloc[:, i].values
        nonans = arr[~np.isnan(arr)]
        a = [n for n in nonans if n != 0.]
        a_all = np.array(a)
        a2 = np.array(sorted(a)[:2])
        a3 = np.array(sorted(a)[:3])
        a4 = np.array(sorted(a)[:4])
        o_all = 1/(1/a_all).sum()
        o2 = 1/(1/a2).sum()
        o3 = 1/(1/a3).sum()
        o4 = 1/(1/a4).sum()
        syn.append(round(o_all, 1))
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

    race = onerace("20220227", "川口", "12")
    df = oddswin(race)
    print(df)