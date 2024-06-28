import plotly.express as px
import pandas as pd
import streamlit as st

password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":
    st.title("Project Management App")
    st.write("Upload your project timeline file and generate a Gantt chart")
    st.write("Step 1: Download the project timeline template")
    download = st.download_button(label="Download Template", data= 'template.csv', file_name = 'template.csv')
    st.write("")
    st.write("Step 2: Upload your project timeline file")
    data = st.file_uploader('Fill out the project timeline template and upload your file here.', type=['csv'])
    if data == True:
        st.write(data)
        st.write("")
        st.write("Step 3: Generate a Gantt chart")
        if st.button("Generate a Gantt chart"):
            # 데이터셋 만들기
            df = pd.DataFream(data=data)
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
        else:
            st.write("Please upload your file")
    else:
        st.write("")
