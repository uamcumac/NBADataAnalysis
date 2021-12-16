import pandas as pd
import sqlite3

from matplotlib import pyplot as plt

"""
[40%] Your boss would like to know the winning secret from the games in 2020/2021. Please give your finding by 
carefully anaylzing the data in the table “game” of (1) Kaggle basketball dataset. 

For instance, you can say that the winning secret to win a game is to score more than your rival since the 
correlation between the winning status (1) and score more than your rival (1) is always ONE (strongly correlated). 
However, this is definitely a bad idea to tell this fact to your boss. 

After a careful analysis, you may find that the field goal percentage (FG%) (or any other combinations) is the 
winning secret since bilibala bilibala… 

[40%]您的老板想知道2020/2021年奥运会的获胜秘诀。请仔细分析（1）Kaggle basketball数据集“游戏”表中的数据，给出您的发现。
例如，您可以说赢得比赛的秘诀是得分高于对手，因为获胜状态（1）与得分高于对手（1）之间的相关性始终为1（强相关性）。然而，把这个事实告诉你的老板绝对不是一个好主意。
经过仔细分析，你可能会发现球场进球率（FG%）（或任何其他组合）是获胜的秘诀，因为 bilibala bilibala…
"""

"""
column descriptors and equations created via the NBA Stats Glossary, https://www.nba.com/stats/help/glossary/

SEASON_ID: 赛季ID，22020为题目要求的赛季
TEAM_ABBREVIATION: 队名缩写
WL: Win or Loss
MIN: Minutes Played
FGM: Field Goals Made，投中次数
FGA: Field Goals Attempted，尝试投篮数
FG_PCT: Field Goal Percentage，投篮命中率
FTM: Free Throws Made，罚中次数
OREB: Offensive Rebounds，进攻篮板球
"""

con = sqlite3.connect('datasets/basketball.sqlite')
cur = con.cursor()

# SQL select statement using sqlite3 function (returning a list)
cur.execute("SELECT * FROM game")
L = cur.fetchall()
print("List length:", len(L))
# print(L[0])  # print the first record in the table "game"

# SQL select statement using Pandas
# print(str(pd.read_sql_query("SELECT * FROM game WHERE SEASON_ID=22020", con).columns.values).replace(' ', ', '))
df = pd.read_sql_query("SELECT * FROM game WHERE SEASON_ID=22020", con)
pd.set_option('display.max_columns', None)
for i in range(len(df)):
    if df.iloc[i, 7] == 'W':
        df.iloc[i, 7] = 1
    if df.iloc[i, 33] == 'W':
        df.iloc[i, 33] = 1
    if df.iloc[i, 7] == 'L':
        df.iloc[i, 7] = 0
    if df.iloc[i, 33] == 'L':
        df.iloc[i, 33] = 0
    if df.iloc[i, 7] is None:
        df.iloc[i, 7] = -1
    if df.iloc[i, 33] is None:
        df.iloc[i, 33] = -1
df['WL_HOME'] = df['WL_HOME'].astype(int)
df['WL_AWAY'] = df['WL_AWAY'].astype(int)
for i in range(len(df)):
    if df.iloc[i, 7] == -1:
        df.iloc[i, 7] = None
    if df.iloc[i, 33] == -1:
        df.iloc[i, 33] = None
corr = df.corr()
print(corr['WL_HOME'].sort_values(ascending=False))
print(corr['WL_AWAY'].sort_values(ascending=False))