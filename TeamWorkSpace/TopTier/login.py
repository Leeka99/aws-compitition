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
            st.query_params(logged_in=True)  # 쿼리 매개변수 설정
            st.write('<meta http-equiv="refresh" content="0; url=/main">', unsafe_allow_html=True) ## 추가가

        else:
            st.error("사용자 이름 또는 비밀번호가 올바르지 않습니다.")

# 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'redirect_to_main' not in st.session_state:  ## 추가가
    st.session_state.redirect_to_main = False  ## 추가


# 쿼리 매개변수 확인
query_params = st.query_params
if 'logged_in' in query_params and query_params['logged_in'][0] == 'True':
    st.session_state.logged_in = True

# 로그인 상태 검사
if not st.session_state.logged_in:
    login_page()
    st.stop()  # 로그인되지 않은 경우 이후 코드 실행 중지

# 페이지 렌더링  ## 추가
if st.session_state.logged_in and st.session_state.redirect_to_main:
    # HTML 메타 태그를 사용하여 페이지를 리디렉션합니다.
    st.write('<meta http-equiv="refresh" content="0; url=/main">', unsafe_allow_html=True)
else:
    login_page()

    
