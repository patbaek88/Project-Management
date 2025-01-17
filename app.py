import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Project Management App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# 비밀번호 입력
password_input = st.text_input("암호를 입력해주세요", type="password")

# 비밀번호 확인
if password_input == "cmcpl":
    st.title("Project Management App")
    st.write("Upload your project timeline file and generate a Gantt chart")
    st.write("Step 1: Download the project timeline template")

    # 템플릿 CSV 데이터 생성
    columns = ['Task', 'Start', 'Finish', 'Resource', 'Completion_pct']
    data = {
        'Task': ["Job A", "Job B", "Job C"],
        'Start': [datetime.datetime(2009, 1, 1), datetime.datetime(2009, 3, 5), datetime.datetime(2009, 2, 20)],
        'Finish': [datetime.datetime(2009, 2, 28), datetime.datetime(2009, 4, 15), datetime.datetime(2009, 5, 30)],
        'Resource': ["Resource 1", "Resource 2", "Resource 3"],
        'Completion_pct': [100, 75, 50]
    }

    df = pd.DataFrame(data, columns=columns)

    # CSV 파일 다운로드 버튼
    template = df.to_csv(index=False)
    download = st.download_button(
        label="Download Template",
        data=template,
        file_name='template.csv',
        mime="text/csv"
    )

    st.write("")
    st.write("Step 2: Upload your project timeline file")

    # 파일 업로드
    uploaded_file = st.file_uploader('Fill out the project timeline template and upload your file here.', type=['csv'])

    if uploaded_file is not None:
        df_origin = pd.read_csv(uploaded_file)
        df = st.data_editor(df_origin, num_rows="dynamic")

        # Gantt 차트 생성
        fig = go.Figure(go.Timeline(
            x=[df["Start"], df["Finish"]],
            y=[df["Task"]],
            text=[df["Task"]],
            orientation="v",
            line=dict(color="blue"),
            textposition="bottom center"
        ))

        fig.update_layout(
            xaxis=dict(
                rangeslider_visible=False,
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray'
            ),
            yaxis=dict(
                automargin=True,
                nticks=len(df["Task"]),
                gridcolor='LightGray',
                gridwidth=1,
                zeroline=False
            )
        )

        st.plotly_chart(fig)

    else:
        st.write("Please upload your file")

else:
    st.write("")
