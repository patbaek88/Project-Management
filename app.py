import plotly.express as px
import pandas as pd
import streamlit as st

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
        df = st.experimental_data_editor(df_origin, num_rows="dynamic")
        #st.dataframe(df)
        st.write("")
        option = st.selectbox("View Gantt Chart by:", ("Team", "Completion %"))
        st.write("Step 3: Generate a Gantt chart")
        if st.button("Generate a Gantt chart"):       
            # 데이터프레임을 Resource와 Start 열을 기준으로 정렬
            df = df.sort_values(['Resource', 'Start'])            
            # Gantt Chart 만들기
            if option == "Team":
                fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
            elif option == "Completion %":
                fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Completion_pct")

            fig.update_xaxes(
                dtick="M1",  # 매월 표시
                tickformat="%Y-%m-%d",  # 날짜 형식 설정
                tickangle=45  # 날짜 라벨 각도 설정
            )
    

            # 위에서부터 시작하게 Y축 역방향으로 설정
            fig.update_yaxes(autorange="reversed")
            #fig.show()
            #st.set_option('deprecation.showPyplotGlobalUse', False)
            st.plotly_chart(fig)
            
    else:
        st.write("Please upload your file")
else:
    st.write("")
