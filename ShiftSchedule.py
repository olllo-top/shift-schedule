import streamlit as st
import pandas as pd

holidays = {
    '2024年1周': '元旦',
    '2024年6周': '除夕',
    '2024年7周': '春节',
    '2024年14周': '清明节',
    '2024年15周': '三月三',
    '2024年18周': '劳动节',
    '2024年24周': '端午节',
    '2024年37周': '中秋节',
    '2024年40周': '国庆节',
    '2025年1周': '元旦',
    '2025年5周': '除夕',
    '2025年6周': '春节',
    '2025年15周': '清明节,三月三',
    '2025年18周': '劳动节',
    '2025年22周': '端午节',
    '2025年40周': '国庆节',
    '2025年41周': '中秋节',
}

def calculate_duty_schedules(center_department, personnel, start_person_indoor, start_person_center, start_year, start_week, end_year, end_week, start_week_center, center_round_weeks):
    indoor_start_index = personnel.index(start_person_indoor)
    indoor_duty = {}
    center_start_index = personnel.index(start_person_center)
    center_duty = {}

    year = start_year 
    week = min(start_week,start_week_center)
    
    week_indoor = 0
    week_center = 0

    while year < end_year or (year == end_year and week < end_week):

        current_week = f"{year}年{week}周"
        
        if week == start_week and week_indoor == 0:
            week_indoor = week
        
        if week == week_indoor:
            indoor_duty[current_week] = personnel[indoor_start_index]
            indoor_start_index = (indoor_start_index + 1) % len(personnel)
            
            week_indoor += 1
            
            if week_indoor > 52:
                week_indoor = week_indoor - 52
        else:
            indoor_duty[current_week] = ''
        
        if week == start_week_center and week_center == 0:
            week_center = week
        
        if week == week_center:
            #center_duty[current_week] = personnel[center_start_index] 
            center_duty[current_week] = personnel[center_start_index] 
            
            center_start_index = (center_start_index + 1) % len(personnel)
            
            #print('center_start_index',center_start_index,personnel[center_start_index])
            
            week_center += center_round_weeks
            
            if week_center > 52:
                week_center = week_center - 52
            
        else:
            center_duty[current_week] = center_department[week % len(center_department)]

        # Calculate the number of weeks
        week += 1
        if week > 52:
            year += 1
            week = 1
            
        

    return indoor_duty, center_duty

@st.cache_data 
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def main(default_params):
        
    #st.set_page_config(layout="wide")
    st.set_page_config(page_title='排班表和节假日', page_icon=None, layout='wide', initial_sidebar_state='collapsed')
    #st.title("排班表和节假日")
    title = "排班表和节假日"
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    

        
    if default_params == {}:
        default_params = st.session_state.get("params",
            # 读取默认参数
            {
                "center_department":"实体室,网格室,数智室",
                "personnel":"覃*, 林*, 曹*, 黄*, 卢*, 沈继*, 方*, 戴*, 周*, 毛*, 来*",
                "start_year": 2023,
                "start_week": 48,
                "start_person_indoor": 0,
                "start_week_center": 48,
                "start_person_center": 0,
                "center_round_weeks": 3,
                "end_year":2024,
                "end_week":52
            }
            
        )
    
    
    with st.sidebar:
        st.header("输入信息")
        
        center_department = st.text_input("顺序输入渠道各个室表（用逗号分隔）:", value=default_params["center_department"])
        center_department = [p.strip() for p in center_department.split(",")]
        
        personnel = st.text_area("输入室内人员列表（用逗号分隔）:", value=default_params["personnel"])
        personnel = [p.strip() for p in personnel.split(",")]

        start_year = st.number_input("输入起始年份:", min_value=2000, max_value=3000, value=default_params["start_year"])
        start_week = st.number_input("输入室内周报起始周数:", min_value=1, max_value=52, value=default_params["start_week"])
        start_person_indoor = st.selectbox("选择室内周报起始人员:", personnel,index=default_params["start_person_indoor"])
        
        start_week_center = st.number_input("输入中心周报起始周数:", min_value=1, max_value=52, value=default_params["start_week_center"])
        start_person_center = st.selectbox("选择中心周报起始人员:", personnel,index=default_params["start_person_center"])
        center_round_weeks = st.number_input("中心周报轮换周期:", min_value=1, max_value=52, value=default_params["center_round_weeks"])

        end_year = st.number_input("输入结束年份:", min_value=start_year, max_value=3000, value=default_params["end_year"])
        end_week = st.number_input("输入结束周数:", min_value=1, max_value=52, value=default_params["end_week"])


        indoor_duty, center_duty = calculate_duty_schedules(center_department, personnel, start_person_indoor, start_person_center, start_year, start_week, end_year, end_week, start_week_center, center_round_weeks)

        col1, col2 = st.columns([1, 1])
        with col1:         
            if st.button("重新排序"):
                indoor_duty, center_duty = calculate_duty_schedules(center_department, personnel, start_person_indoor, start_person_center, start_year, start_week, end_year, end_week, start_week_center, center_round_weeks)
            else:
                indoor_duty, center_duty = calculate_duty_schedules(center_department, personnel, start_person_indoor, start_person_center, start_year, start_week, end_year, end_week, start_week_center, center_round_weeks)
            
        with col2:
            if st.button("保存参数"):
                with open('parameters.txt', 'w',encoding='utf8') as f:
                    f.write(f"{center_department}|{personnel}|{start_year}|{start_week}|{personnel.index(start_person_indoor)}|{start_week_center}|{personnel.index(start_person_center)}|{center_round_weeks}|{end_year}|{end_week}")

    st.subheader("本周排班")
    

    df = pd.DataFrame({'时间（周）': list(indoor_duty.keys()),
                        '室内周报': list(indoor_duty.values()),
                        '中心周报': list(center_duty.values()),
                        '重要节假日': [holidays.get(key, '') for key in list(indoor_duty.keys())]})
    
    current_year_week = get_current_year_week()

    st.dataframe(df.loc[df['时间（周）'] == current_year_week].style.set_properties(**{
        "background-color": "yellow",
        "font-weight": "bold",
    }), use_container_width=True )
    
    st.download_button(
        label="下载排班表",
        data=convert_df(df),
        file_name='duty_schedule.csv',
        mime='text/csv',
    )
    
    
    st.dataframe(df, use_container_width=True, height=600)
    
        

import datetime
def get_current_year_week():
    current_date = datetime.datetime.now()
    year, week, _ = current_date.isocalendar()
    return f"{year}年{week}周"
        
        
if __name__ == "__main__":
    default_params = {}
    try:     
        with open('parameters.txt', 'r',encoding='utf8') as f:
            x = f.read().split('|')
            default_params['center_department'] = ','.join(eval(x[0]))
            default_params['personnel'] = ','.join(eval(x[1]))
            default_params['start_year'] = int(x[2])
            default_params['start_week'] = int(x[3])
            default_params['start_person_indoor'] = int(x[4])
            default_params['start_week_center'] = int(x[5])
            default_params['start_person_center'] = int(x[6])
            default_params['center_round_weeks'] = int(x[7])
            default_params['end_year'] = int(x[8])
            default_params['end_week'] = int(x[9])

    except:
        default_params = {}
        print('打开配置文件错误')
        # 读取默认参数
        
    main(default_params)
