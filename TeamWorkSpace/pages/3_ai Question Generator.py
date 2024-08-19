import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import random

st.set_page_config(page_title="AI 질문 생성기", page_icon="🤖")

def get_bedrock_client():
    try:
        client = boto3.client('bedrock')
        return client
    except NoCredentialsError:
        st.error("AWS 자격 증명이 필요합니다.")
        return None

def show_question_generator_page():
    st.title("AI 질문 생성기 🤖")

    options = st.session_state.get('categories', [])
    selected_category = st.selectbox("분류", options, index=options.index(st.session_state.get('current_category', options[0])) if options else 0)

    if selected_category:
        st.session_state.current_category = selected_category

        if st.button("질문 생성하기"):
            client = get_bedrock_client()
            if client:
                memo_items = st.session_state.memos.get(selected_category, {})
                if memo_items:
                    title, memo = random.choice(list(memo_items.items()))
                    
                    try:
                        response = client.invoke_model(
                            modelId='text-davinci-003',  # 실제 Bedrock 모델 ID로 변경
                            prompt=f"다음 메모 내용을 바탕으로 질문을 생성하세요: {memo}",
                            maxTokens=100
                        )
                        
                        question = response['body']['generatedText'].strip()
                        
                        st.write(f"생성된 질문: {question}")

                        user_answer = st.text_input("답변을 입력하세요")

                        if st.button("정답 확인"):
                            correct_answer = "예상 답변"  # 실제 정답을 설정해 주세요
                            if user_answer.lower() == correct_answer.lower():
                                st.success("정답입니다!")
                            else:
                                st.error("정답이 아닙니다. 다시 시도해보세요.")
                    except Exception as e:
                        st.error(f"질문 생성에 실패했습니다: {e}")
                else:
                    st.warning("이 카테고리에는 메모가 없습니다.")
            else:
                st.error("AWS Bedrock 클라이언트를 사용할 수 없습니다.")
    else:
        st.warning("선택된 항목이 없습니다.")

query_params = st.query_params
if 'questions' in query_params:
    st.session_state.current_page = 'questions'
else:
    st.session_state.current_page = 'questions'

if st.session_state.current_page == 'questions':
    show_question_generator_page()
