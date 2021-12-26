'''
[20% / 30%] Name the most important player in each team.
You could simply use the result in Task 1 but you may just get the basic mark (<20%) of this question.
If you only use datasets (1) and (3) to answer this task, the highest mark is 20%.
You could try to analyze the data in the (2) NBA Basketball Datasets that provides the most detail actions in every game.
You will get (up to) 30% if you successfully run your analysis on this dataset.

您可以简单地使用任务 1 中的结果，但您可能只会获得此问题的基本分数 (<20%)。
如果只用数据集（1）和（3）来回答这个任务，最高分是20%。
您可以尝试分析 (2) NBA Basketball Datasets 中的数据，这些数据集提供了每场比赛中最详细的动作。如果您成功地对该数据集运行分析，您将获得（最多）30%
'''
'''
'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%',
       'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'
'球员', '位置', '年龄', '球队', '出场次数', '首发出场次数', '出场时间', '命中次数', '出手次数', '命中率', '三分球命中', '三分球出手', '三分球命中率', '两分球命中', '两分球出手', '两分球命中率', '真实命中率',
       '罚球命中', '罚球次数', '罚球命中率', '进攻篮板', '防守篮板', '总篮板', '助攻', '抢断', '盖帽', '失误', '犯规', '得分'
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('datasets/nba2021_per_game.csv')
column = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA',
       'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%',
       'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
       'PF', 'PTS']
data.columns = column

import matplotlib.pyplot as plt
x = data['Tm'].value_counts().index
y = data['Tm'].value_counts().values

plt.figure(figsize=(13,5))
plt.bar(x,y)
plt.title("Number of players in each team")
plt.xlabel('team')
plt.ylabel('number')
# plt.savefig('Number of players in each team.png',dpi=600)

# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
def fun(team,Player):
    data1 = data.loc[data['Tm']==team]
    lanban = data1['TRB']
    zhugong = data1['AST']
    defen = data1['PTS']
    sanfen = data1['3P']
    toulan = data1['2P%']
    gaimao = data1['BLK']
    qiangduan = data1['STL']
    lanban_max = max(lanban)
    zhugong_max = max(zhugong)
    defen_max = max(defen)
    sanfen_max = max(sanfen)
    toulan_max = max(toulan)
    gaimao_max = max(gaimao)
    qiangduan_max = max(qiangduan)
    x = np.array(data1.loc[data1['Player'] == Player][['TRB','AST','PTS',
                                                    '3P','2P%','BLK','STL']])[0]
    keys = ['TRB','AST','PTS','3P','2P%','BLK','STL']
    values = [x[0]/lanban_max*100,x[1]/zhugong_max*100,
            x[2]/defen_max*100,x[3]/sanfen_max*100,x[4]/toulan_max*100
            ,x[5]/gaimao_max*100,x[6]/qiangduan_max*100]
    results = dict(zip(keys, values))
    data_length = len(results)
    # 将极坐标根据数据长度进行等分
    angles = np.linspace(0, 2*np.pi, data_length, endpoint=False)
    labels = [key for key in results.keys()]
    score = [v for v in results.values()]
    # 使雷达图数据封闭
    score_a = np.concatenate((score, [score[0]]))
    score_b = np.concatenate((score, [score[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    labels = np.concatenate((labels, [labels[0]]))
    # 设置图形的大小
    fig = plt.figure(figsize=(8, 6), dpi=100)
    # 新建一个子图
    ax = plt.subplot(111, polar=True)
    # 绘制雷达图
    ax.plot(angles, score_a, color='g')
    ax.plot(angles, score_b, color='b')
    # 设置雷达图中每一项的标签显示
    ax.set_thetagrids(angles*180/np.pi, labels)
    # 设置雷达图的0度起始位置
    ax.set_theta_zero_location('N')
    # 设置雷达图的坐标刻度范围
    ax.set_rlim(0, 100)
    # 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
    ax.set_rlabel_position(270)
    ax.set_title(Player)
    ax.fill(angles,score_a, alpha=0.4)
    plt.savefig(Player+'.png',dpi=300)
    plt.show()
    return values

score = []
for i in data['Tm'].value_counts().index:
    for j in data.loc[data['Tm']==i]['Player'].values:
        score.append(fun(i,j))

player = pd.DataFrame(score,columns=['TRB','AST','PTS',
        '3P','2P%','BLK','STL'])
Player = []
team = []
for i in data['Tm'].value_counts().index:
    for j in data.loc[data['Tm']==i]['Player'].values:
        Player.append(j)
        team.append(i)
player['Player'] = Player
player['Tm'] = team
player['G'] = player['Player'].map(dict(zip(data['Player'].values,data['G'].values)))
player['GS'] = player['Player'].map(dict(zip(data['Player'].values,data['GS'].values)))
player['MP'] = player['Player'].map(dict(zip(data['Player'].values,data['MP'].values)))

Team = []
bestplayer = []
for i in data['Tm'].value_counts().index:
    test = player.loc[player['Tm'] == i]
    test['G'] = test['G']/test['G'].max()*100
    test['GS'] = test['GS']/test['GS'].max()*100
    test['MP'] = test['MP']/test['MP'].max()*100
    test['Weighted total score'] = test[['TRB','AST','PTS',
          '3P','2P%','BLK','STL','G','MP','GS']].sum(axis = 1)
    test = test.sort_values(by = 'Weighted total score',ascending=0)
    Team.append(i)
    bestplayer.append(test['Player'].values[0])
    print("Team：",i,"  The most important player：",test['Player'].values[0])
    # test.to_csv('Tm'+i+'球员数据总得分.csv',index = 0)
data_best = pd.DataFrame(Team,columns = ['Tm'])
data_best['Player'] = bestplayer
# data_best.to_csv('各队最重要的球星.csv',index = 0)

import sqlite3 as sql
conn = sql.connect('datasets/basketball.sqlite') # create connection object to database
df = pd.read_sql('select * from Player_Salary', conn)
df = df[['namePlayer','value']].groupby(by='namePlayer').agg(np.mean)['value']
df_= pd.DataFrame(df.values,columns=['salary'])
df_['Player'] = df.index
data['salary'] = data['Player'].map(dict(zip(df_['Player'],df_['salary'])))
for i in data['Tm'].value_counts().index:
    test = data.loc[data['Tm']==i]
    test = test.sort_values(by='salary',ascending=0)
    print("Team：",i,"  The highest paid player：",test['Player'].values[0])
    # test.to_csv('Tm'+i+'球员工资排名.csv',index = 0)



