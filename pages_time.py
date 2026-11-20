# -*- coding: utf-8 -*-
import platform

import streamlit as st
from common import now_bj


def render():
    st.subheader("⏰ 时间（北京时间）")
    if st.button("🔄 刷新"):
        st.rerun()
    st.markdown(f"### {now_bj():%Y-%m-%d %H:%M:%S}")
    st.caption(f"服务器：{platform.system()} {platform.release()}")