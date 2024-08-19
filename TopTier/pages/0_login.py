import streamlit as st

# 페이지 설정
st.set_page_config(page_title="로그인 페이지", page_icon="🔐")

# 사용자 데이터 (실제 사용 시에는 데이터베이스나 안전한 저장소에서 관리해야 합니다)
users = {
    "user1": "password1",
    "user2": "password2"
}

# 로그인 페이지 함수
def login_page():
    st.title("로그인 페이지 🔐")

    # 사용자 입력
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")

    # 로그인 버튼
    if st.button("로그인"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.experimental_rerun()  # 로그인 후 페이지 새로 고침
        else:
            st.error("사용자 이름 또는 비밀번호가 올바르지 않습니다.")

# 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 로그인 상태에 따른 페이지 렌더링
if st.session_state.logged_in:
    st.success("로그인 성공! 이 페이지는 로그인 후 표시됩니다.")
    # 로그인 후 이동할 페이지를 여기에 추가하거나, 성공 메시지를 표시할 수 있습니다.
else:
    login_page()
