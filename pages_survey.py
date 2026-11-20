# -*- coding: utf-8 -*-
import streamlit as st
from common import REPLY_FILE, read, write, now_bj


def render():
    st.subheader("📋 调查问卷")
    with st.form("s"):
        qs = [st.text_input(f"{i}. {t}") for i, t in enumerate(
            ["评价", "想添加什么", "哪里可优化", "音乐建议", "喜欢的游戏"], 1)]
        ok = st.form_submit_button("提交")
    if ok:
        write(REPLY_FILE, read(REPLY_FILE) + f"[{now_bj():%Y-%m-%d %H:%M:%S}]\n" +
              "\n".join(f"{i}. {q}" for i, q in enumerate(qs, 1)) + "\n---\n")
        st.success("提交成功")
    with st.expander("历史反馈"):
        st.text(read(REPLY_FILE) or "暂无")