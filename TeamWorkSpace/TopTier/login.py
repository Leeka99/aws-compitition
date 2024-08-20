import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로그인 페이지", page_icon="🔐")

def login_page():
    st.title("로그인 페이지 🔐")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if username == "wku" and password == "1234":
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            # 쿼리 매개변수를 설정하는 대신 세션 상태만 업데이트
            st.rerun()
        else:
            st.error("사용자 이름 또는 비밀번호가 올바르지 않습니다.")

# 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 쿼리 매개변수 확인 (필요한 경우)
if 'logged_in' in st.query_params:
    if st.query_params['logged_in'] == 'true':
        st.session_state.logged_in = True

# 로그인 상태 검사
if not st.session_state.logged_in:
    login_page()
else:
    st.success("로그인 성공! ")

# 로그아웃 기능 (선택적)
if st.session_state.logged_in:
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.rerun()