import streamlit as st
import requests

# 페이지 설정
st.set_page_config(page_title="회원 관리 페이지", page_icon="🔐")

# 로그인 페이지 함수
def login_page():
    st.title("로그인 페이지 🔐")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        response = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.experimental_rerun()  # 로그인 성공 후 페이지를 새로 고침하여 상태 업데이트
        else:
            st.error("로그인 실패. 사용자 이름이나 비밀번호를 확인하세요.")

# 회원가입 페이지 함수
def register_page():
    st.title("회원가입 페이지 ✨")
    username = st.text_input("사용자 이름", key="register_username")
    password = st.text_input("비밀번호", type="password", key="register_password")
    
    if st.button("회원가입"):
        response = requests.post("http://localhost:8000/register", json={"username": username, "password": password})
        if response.status_code == 201:
            st.success("회원가입 성공! 로그인해 주세요.")
            st.session_state.registered = True
            st.experimental_rerun()  # 회원가입 후 페이지를 새로 고침하여 상태 업데이트
        else:
            st.error("회원가입 실패. 사용자 이름이 이미 등록되어 있을 수 있습니다.")

# 초기화 및 상태 설정
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'registered' not in st.session_state:
    st.session_state.registered = False

# 페이지 라우팅
if st.session_state.logged_in:
    st.success("로그인 성공!")
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.experimental_rerun()  # 로그아웃 후 페이지를 새로 고침하여 상태 업데이트
else:
    if st.session_state.registered:
        st.success("회원가입 완료! 로그인해 주세요.")
        login_page()
    else:
        choice = st.radio("원하시는 작업을 선택하세요", ("로그인", "회원가입"))
        if choice == "로그인":
            login_page()
        else:
            register_page()
