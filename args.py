import os
import pandas as pd
import pickle
import sys

def new_entry_df(entry_df):
    rows = []
    for racer in  entry_df.iloc[:,:].values:
        no = racer[0]
        name = " ".join(racer[1].split()[:2])
        gen = racer[1].split()[2].split("/")[1]
        machine = racer[1].split()[4].split("/")[0]
        racer3 = racer[3].replace("再", "")
        handi, trial, dev = racer3.split()
        ranks = racer[4].split()
        if len(ranks) == 3:
            rank, pre_rank, point = ranks
        if len(ranks) == 2:
            rank, point = ranks
            pre_rank = "-"
        mean_trail, mean_race, max_race = racer[5].split()
        row = no, name, gen, rank, pre_rank, machine, handi, trial, dev, point, mean_trail, mean_race, max_race
        rows.append(row)

    col = "no", "name", "gen", "rank", "(rank)", "machine", "handi", "trial", "div", "point", "mtri", "mean", "max"

    return pd.DataFrame(rows, columns=col)

def entry(entry_df):    
    racers = []
    for racer in  entry_df.iloc[:,:].values:
        no = racer[0]
        name = "".join(racer[1].split()[:2])
        racer3 = racer[3].replace("再", "")
        handi, trial, dev = racer3.split()
        rank = racer[4].split()[0]
        mean_trial, mean_race, _ = racer[5].split()
        handi = handi.strip("m")
        racer6 = racer[6].split()
        st = racer6[1]
        chakujun = racer6[0][3:8]

        p = "./photos"
        d_files = os.listdir(p)
        files = [f for f in d_files if os.path.isfile(os.path.join(p, f))]
        jpgs = [f for f in files if f.endswith(name + ".jpg")]
        filename = ""
        if len(jpgs) == 1:
            filename = jpgs[0]
        racers.append((int(no), filename, name, rank, int(handi), float(trial), float(dev), \
            float(mean_trial), float(mean_race), float(st), chakujun))

    return racers

if __name__ == '__main__':

    args = sys.argv 

    filename = args[1]
    with open(filename, mode="rb") as f:
        races = pickle.load(f)

    for race in races:
        entry_df = race[1]
        ret = entry(entry_df)
        print(ret)


