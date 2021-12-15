# [40%] Your boss would like to know the top-3 players of the best cost–performance ratio in 2020/2021 season,
# where the cost and the performance can be calculated by PERFORMANCE: Efficiency equation based on the statistics in
# the (3) Kaggle 2020/2021 season data. You could replace this equation if there is any better option. COST: Salary
# in table "Player_Salary" of (1) Kaggle basketball dataset. You are welcome to develop any better equation(s) to
# estimate the CP ratio to rank the top-3 players.

# Efficiency equation：
# (PTS + REB + AST + STL + BLK − Missed FG − Missed FT - TO) / GP
# PTS: Points 得分
# REB, OREB, DREB: (Rebound) 篮板, 进攻篮板, 防守篮板
# AST： (Assist缩写) 助攻
# STL: Steals 抢断、断球
# BLK: Blocks 盖帽
# FG: Field Goals 投球命中（次数）/投篮(总称)，包括两分、三分球的投篮
# FT：Free Throws 罚球
# TOV（或TO）: Turnovers 失误次数
# GM, GP; GS: games played; games started

import pandas as pd

df = pd.read_csv('datasets/nba2021_per_game.csv')
top10 = []


def Efficiency(r):
    return r['PTS'] + r['ORB'] + r['DRB'] + r['AST'] + r['STL'] + r['BLK'] - r['FGA'] * (1-r['FG%']) \
           - r['FTA'] * (1-r['FT%']) - r['TOV']


for i in range(len(df)):
    record = df.iloc[i]
    EFF = Efficiency(record)
    print(i, record['Player'], EFF)
