import json
import boto3
import streamlit as st

if not st.session_state.logged_in:
    st.warning("로그인이 필요합니다.")
    st.stop()

st.set_page_config(page_title="AI 챗봇 서비스", page_icon="👨‍🏫👩‍🏫")

bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

st.title("AI 챗봇 서비스👨‍🏫👩‍🏫")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def chunk_handler(chunk):
    text = ""
    chunk_type = chunk.get("type")

    if chunk_type == "message_start":

        role = chunk["message"]["role"]
        text = ""
    elif chunk_type == "content_block_start":

        text = chunk["content_block"]["text"]
    elif chunk_type == "content_block_delta":

        text = chunk["delta"]["text"]
    elif chunk_type == "message_delta":

        stop_reason = chunk["delta"]["stop_reason"]
        text = ""
    elif chunk_type == "message_stop":

        metric = chunk["amazon-bedrock-invocationMetrics"]
        inputTokenCount = metric["inputTokenCount"]
        outputTokenCount = metric["outputTokenCount"]
        firstByteLatency = metric["firstByteLatency"]
        invocationLatency = metric["invocationLatency"]
        text = ""

    print(text, end="")
    return text


def get_streaming_response():
    try:
        prompt = st.session_state.messages[-1]["content"]
        history = []
        for msg in st.session_state.messages:
            history.append({
                "role": msg["role"],
                "content" : [{"type": "text", "text": msg["content"]}]
            })
            
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": history
                
            }
        )

        # stream
        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            # modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=body,
        )
        stream = response.get("body")

        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    yield chunk_handler(chunk_json)
    except Exception as e:
        print(e)


# 사용자로부터 입력 받음
if prompt := st.chat_input("Message Bedrock..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):  # 사용자 메시지 채팅 메시지 버블 생성
        st.markdown(prompt)  # 사용자 메시지 표시

    with st.chat_message("assistant"):  # 보조 메시지 채팅 메시지 버블 생성
        model_output = st.write_stream(get_streaming_response)

    # 보조 응답 세션 상태에 추가
    st.session_state.messages.append({"role": "assistant", "content": model_output})
