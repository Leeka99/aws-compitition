import streamlit as st
import boto3
import json
import random
import re
from botocore.config import Config

# 로그인 상태 검사
if not st.session_state.logged_in:
    st.warning("로그인이 필요합니다.")
    st.stop()  # 로그인되지 않은 경우 이후 코드 실행 중지

# Streamlit 설정
st.set_page_config(page_title="IT 면접 질문 생성기", page_icon="💼")

# AWS Bedrock 클라이언트 설정
def get_bedrock_client():
    try:
        session = boto3.Session()
        client = session.client(
            service_name="bedrock-runtime",
            region_name="us-east-1",
            config=Config(
                retries={'max_attempts': 10, 'mode': 'adaptive'}
            )
        )
        return client
    except Exception as e:
        st.error(f"AWS Bedrock 클라이언트 생성 실패: {e}")
        return None

bedrock_runtime = get_bedrock_client()

def get_streaming_response(prompt, max_tokens=1000):
    if not bedrock_runtime:
        st.error("AWS Bedrock 클라이언트가 초기화되지 않았습니다.")
        return ""
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body
        )
        stream = response.get("body")
        if stream:
            text = ""
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    text += chunk_json.get("delta", {}).get("text", "")
            return text
        return ""
    except Exception as e:
        st.error(f"응답 생성 중 오류 발생: {e}")
        return ""

def generate_questions(role):
    prompt = f"다음 IT 직군 '{role}'의 면접을 대비할 수 있는 5개의 질문을 생성하세요. 각 질문은 새로운 줄에 작성해 주세요. 질문 앞에 숫자를 붙이지 마세요."
    response = get_streaming_response(prompt)
    questions = [re.sub(r'^\d+\.\s*', '', q.strip()) for q in response.split('\n') if q.strip()]
    return questions

def generate_feedback(role, question, answer):
    prompt = f"""
    당신은 {role} 직군의 면접관입니다. 다음 질문에 대한 지원자의 답변을 평가하고 구체적인 피드백을 제공해주세요.
    질문: {question}
    답변: {answer}
    다음 형식으로 피드백을 작성해주세요:
    1. 강점: 답변에서 잘한 점
    2. 개선점: 보완이 필요한 부분
    3. 추가 조언: 더 나은 답변을 위한 구체적인 제안
    """
    feedback = get_streaming_response(prompt, max_tokens=1000)
    return feedback

def show_question_generator_page():
    st.title("IT 면접 질문 생성기 💼")
    
    # IT 직군 목록
    job_roles = [
        "소프트웨어 엔지니어",
        "DevOps 엔지니어",
        "사이버 보안 분석가",
        "UI/UX 디자이너",
        "클라우드 엔지니어",
        "AI 엔지니어",
        "웹 개발자",
        "모바일 개발자", 
        "데이터 사이언티스트", 
        "시스템 관리자", 
        "기술 지원", 
        "네트워크 엔지니어"
        ]
    
    # 직군 선택
    st.write("### 직군 선택")
    selected_role = st.selectbox(
        "미리 정의된 직군 목록:",
        ["직접 입력"] + job_roles
    )
    
    # 직군 직접 입력
    if selected_role == "직접 입력":
        st.write("### 직군 직접 입력")
        custom_role = st.text_input(
            "직군을 직접 입력하세요:",
            placeholder="예: 빅데이터 엔지니어"
        )
        selected_role = custom_role
    
    if selected_role:
        st.session_state.current_role = selected_role
        if 'current_question' not in st.session_state:
            st.session_state.current_question = ""
        if st.button("새로운 질문 생성"):
            with st.spinner("질문 생성 중..."):
                questions = generate_questions(selected_role)
                if questions:
                    st.session_state.current_question = random.choice(questions)
                else:
                    st.error("질문 생성에 실패했습니다. 다시 시도해 주세요.")
        if st.session_state.current_question:
            st.write(f"질문: {st.session_state.current_question}")
            user_answer = st.text_area("답변을 입력하세요", height=150)
            
            if st.button("답변 제출 및 피드백 받기"):
                if user_answer:
                    with st.spinner("피드백 생성 중..."):
                        feedback = generate_feedback(selected_role, st.session_state.current_question, user_answer)
                        st.subheader("피드백")
                        st.markdown(feedback)
                else:
                    st.warning("답변을 입력해주세요.")
    else:
        st.warning("직군을 선택하거나 입력해 주세요.")

# 초기화 세션 상태
if 'current_role' not in st.session_state:
    st.session_state.current_role = None

show_question_generator_page()