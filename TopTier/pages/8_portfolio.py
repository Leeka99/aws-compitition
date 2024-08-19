import streamlit as st
import plotly.graph_objects as go

# 기술 숙련도 그래프
def plot_bar_chart():
    labels = ['AWS', 'Docker', 'CI/CD', 'Python']
    values = [75, 65, 80, 90]
    
    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker_color=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'])])
    fig.update_layout(title='기술 숙련도', xaxis_title='기술', yaxis_title='숙련도 (%)')
    st.plotly_chart(fig)

# 학습 진행 상황 그래프
def plot_doughnut_chart():
    labels = ['완료: GitActions 및 CodePipeline을 이용한 CI/CD', 
              '진행 중: 컨테이너 오케스트레이션, 서버리스, 모니터링', 
              '시작 안 함: 세부 보안 네트워크 구성 및 모니터링']
    sizes = [30, 50, 20]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3)])
    fig.update_layout(title='학습 진행 상황')
    st.plotly_chart(fig)

#프로젝트 기여 그래프
def plot_pie_chart():
    labels = ['백엔드 개발', '프론트엔드 개발', '데이터베이스 관리', '테스팅']
    sizes = [40, 30, 15, 15]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig.update_layout(title='프로젝트 기여')
    st.plotly_chart(fig)

# Page layout
st.set_page_config(page_title="포트폴리오", layout="wide")

# Apply background color to the entire page
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background-color: #50b3a2; padding: 20px; text-align: center; color: white;'>
        <h1 style='font-size: 24px;'>대학생 데브옵스 엔지니어 이력서</h1>
    </div>
    """, unsafe_allow_html=True)

# Showcase
st.markdown("""
    <div style='background-color: #2c7a7b; padding: 40px; text-align: center; color: white;'>
        <h1 style='font-size: 48px;'>이강현</h1>
        <h2 style='font-size: 24px;'>데브옵스 엔지니어링에 대한 열정을 가진 대학생</h2>
    </div>
    """, unsafe_allow_html=True)

# Top Sections
st.markdown("""
    <div style='display: flex; justify-content: space-around; padding: 20px;color:black'>
        <div style='flex: 1; margin: 10px; padding: 20px; background-color: #f7fafc; border-radius: 10px; '>
            <h2 style='color: black;'>소개</h2>
            <p>저는 ~대학교에서 컴퓨터 과학을 전공하고 있으며, 데브옵스 분야에 큰 관심을 가지고 있습니다. 클라우드 인프라, 자동화, CI/CD에 대한 지식을 갖추고 있으며, 이를 프로젝트에 적용하는 데 열정적입니다.</p>
        </div>
        <div style='flex: 1; margin: 10px; padding: 20px; background-color: #f7fafc; border-radius: 10px;'>
            <h2 style='color: black;'>교육</h2>
            <p>원광대학교 컴퓨터 소프트웨어 공학과 | 예상 졸업년도: 2025년</p>
        </div>
        <div style='flex: 1; margin: 10px; padding: 20px; background-color: #f7fafc; border-radius: 10px;'>
            <h2 style='color: black;'>프로젝트 경험</h2>
            <p>다양한 학교 프로젝트에 참여했으며, 특히 AWS를 사용한 웹 애플리케이션 배포와 GitHub Actions를 통한 CI/CD 파이프라인 구축에 관심을 가지고 있습니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


plot_bar_chart()

plot_doughnut_chart()

plot_pie_chart()

st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# Contact Section
st.markdown("""
    <div style='padding: 20px; background-color: #f7fafc; border-radius: 10px;'>
        <h2 style='color: black;'>연락처</h2>
        <p style='color: black;'>Phone: 010-1234-5678</p>
        <p><a href="mailto:example@example.com" style='color: #3182ce;'>example@example.com</a></p>
        <p><a href="https://github.com/yourgithubid" target="_blank" style='color: #3182ce;'>Github: yourid</a></p>
        <p><a href="https://linkedin.com/in/yourprofile" target="_blank" style='color: #3182ce;'>LinkedIn: yourprofile</a></p>
    </div>
    """, unsafe_allow_html=True)
