# -*- coding: utf-8 -*-
import platform

import streamlit as st
from common import VERSION


def render():
    st.subheader("ℹ️ 关于")
    st.write(f"- 版本：**{VERSION}**")
    st.write(f"- Python：**{platform.python_version()}**")
    st.write("- Streamlit 轻量版")