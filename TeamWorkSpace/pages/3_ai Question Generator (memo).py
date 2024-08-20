import streamlit as st
import boto3
import json
import random
import re
from botocore.config import Config

# Streamlit 페이지 설정
st.set_page_config(page_title="메모 기반 AI 질문 생성기", page_icon="📝")

# 세션 상태 초기화
if 'memos' not in st.session_state:
    st.session_state.memos = {}
if 'categories' not in st.session_state:
    st.session_state.categories = []
if 'current_category' not in st.session_state:
    st.session_state.current_category = None
if 'generated_question' not in st.session_state:
    st.session_state.generated_question = None
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""

# AWS Bedrock 클라이언트 초기화 함수
def get_bedrock_client():
    session = boto3.Session()
    client = session.client(
        service_name='bedrock-runtime',
        region_name='us-east-1',
        config=Config(
            retries={'max_attempts': 10, 'mode': 'adaptive'}
        )
    )
    return client

# 질문 생성 함수
def generate_question(prompt):
    try:
        bedrock_runtime = get_bedrock_client()
        instruction = f"Human: 다음 메모 내용을 바탕으로 관련된 여러 개의 질문을 만들어 주세요:\n\n{prompt}\n\nAssistant: 네, 이해했습니다. 메모 내용을 바탕으로 관련 질문들을 생성해 드리겠습니다:\n\n1."
        
        body = json.dumps({
            "prompt": instruction,
            "max_tokens_to_sample": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]
        })
        
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-v2",
            body=body
        )
        
        response_body = json.loads(response.get('body').read())
        generated_text = response_body.get('completion', '')
        
        questions = re.findall(r'\d+\.\s*(.*)', generated_text)
        if not questions:
            st.error("생성된 텍스트에서 질문을 추출할 수 없습니다.")
            return None
        return random.choice(questions).strip()
        
    except Exception as e:
        st.error(f"질문 생성에 실패했습니다: {str(e)}")
        return None

# 피드백 제공 함수
def provide_feedback(question, user_answer):
    try:
        bedrock_runtime = get_bedrock_client()
        instruction = f"Human: 다음 질문과 사용자의 답변에 대해 자세하고 친절한 피드백을 제공해 주세요.\n\n질문: {question}\n\n사용자의 답변: {user_answer}\n\nAssistant: 네, 이해했습니다. 질문과 사용자의 답변을 바탕으로 피드백을 제공해 드리겠습니다.\n\n"
        
        body = json.dumps({
            "prompt": instruction,
            "max_tokens_to_sample": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]
        })
        
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-v2",
            body=body
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body.get('completion', '').strip()
        
    except Exception as e:
        st.error(f"피드백 생성에 실패했습니다: {str(e)}")
        return None

def show_ai_question_generator():
    st.title("AI 질문 생성기 (메모기반) 🤖")

    categories = list(st.session_state.memos.keys())
    if categories:
        selected_category = st.selectbox("카테고리 선택", categories)
        
        if st.button("질문 생성하기"):
            if selected_category:
                st.session_state.current_category = selected_category
                memo_items = st.session_state.memos[selected_category]
                if memo_items:
                    title, memo = random.choice(list(memo_items.items()))
                    with st.spinner("질문 생성 중..."):
                        generated_question = generate_question(memo)
                        if generated_question:
                            st.session_state.generated_question = generated_question
                            st.session_state.user_answer = ""
                            st.write(f"**생성된 질문:** {generated_question}")
                else:
                    st.warning("이 카테고리에는 메모가 없습니다.")
            else:
                st.warning("카테고리를 선택해주세요.")

        if st.session_state.generated_question:
            st.session_state.user_answer = st.text_input("답변을 입력하세요", st.session_state.user_answer)
            
            if st.button("피드백 받기"):
                if st.session_state.user_answer.strip() == "":
                    st.warning("답변을 입력해 주세요.")
                else:
                    with st.spinner("피드백 생성 중..."):
                        feedback = provide_feedback(st.session_state.generated_question, st.session_state.user_answer)
                        if feedback:
                            st.write(f"**피드백:** {feedback}")
    else:
        st.warning("저장된 메모가 없습니다. 먼저 메모를 작성해주세요.")

def main():
    show_ai_question_generator()

if __name__ == "__main__":
    main()