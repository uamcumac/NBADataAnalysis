import pandas as pd
import sqlite3

"""
[40%] Your boss would like to know the winning secret from the games in 2020/2021. Please give your finding by 
carefully anaylzing the data in the table “game” of (1) Kaggle basketball dataset. For instance, you can say that the 
winning secret to win a game is to score more than your rival since the correlation between the winning status (1) 
and score more than your rival (1) is always ONE (strongly correlated). However, this is definitely a bad idea to 
tell this fact to your boss. After a careful analysis, you may find that the field goal percentage (FG%) (or any 
other combinations) is the winning secret since bilibala bilibala… 

[40%]您的老板想知道2020/2021年奥运会的获胜秘诀。请仔细分析（1）Kaggle basketball数据集“游戏”表中的数据，给出您的发现。
例如，您可以说赢得比赛的秘诀是得分高于对手，因为获胜状态（1）与得分高于对手（1）之间的相关性始终为1（强相关性）。然而，把这个事实告诉你的老板绝对不是一个好主意。
经过仔细分析，你可能会发现球场进球率（FG%）（或任何其他组合）是获胜的秘诀，因为 bilibala bilibala…
"""

con = sqlite3.connect('datasets/basketball.sqlite')
cur = con.cursor()

# SQL select statement using sqlite3 function (returning a list)
cur.execute("SELECT * FROM game")
L = cur.fetchall()
print("List length:", len(L))
print(L[0])  # print the first record in the table "game"

# SQL select statement using Pandas
df = pd.read_sql_query("SELECT * FROM game WHERE SEASON_ID=22020", con)
print("Pandas dataframe size:", len(df))
print(df.iloc[0])  # print the first record in the table "game" of year 2020
