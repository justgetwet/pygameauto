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

def set_entry(entry_df):
    racers = []
    for racer in  entry_df.iloc[:,:].values:
        no = racer[0]
        name = "".join(racer[1].split()[:2])
        gradu = racer[1].split()[2].split("/")[1].strip("期")
        machine = racer[1].split()[4].split("/")[0]
        team = racer[2].replace(" ", "")
        rank = racer[4].split()[0]
        _trials = racer[3].replace("再", "").split()
        handi = _trials[0]
        trial = _trials[1]
        dev = "0.0"
        if len(_trials) == 3:
            dev = _trials[2]
        mean_trial= racer[5].split()[0]
        mean_time = racer[5].split()[1]
        mean_st = racer[6].split()[1]

        p = "./photos"
        photo_files = os.listdir(p)
        files = [f for f in photo_files if os.path.isfile(os.path.join(p, f))]
        filename = [f for f in files if f.endswith(name + ".jpg")][0]

        tp = no, filename, name, gradu, machine, team, rank, handi, trial, dev, mean_trial, mean_time, mean_st
        racers.append(tp)
        # racers.append((int(no), filename, name, rank, int(handi), float(trial), float(dev), \
        #     float(mean_trial), float(mean_time), float(mean_st))

    return racers

if __name__ == '__main__':

    args = sys.argv 

    filename = args[1]
    with open(filename, mode="rb") as f:
        races = pickle.load(f)

    for race in races:
        entry_df = race[1]
        ret = set_entry(entry_df)
        print(ret)


