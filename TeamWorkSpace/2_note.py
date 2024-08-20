import streamlit as st

st.set_page_config(page_title="정리노트", page_icon="📒")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'note'
if 'memos' not in st.session_state:
    st.session_state.memos = {}
if 'categories' not in st.session_state:
    st.session_state.categories = []
if 'current_category' not in st.session_state:
    st.session_state.current_category = None
if 'current_title' not in st.session_state:
    st.session_state.current_title = None

def show_notes_page():
    st.title("나의 정리노트 📒")

    options = st.session_state.categories
    selected_category = st.selectbox("분류", options, index=options.index(st.session_state.current_category) if st.session_state.current_category in options else 0)

    if selected_category:
        st.session_state.current_category = selected_category

        st.markdown(f"""
        <div style="font-size:24px; font-weight:bold; padding: 10px; border-bottom: 2px solid #1E90FF; margin-bottom: 20px;">
            {selected_category}
        </div>
        """, unsafe_allow_html=True)

        if selected_category in st.session_state.memos:
            memo_items = st.session_state.memos[selected_category]
            columns = st.columns(4)

            col_index = 0
            for title, memo in memo_items.items():
                short_title = title[:10] + ('...' if len(title) > 10 else '')
                with columns[col_index]:
                    # Display memo item
                    st.markdown(f"""
                    <div style="padding: 10px; border: 1px solid #FF6F61; border-radius: 8px; margin-bottom: 10px; background-color: #f9f9f9; width: 150px; height: 150px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div style="font-size:14px; font-weight:bold; padding-bottom: 5px; border-bottom: 2px solid #FF6F61; color: black; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                            {short_title}
                        </div>
                        <div style="padding-top: 5px; font-size:12px; color: black; flex-grow: 1; overflow: hidden; text-overflow: ellipsis;">
                            {memo[:50]}{'...' if len(memo) > 50 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Define a unique key for each button
                    button_key = f"edit_{title}"
                    if st.button("수정하러가기⚙️", key=button_key):
                        st.session_state.current_title = title
                        st.session_state.current_page = 'edit'
                        st.rerun()
                    
                    col_index = (col_index + 1) % 4
        else:
            st.warning("이 카테고리에는 메모가 없습니다.")
    else:
        st.warning("선택된 항목이 없습니다.")

def show_view_note_page():
    category = st.session_state.current_category
    title = st.session_state.current_title
    st.title(f"보기: {category} - {title}")

    if category in st.session_state.memos and title in st.session_state.memos[category]:
        memo = st.session_state.memos[category][title]
        st.markdown(f"""
        <div style="padding: 10px; border: 1px solid #FF6F61; border-radius: 8px; margin-bottom: 10px; background-color: #f9f9f9;">
            <div style="font-size:16px; font-weight:bold; padding-bottom: 5px; border-bottom: 2px solid #FF6F61; color: black;">
                {title}
            </div>
            <div style="padding-top: 10px; font-size:14px; color: black;">
                {memo}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("수정하기"):
            st.session_state.current_page = 'edit'
            st.rerun()

    if st.button("나의 정리노트로 돌아가기"):
        st.session_state.current_page = 'note'
        st.rerun()

def show_edit_note_page():
    category = st.session_state.current_category
    title = st.session_state.current_title
    st.title(f"편집: {category} - {title}")

    if category in st.session_state.memos and title in st.session_state.memos[category]:
        memo = st.session_state.memos[category][title]
        new_memo = st.text_area("내용", value=memo, height=300)  # 긴 메모를 위한 높이 설정

        uploaded_file = st.file_uploader("파일 추가", type=['pdf', 'txt', 'md'])

        if st.button("저장"):
            if uploaded_file is not None:
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("파일이 저장되었습니다!")

            st.session_state.memos[category][title] = new_memo
            st.success("메모가 수정되었습니다!")
            st.session_state.current_page = 'note'  # 수정 후 돌아가기
            st.rerun()
    else:
        st.warning("해당 카테고리의 메모가 없습니다!")

    if st.button("나의 정리노트로 돌아가기"):
        st.session_state.current_page = 'note'
        st.rerun()

# Main page rendering logic
if st.session_state.current_page == 'note':
    show_notes_page()
elif st.session_state.current_page == 'view':
    show_view_note_page()
elif st.session_state.current_page == 'edit':
    show_edit_note_page()