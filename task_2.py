import pandas as pd
import sqlite3

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

"XXXX" for "HOME" or "AWAY"
WL_XXXX: Win or Loss
PLUS_MINUS_XXXX: The point differential when a player or team is on the floor
XXXX_TEAM_WINS: ? - The number of games won by a player or team
XXXX_TEAM_LOSSES: ? - The number of games lost by a player or team
PTS_XXXX: Points, The number of points scored
PTS_XXXX_y: ?
FG_PCT_XXXX: ? - 2 and 3 Point Field Goal Percentage, The percentage of 2 and 3 point field goal attempts of a specified criteria that a player or team makes
FGM_XXXX: Field Goals Made, The number of field goals that a player or team has made. This includes both 2 pointers and 3 pointers
FG3_PCT_XXXX: 3 Point Field Goal Percentage, The percentage of 3 point field goal attempts of a specified criteria that a player or team makes

"""

con = sqlite3.connect('datasets/basketball.sqlite')
cur = con.cursor()

# SQL select statement using sqlite3 function (returning a list)
cur.execute("SELECT * FROM game")
L = cur.fetchall()

# SQL select statement using Pandas
df = pd.read_sql_query("SELECT * FROM game WHERE SEASON_ID=22020", con)
pd.set_option('display.max_columns', None)  # 设置输出列数不受限
for i in range(len(df)):  # 将胜负结果设为1或0
    if df.iloc[i, 7] == 'W':
        df.iloc[i, 7] = 1
    if df.iloc[i, 33] == 'W':
        df.iloc[i, 33] = 1
    if df.iloc[i, 7] == 'L':
        df.iloc[i, 7] = 0
    if df.iloc[i, 33] == 'L':
        df.iloc[i, 33] = 0
    if df.iloc[i, 7] is None:  # 无胜负结果的先置-1，不然下面转格式会报错
        df.iloc[i, 7] = -1
    if df.iloc[i, 33] is None:
        df.iloc[i, 33] = -1
df['WL_HOME'] = df['WL_HOME'].astype(int)
df['WL_AWAY'] = df['WL_AWAY'].astype(int)
for i in range(len(df)):  # 再把无结果的转回去
    if df.iloc[i, 7] == -1:
        df.iloc[i, 7] = None
    if df.iloc[i, 33] == -1:
        df.iloc[i, 33] = None

pearsonHome = df.corr()['WL_HOME'].sort_values(ascending=False)  # 默认使用pearson相关系数
homeRow = pearsonHome.index.tolist()
homeValue = pearsonHome.values.tolist()
pearsonAway = df.corr()['WL_AWAY'].sort_values(ascending=False)  # 默认使用pearson相关系数
awayRow = pearsonAway.index.tolist()
awayValue = pearsonAway.values.tolist()

homeStrong = []
homeMid = []
awayStrong = []
awayMid = []

for i in range(len(homeRow)):
    if 1 > homeValue[i] >= 0.5:
        homeStrong.append({homeRow[i]: round(homeValue[i], 3)})
    if 0.5 > homeValue[i] >= 0.3:
        homeMid.append({homeRow[i]: round(homeValue[i], 3)})
    if 1 > awayValue[i] >= 0.5:
        awayStrong.append({awayRow[i]: round(awayValue[i], 3)})
    if 0.5 > awayValue[i] >= 0.3:
        awayMid.append({awayRow[i]: round(awayValue[i], 3)})

print('For home team:')
print("\tStrong correlation between win:")
print('\t\t' + str(homeStrong).replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('\'', ''))
print("\tModerate correlation between win:")
print('\t\t' + str(homeMid).replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('\'', ''))
print('\nFor away team:')
print("\tStrong correlation between win:")
print('\t\t' + str(awayStrong).replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('\'', ''))
print("\tModerate correlation between win:")
print('\t\t' + str(awayMid).replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('\'', ''))
