import json  # JSON 파싱
import streamlit as st
import boto3
import random

st.set_page_config(page_title="AI 질문 생성기 (메모기반)", page_icon="🤖")

# Initialize session state if necessary
if 'memos' not in st.session_state:
    st.session_state.memos = {}
if 'categories' not in st.session_state:
    st.session_state.categories = []
if 'current_category' not in st.session_state:
    st.session_state.current_category = None

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def generate_question(prompt):
    try:
        history = [{
            "role": "user",
            "content": [{"type": "text", "text": "다음 메모 내용을 바탕으로 질문을 생성하세요: " + prompt}]
        }]
        
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": history
            }
        )

        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
        )

        # Print the response for debugging
        response_body = json.loads(response["body"].read().decode())
        st.write("API 응답:", response_body)  # For debugging

        # Check the actual keys in the response
        if "completions" in response_body:
            generated_question = response_body["completions"][0]["data"]["text"].strip()
        else:
            st.error("API 응답에서 'completions' 키를 찾을 수 없습니다.")
            return None
        
        return generated_question
    
    except Exception as e:
        st.error(f"질문 생성에 실패했습니다: {e}")
        return None

def show_question_generator_page():
    st.title("AI 질문 생성기 (메모기반) 🤖")

    options = st.session_state.get('categories', [])
    
    if options:
        current_category = st.session_state.get('current_category', options[0])
        if current_category not in options:
            current_category = options[0]
        
        selected_category = st.selectbox("분류", options, index=options.index(current_category))
        
        if selected_category:
            st.session_state.current_category = selected_category

            if st.button("질문 생성하기"):
                memo_items = st.session_state.memos.get(selected_category, {})
                if memo_items:
                    title, memo = random.choice(list(memo_items.items()))

                    with st.spinner("질문 생성 중..."):
                        generated_question = generate_question(memo)
                        if generated_question:
                            st.write(f"생성된 질문: {generated_question}")

                            user_answer = st.text_input("답변을 입력하세요")

                            if st.button("정답 확인"):
                                correct_answer = "예상 답변"  # 실제 정답을 설정해 주세요
                                if user_answer.lower() == correct_answer.lower():
                                    st.success("정답입니다!")
                                else:
                                    st.error("정답이 아닙니다. 다시 시도해보세요.")
                else:
                    st.warning("이 카테고리에는 메모가 없습니다.")
    else:
        st.warning("선택된 항목이 없습니다.")

show_question_generator_page()
