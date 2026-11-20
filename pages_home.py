# -*- coding: utf-8 -*-
import random
import streamlit as st
from common import now_bj, ONE_LINERS


def render():
    st.markdown("## :orange[:sunglasses: Python 创赛营根据地]")
    c1, c2, c3 = st.columns(3)
    c1.metric("时间", now_bj().strftime("%H:%M:%S"))
    c2.metric("访客", st.session_state.get("_visited", 0))
    c3.metric("模式", "🌙" if st.session_state.get("dark") else "☀️")
    st.info(f"💬 {random.choice(ONE_LINERS)}")
    st.text("这里是 Python 创赛营根据地，由各位优秀的同学们一起建设。")
    name = st.text_input("请输入你的名字：", value=st.session_state.get("name", ""))
    if name:
        st.session_state["name"] = name
        st.success(f"你好呀，{name} 👋")