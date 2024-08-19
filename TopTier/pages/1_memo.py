import streamlit as st

st.set_page_config(page_title="메모 작성", page_icon="📝")

def show_new_note_page():
    st.title("새로운 메모 작성 📝")

    category = st.text_input("분류")
    title = st.text_input("제목")
    memo = st.text_area("내용", height=1000)
    uploaded_file = st.file_uploader("파일 추가")

    if st.button("저장"):
        if category and title and memo:
            if 'memos' not in st.session_state:
                st.session_state.memos = {}
            if category not in st.session_state.memos:
                st.session_state.memos[category] = {}
            st.session_state.memos[category][title] = memo

            if 'categories' not in st.session_state:
                st.session_state.categories = []
            if category not in st.session_state.categories:
                st.session_state.categories.append(category)

            if uploaded_file is not None:
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("파일이 저장되었습니다!")

            st.success("메모가 저장되었습니다!")
        else:
            st.warning("분류, 제목, 그리고 내용을 입력해주세요!")

show_new_note_page()
