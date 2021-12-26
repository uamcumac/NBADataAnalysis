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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('datasets/nba2021_per_game.csv')
column = ['Player', '位置', '年龄', '球队', '出场次数', '首发出场次数', '出场时间', '命中次数', '出手次数',
       '命中率', '三分球命中', '三分球出手', '三分球命中率', '两分球命中', '两分球出手', '两分球命中率', '真实命中率',
       '罚球命中', '罚球次数', '罚球命中率', '进攻篮板', '防守篮板', '总篮板', '助攻', '抢断', '盖帽', '失误',
       '犯规', '得分']
data.columns = column


import matplotlib.pyplot as plt
x = data['球队'].value_counts().index
y = data['球队'].value_counts().values
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(13,5))
plt.bar(x,y)
plt.title("每队的球员数")
plt.xlabel('team')
plt.ylabel('number')
# plt.savefig('每队的球员数.png',dpi=600)

# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
def fun(team,Player):
    data1 = data.loc[data['球队']==team]
    lanban = data1['总篮板']
    zhugong = data1['助攻']
    defen = data1['得分']
    sanfen = data1['三分球命中']
    toulan = data1['两分球命中率']
    gaimao = data1['盖帽']
    qiangduan = data1['抢断']
    lanban_max = max(lanban)
    zhugong_max = max(zhugong)
    defen_max = max(defen)
    sanfen_max = max(sanfen)
    toulan_max = max(toulan)
    gaimao_max = max(gaimao)
    qiangduan_max = max(qiangduan)
    x = np.array(data1.loc[data1['Player'] == Player][['总篮板','助攻','得分',
                                                    '三分球命中','两分球命中率','盖帽','抢断']])[0]
    keys = ['总篮板','助攻','得分','三分球命中','两分球命中率','盖帽','抢断']
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
for i in data['球队'].value_counts().index:
    for j in data.loc[data['球队']==i]['Player'].values:
        score.append(fun(i,j))

player = pd.DataFrame(score,columns=['总篮板','助攻','得分',
        '三分球命中','两分球命中率','盖帽','抢断'])
Player = []
team = []
for i in data['球队'].value_counts().index:
    for j in data.loc[data['球队']==i]['Player'].values:
        Player.append(j)
        team.append(i)
player['球员'] = Player
player['球队'] = team
player['出场次数'] = player['球员'].map(dict(zip(data['Player'].values,data['出场次数'].values)))
player['首发出场次数'] = player['球员'].map(dict(zip(data['Player'].values,data['首发出场次数'].values)))
player['出场时间'] = player['球员'].map(dict(zip(data['Player'].values,data['出场时间'].values)))

Team = []
bestplayer = []
for i in data['球队'].value_counts().index:
    test = player.loc[player['球队'] == i]
    test['出场次数'] = test['出场次数']/test['出场次数'].max()*100
    test['首发出场次数'] = test['首发出场次数']/test['首发出场次数'].max()*100
    test['出场时间'] = test['出场时间']/test['出场时间'].max()*100
    test['加权总得分'] = test[['总篮板','助攻','得分',
          '三分球命中','两分球命中率','盖帽','抢断','出场次数','出场时间','首发出场次数']].sum(axis = 1)
    test = test.sort_values(by = '加权总得分',ascending=0)
    Team.append(i)
    bestplayer.append(test['球员'].values[0])
    print("球队：",i," 最重要的球星：",test['球员'].values[0])
    test.to_csv('球队'+i+'球员数据总得分.csv',index = 0)
data_best = pd.DataFrame(Team,columns = ['球队'])
data_best['球员'] = bestplayer
# data_best.to_csv('各队最重要的球星.csv',index = 0)

import sqlite3 as sql
conn = sql.connect('datasets/basketball.sqlite') # create connection object to database
df = pd.read_sql('select * from Player_Salary', conn)
df = df[['namePlayer','value']].groupby(by='namePlayer').agg(np.mean)['value']
df_= pd.DataFrame(df.values,columns=['工资'])
df_['球员'] = df.index
data['工资'] = data['Player'].map(dict(zip(df_['球员'],df_['工资'])))
for i in data['球队'].value_counts().index:
    test = data.loc[data['球队']==i]
    test = test.sort_values(by='工资',ascending=0)
    print(i+'球队工资最高的球员:',test['Player'].values[0])
    # test.to_csv('球队'+i+'球员工资排名.csv',index = 0)



