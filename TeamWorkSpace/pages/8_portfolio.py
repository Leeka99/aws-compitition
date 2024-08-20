import streamlit as st
import plotly.graph_objects as go

def plot_bar_chart(skills):
    labels = list(skills.keys())
    values = list(skills.values())
    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'])])
    fig.update_layout(title='기술 숙련도', xaxis_title='기술', yaxis_title='숙련도 (%)')
    return fig

def plot_doughnut_chart(learning_progress):
    labels = list(learning_progress.keys())
    sizes = list(learning_progress.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3)])
    fig.update_layout(title='학습 진행 상황')
    return fig

def plot_pie_chart(project_contribution):
    labels = list(project_contribution.keys())
    sizes = list(project_contribution.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig.update_layout(title='프로젝트 기여')
    return fig

def get_portfolio_info(existing_info=None):
    st.header("포트폴리오 정보 입력")
    
    name = st.text_input("이름", value=existing_info.get('name', '') if existing_info else '')
    intro = st.text_area("자기소개", value=existing_info.get('intro', '') if existing_info else '')
    education = st.text_input("학교 및 전공", value=existing_info.get('education', '') if existing_info else '')
    expected_graduation = st.text_input("예상 졸업년도", value=existing_info.get('expected_graduation', '') if existing_info else '')
    project_experience = st.text_area("프로젝트 경험", value=existing_info.get('project_experience', '') if existing_info else '')
    
    skills = {}
    st.subheader("기술 숙련도")
    for i in range(4):
        skill = st.text_input(f"기술 {i+1}", key=f"skill_{i}", value=list(existing_info.get('skills', {}).keys())[i] if existing_info and i < len(existing_info.get('skills', {})) else '')
        proficiency = st.slider(f"{skill} 숙련도", 0, 100, list(existing_info.get('skills', {}).values())[i] if existing_info and i < len(existing_info.get('skills', {})) else 50, key=f"proficiency_{i}")
        if skill:
            skills[skill] = proficiency
    
    learning_progress = {}
    st.subheader("학습 진행 상황")
    for i in range(3):
        topic = st.text_input(f"학습 주제 {i+1}", key=f"topic_{i}", value=list(existing_info.get('learning_progress', {}).keys())[i] if existing_info and i < len(existing_info.get('learning_progress', {})) else '')
        progress = st.number_input(f"{topic} 진행률", 0, 100, list(existing_info.get('learning_progress', {}).values())[i] if existing_info and i < len(existing_info.get('learning_progress', {})) else 33, key=f"progress_{i}")
        if topic:
            learning_progress[topic] = progress
    
    project_contribution = {}
    st.subheader("프로젝트 기여")
    for i in range(4):
        area = st.text_input(f"기여 영역 {i+1}", key=f"area_{i}", value=list(existing_info.get('project_contribution', {}).keys())[i] if existing_info and i < len(existing_info.get('project_contribution', {})) else '')
        contribution = st.number_input(f"{area} 기여도", 0, 100, list(existing_info.get('project_contribution', {}).values())[i] if existing_info and i < len(existing_info.get('project_contribution', {})) else 25, key=f"contribution_{i}")
        if area:
            project_contribution[area] = contribution
    
    contact = {
        "phone": st.text_input("전화번호", key="contact_phone", value=existing_info.get('contact', {}).get('phone', '') if existing_info else ''),
        "email": st.text_input("이메일", key="contact_email", value=existing_info.get('contact', {}).get('email', '') if existing_info else ''),
        "github": st.text_input("Github 프로필 URL", key="contact_github", value=existing_info.get('contact', {}).get('github', '') if existing_info else ''),
        "linkedin": st.text_input("LinkedIn 프로필 URL", key="contact_linkedin", value=existing_info.get('contact', {}).get('linkedin', '') if existing_info else '')
    }
    
    return {
        "name": name,
        "intro": intro,
        "education": education,
        "expected_graduation": expected_graduation,
        "project_experience": project_experience,
        "skills": skills,
        "learning_progress": learning_progress,
        "project_contribution": project_contribution,
        "contact": contact
    }

def generate_portfolio_page(info):
    st.markdown(f"""
    <div style='background-color: #50b3a2; padding: 20px; text-align: center; color: white;'>
        <h1 style='font-size: 24px;'>대학생 데브옵스 엔지니어 이력서</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background-color: #2c7a7b; padding: 40px; text-align: center; color: white;'>
        <h1 style='font-size: 48px;'>{info['name']}</h1>
        <h2 style='font-size: 24px;'>데브옵스 엔지니어링에 대한 열정을 가진 대학생</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='display: flex; justify-content: space-around; padding: 20px;color:black'>
        <div style='flex: 1; margin: 10px; padding: 20px; background-color: #f7fafc; border-radius: 10px; '>
            <h2 style='color: black;'>소개</h2>
            <p>{info['intro']}</p>
        </div>
        <div style='flex: 1; margin: 10px; padding: 20px; background-color: #f7fafc; border-radius: 10px;'>
            <h2 style='color: black;'>교육</h2>
            <p>{info['education']} | 예상 졸업년도: {info['expected_graduation']}</p>
        </div>
        <div style='flex: 1; margin: 10px; padding: 20px; background-color: #f7fafc; border-radius: 10px;'>
            <h2 style='color: black;'>프로젝트 경험</h2>
            <p>{info['project_experience']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(plot_bar_chart(info['skills']))
    st.plotly_chart(plot_doughnut_chart(info['learning_progress']))
    st.plotly_chart(plot_pie_chart(info['project_contribution']))
    
    st.markdown(f"""
    <div style='padding: 20px; background-color: #f7fafc; border-radius: 10px;'>
        <h2 style='color: black;'>연락처</h2>
        <p style='color: black;'>Phone: {info['contact']['phone']}</p>
        <p><a href="mailto:{info['contact']['email']}" style='color: #3182ce;'>{info['contact']['email']}</a></p>
        <p><a href="{info['contact']['github']}" target="_blank" style='color: #3182ce;'>Github</a></p>
        <p><a href="{info['contact']['linkedin']}" target="_blank" style='color: #3182ce;'>LinkedIn</a></p>
    </div>
    """, unsafe_allow_html=True)

def show_portfolio_page():
    st.title("포트폴리오 생성기")
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    if st.session_state.edit_mode or 'portfolio_info' not in st.session_state:
        existing_info = st.session_state.get('portfolio_info', None)
        portfolio_info = get_portfolio_info(existing_info)
        if st.button("포트폴리오 저장"):
            st.session_state.portfolio_info = portfolio_info
            st.session_state.edit_mode = False
            st.success("포트폴리오가 저장되었습니다!")
            st.rerun()
    else:
        generate_portfolio_page(st.session_state.portfolio_info)
        if st.button("포트폴리오 수정"):
            st.session_state.edit_mode = True
            st.rerun()

if __name__ == "__main__":
    show_portfolio_page()