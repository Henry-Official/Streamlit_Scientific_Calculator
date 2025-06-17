import streamlit as st
import math
import re

if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'history' not in st.session_state:
    st.session_state.history = []

def evaluate_expression():
    expression = (st.session_state.expression.replace("² ", "**2")
                  .replace("²√", "sqrt")
                  .replace('^','**'))
    expression = re.sub(r'\|([^|]+)\|', r'abs(\1)', expression)
    expression = re.sub(r'(\d+)!', r'factorial(\1)', expression)
    if not expression:
        return

    try:
        safe_locals = { "sqrt": math.sqrt,"sin":math.sin,"cos":math.cos,"log":math.log,
                        'factorial':math.factorial,'abs':abs}
        result = eval(expression, {"__builtins__": {}}, safe_locals)
        expression = (st.session_state.expression.replace("**2","² " )
                      .replace("sqrt","²√" )
                      .replace('**', '^')
                      .replace('factorial',"!"))
        expression = re.sub(r'abs\(([^()]+)\)', r'|\1|', expression)
        expression = re.sub(r'factorial\((\d+)\)', r'\1!', expression)
        history_entry = f"{expression} = {result}"
    except Exception:
        result = "Error"
        history_entry = f"{expression} = Error"

    if st.session_state.history and st.session_state.history[0] == history_entry:
        return

    st.session_state.result = result
    st.session_state.history.insert(0, history_entry)
    st.session_state.history = st.session_state.history[:10]

calc_col, history_col = st.columns([2, 1])

with calc_col:
    with st.container(border=True):
        col1, col2, col3 = st.columns([0.4, 1, 0.1])
        with col2:
            st.title('Calculator')

        st.session_state.expression = st.text_input(
            "", st.session_state.expression
        )
        if 'result' in st.session_state:
            st.markdown(f"#### =`{st.session_state.result}`")

        buttons = [
            ['','','','C',"⌫"],
            ["|x|","*n*!","²√", "(", ")"],
            ["cos","7", "8", "9", "/"],
            ["sin","4", "5", "6", " *"],
            ["log","1", "2", "3", " -"],
            ["x²","xʸ", "0", ".", " +"],
        ]

        for row in buttons:
            cols = st.columns(5)
            for i, label in enumerate(row):
                if label!='':
                    if cols[i].button(label, use_container_width=True):
                        if label == "²√": st.session_state.expression += "²√("
                        elif label == "C": st.session_state.expression = ""
                        elif label == "*n*!": st.session_state.expression += "!"
                        elif label == "|x|": st.session_state.expression += "|"
                        elif label == "xʸ": st.session_state.expression += "^"
                        elif label == "x²": st.session_state.expression += "² "
                        elif label == "sin": st.session_state.expression += "sin("
                        elif label == "cos": st.session_state.expression += "cos("
                        elif label == "log": st.session_state.expression += "log("
                        elif label == "⌫": st.session_state.expression = st.session_state.expression[:-1]
                        else:
                            if label == " +" or label == " *" or label == " -":
                                st.session_state.expression += label[1]
                            else:
                                st.session_state.expression += label
                        st.rerun()


        if st.button("=", use_container_width=True):
            evaluate_expression()
            st.rerun()

with history_col:
    st.markdown("### History\n--------")
    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history):
            expression = entry.split('=')[0].strip()
            if st.button(entry):
                st.session_state.expression = expression
                st.rerun()
    else:
        st.markdown("*No history yet*")
