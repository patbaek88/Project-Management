import plotly.express as px
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

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
            # 데이터프레임을 Resource와 Start 열을 기준으로 정렬
            #df = df.sort_values(['Resource', 'Start'])            
            # Gantt Chart 만들기
            df['Text'] = df['Start'] + '→' + df['Finish'] +" : " + df['Task']
            if option == "Team":
                fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource", category_orders={"Task": df["Task"].tolist()[::-1]}, text = "Text")


            elif option == "Completion %":
                fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Completion_pct",   category_orders={"Task": df["Task"].tolist()[::-1]}, text = "Text")



            fig.update_xaxes(
                dtick="M1",  # 매월 표시
                tickformat="%m",  # 날짜 형식 설정
                tickangle=0  # 날짜 라벨 각도 설정
            )

            # 연도 표시를 위한 위치와 텍스트 설정
            min_date = df['Start'].min()
            max_date = df['Finish'].max()

           # 연도 추가
            years = pd.date_range(start=min_date, end=max_date, freq='YS')
            year_ticks = [date for date in years]
            year_labels = [date.strftime('%Y') for date in years]

          # 연도 레이블을 별도로 추가
            for year, label in zip(year_ticks, year_labels):
                fig.add_annotation(
                    x=year,
                    y=-0.05,  # 위치조절
                    showarrow=False,
                    text=label,
                    xref="x",
                    yref="paper"
                )

            # x축 범위 설정 및 그리드 추가
            fig.update_layout(
                xaxis=dict(
                    showgrid=True,      # 그리드 표시
                    gridwidth=1,
                    gridcolor='LightGray'
                )
            )
    
            # 위에서부터 시작하게 Y축 역방향으로 설정
            #fig.update_yaxes(autorange="reversed")
            #fig.show()
            #st.set_option('deprecation.showPyplotGlobalUse', False)

            fig.update_traces(textposition="outside", textfont=dict(color="black"))
            
            st.plotly_chart(fig)



    else:
        st.write("Please upload your file")
else:
    st.write("")
