#!/usr/bin/env python
# coding: utf-8

# In[3]:


import plotly.express as px
import pandas as pd

# 데이터셋 만들기
df = pd.read_csv('data.csv')

# 시작일과 종료일의 최소값과 최대값 구하기
min_date = pd.to_datetime(df['Start']).min()
max_date = pd.to_datetime(df['Finish']).max()

# 월별 세로줄 생성
vlines = []
for year in range(min_date.year, max_date.year+1):
    for month in range(1, 13):
        date = pd.to_datetime(f'{year}-{month}-01')
        if date >= min_date and date <= max_date:
            vlines.append(dict(x=date, line_width=1, line_dash="dash", line_color="gray"))

# 데이터프레임을 Resource와 Start 열을 기준으로 정렬
df = df.sort_values(['Resource', 'Start'])            
# Gantt Chart 만들기
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")

# x축 범위 설정
#fig.update_layout(xaxis_range=[df['Start'].min(), df['Finish'].max()])

# 월별 세로줄 추가
for vline in vlines:
    fig.add_vline(**vline)


# 위에서부터 시작하게 Y축 역방향으로 설정
fig.update_yaxes(autorange="reversed")
fig.show()


# In[40]:


import plotly.figure_factory as ff
import pandas as pd

# 데이터셋 만들기
df = pd.read_csv('data.csv')


# 시작일과 종료일의 최소값과 최대값 구하기
min_date = pd.to_datetime(df['Start']).min()
max_date = pd.to_datetime(df['Finish']).max()

# 월별 세로줄 생성
vlines = []
for year in range(min_date.year, max_date.year+1):
    for month in range(1, 13):
        date = pd.to_datetime(f'{year}-{month}-01')
        if date >= min_date and date <= max_date:
            vlines.append(dict(x=date, line_width=1, line_dash="dash", line_color="gray"))

# 데이터프레임을 Resource와 Start 열을 기준으로 정렬
df = df.sort_values(['Resource', 'Start'])            
            
# 간트차트 생성
fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True)

# x축 범위 설정
fig.update_layout(xaxis_range=[df['Start'].min(), df['Finish'].max()])

# 월별 세로줄 추가
for vline in vlines:
    fig.add_vline(**vline)

# 차트 출력
fig.show()


# In[45]:


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 데이터셋 만들기
df = pd.read_csv('data.csv')

# Convert 'Start Dates' to numeric duration values
df['Start'] = mdates.datestr2num(df['Start'])

# Step 3: Initialize the figure and axis
fig, ax = plt.subplots()

# Step 4: Create the Gantt chart
sns.barplot(data=df, x='Start', y='Task', hue='Resource', ax=ax)

# Step 5: Customize the chart
ax.set_xlabel('Date')
ax.set_ylabel('Tasks')
ax.set_title('Basic Gantt Chart')
ax.grid(True)

# Step 6: Display the chart
plt.show()

