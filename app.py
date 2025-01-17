import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":
    st.title("Project Management App")
    st.write("Upload your project timeline file and generate a Gantt chart")
    st.write("Step 1: Download the project timeline template")
    temp_df = pd.read_csv('template.csv')
    template = temp_df.to_csv(index=False)
    template.encode("utf-8")
    download = st.download_button(label="Download Template", data= template, file_name = 'template.csv', mime="text/csv")
    st.write("")
    st.write("Step 2: Upload your project timeline file")
    uploaded_file = st.file_uploader('Fill out the project timeline template and upload your file here.', type=['csv'])
    if uploaded_file is not None:
        df_origin = pd.read_csv(uploaded_file)
        df = st.data_editor(df_origin, num_rows="dynamic")
        #st.dataframe(df)
        st.write("")
        option = st.selectbox("View Gantt Chart by:", ("Team", "Completion %"))
        st.write("Step 3: Generate a Gantt chart")
        if st.button("Generate a Gantt chart"):  

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
