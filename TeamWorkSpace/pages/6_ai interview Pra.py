import streamlit as st
import boto3
import json

# Streamlit 설정
st.set_page_config(page_title="IT 면접 질문 생성기", page_icon="💼")

# AWS Bedrock 클라이언트 설정
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def get_streaming_response(prompt):
    try:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 150,
                "messages": [
                    {
                        "role": "system",
                        "content": [{"type": "text", "text": prompt}]
                    }
                ]
            }
        )

        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # 실제 모델 ID로 변경
            body=body,
        )
        stream = response.get("body")

        if stream:
            text = ""
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    text += chunk_json.get("text", "")
            return text.strip()
    except Exception as e:
        st.error(f"질문 생성에 실패했습니다: {e}")
        return ""

def show_question_generator_page():
    st.title("IT 면접 질문 생성기 💼")

    # IT 직군 목록
    job_roles = ["개발자", "데이터 사이언티스트", "시스템 관리자", "기술 지원", "네트워크 엔지니어"]
    selected_role = st.selectbox("직군 선택", job_roles)

    if selected_role:
        st.session_state.current_role = selected_role

        if st.button("질문 생성하기"):
            prompt = f"다음 IT 직군 '{selected_role}'의 면접을 대비할 수 있는 질문을 생성하세요."
            with st.spinner("질문 생성 중..."):
                question = get_streaming_response(prompt)
                st.write(f"생성된 질문: {question}")

                user_answer = st.text_input("답변을 입력하세요")

                if st.button("정답 확인"):
                    correct_answer = "예상 답변"  # 실제 답변을 설정해 주세요
                    if user_answer.lower() == correct_answer.lower():
                        st.success("정답입니다!")
                    else:
                        st.error("정답이 아닙니다. 다시 시도해보세요.")
    else:
        st.warning("직군을 선택해 주세요.")

# 초기화 세션 상태
if 'current_role' not in st.session_state:
    st.session_state.current_role = None

show_question_generator_page()