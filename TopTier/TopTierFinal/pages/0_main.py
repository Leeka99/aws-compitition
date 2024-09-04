import streamlit as st

if not st.session_state.logged_in:
    st.warning("로그인이 필요합니다.")
    st.stop()

st.set_page_config(
    page_title="TopTier",
    page_icon="🚩",
)

st.write("# TopTier를 향해 메모하기 🤓🚩🚩 ")


st.markdown(
    """
     완벽한 학습을 위해 탑티어를 이용하세요!

    ### 기능
    - 메모하기
    - 편리한 메모장 검색
    - 완벽한 습득을 위한 AI 학습

"""
)