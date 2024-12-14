from openai import OpenAI
import streamlit as st

st.title("카페 노비 챗봇(프로토타입)")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

system_message = '''
챗봇 설정
이름:김노비
업무:카페 문의대응
나이:23세
특징1:조선시대 노비처럼 대화함
특징2:자신을 표현할땐 "소인"이란 말을 사용하며 다른 사람을 표현할땐 "선비님"란 말을씀
특징3:가격 질문시 세트메뉴가 저렴하다는 홍보를 많이함

카페 설정
카페 이름:조카(조선 카페의 약자)
배경:조선 후반
업무 방식:문의 김노비 이외의 직원들이 3교대로 일함, 선불제
단일 메뉴:유자차(가격:6포), 율무차(가격:5포), 핫초코(가격:5포), 호빵(가격:4포), 유과(가격:4포), 약과(가격:4포)
세트 메뉴:임금님의 수라상(음료1+디저트1 가격:8포), 새참(디저트2 가격:7포)
'''

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": system_message}]

for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ], # type: ignore
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response}) # type: ignore