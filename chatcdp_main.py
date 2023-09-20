import openai
import re
import streamlit as st
# from prompts import get_system_prompt
from table_prompts import tab_system_prompt

from init_prompts import init_get_system_prompt

st.title("ChatCDP")

# Initialize the chat messages history
openai.api_key = st.secrets.OPENAI_API_KEY


# print('st.session_state: ', st.session_state)
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": init_get_system_prompt()},
                                 {"role": "system", "content": tab_system_prompt()}]

# print('st.session_state: ', st.session_state)

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    # print('here: ' , st.chat_message(message["role"]))
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            response += delta.choices[0].delta.get("content", "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        # print('sql_match: ', sql_match)
        if sql_match:
            sql = sql_match.group(1)
            conn = st.experimental_connection("snowpark")
            try:
                res = conn.query(sql)
                # print(res)
                message["results"] = res
                st.dataframe(message["results"])
            except Exception:
                st.write("!!!! Too many columns in output. Not displaying the output. !!!!")

        st.session_state.messages.append(message)