import pandas as pd
import numpy as np
import sqlite3

"""
[40%] Your boss would like to know the top-3 players of the best cost–performance ratio in 2020/2021 season,
where the cost and the performance can be calculated by 

PERFORMANCE: Efficiency equation based on the statistics in the (3) Kaggle 2020/2021 season data. 
    You could replace this equation if there is any better option.     
COST: Salary in table "Player_Salary" of (1) Kaggle basketball dataset. 
You are welcome to develop any better equation(s) to estimate the CP ratio to rank the top-3 players.
"""

"""
Efficiency equation：
(PTS + REB + AST + STL + BLK − Missed FG − Missed FT - TO) / GP
PTS: Points 得分
REB, OREB, DREB: (Rebound) 篮板, 进攻篮板, 防守篮板
AST： (Assist缩写) 助攻
STL: Steals 抢断、断球
BLK: Blocks 盖帽
FG: Field Goals 投球命中（次数）/投篮(总称)，包括两分、三分球的投篮
FT：Free Throws 罚球
TOV（或TO）: Turnovers 失误次数
GM, GP; GS: games played; games started
"""


con = sqlite3.connect('datasets/basketball.sqlite')
cur = con.cursor()

# SQL select statement using sqlite3 function (returning a list)
# cur.execute("SELECT * FROM Player_Salary")
# L = cur.fetchall()
# print("List length:", len(L))
# print(L[0])  # print the first record in the table "game"

# SQL select statement using Pandas
# df = pd.read_sql_query("SELECT * FROM game WHERE SEASON_ID=22020", con)
# print("Pandas dataframe size:", len(df))
# print(df.iloc[0])  # print the first record in the table "game" of year 2020

df = pd.read_csv('datasets/nba2021_per_game.csv')

cps = {}
rank = []


def Efficiency(r):
    return r['PTS'] + r['ORB'] + r['DRB'] + r['AST'] + r['STL'] + r['BLK'] - (r['FGA'] - r['FG']) \
           - (r['FTA'] - r['FT']) - r['TOV']


def get_salary(name):
    salarys = pd.read_sql_query("SELECT value FROM Player_Salary WHERE namePlayer = ?", con, params=(name,))
    # print("salarys:", salarys)
    return np.average(salarys) / 1000000 if len(salarys) != 0 else -1


for i in range(len(df)):
    record = df.iloc[i]
    EFF = Efficiency(record)
    salary = get_salary(record['Player'])
    if salary == -1:
        # print(i, 'No salary record of player: {}'.format(record['Player']))
        continue
    name = EFF / salary
    if record['Player'] not in cps.keys():
        cps[record['Player']] = []
    cps[record['Player']].append(name)
    # print(i, record['Player'], "%.5f" % EFF, "%.5f" % salary, "%.5f" % cp)

for name in cps.keys():
    if len(cps[name]) > 1:
        cps[name] = np.average(cps[name])
    rank.append([name, cps[name]])
list.sort(rank, key=lambda x: x[1], reverse=True)
print('the top-3 players are:')
for i in range(3):
    print(*rank[i])
