# -*- coding: utf-8 -*-
import streamlit as st
from common import link


def render():
    st.subheader("🧭 导航")
    for g, items in {
        "搜索": [("百度", "https://www.baidu.com"), ("Edge", "https://cn.bing.com/")],
        "娱乐": [("B站", "https://www.bilibili.com"), ("抖音", "https://www.douyin.com")],
        "开发": [("GitHub", "https://github.com"), ("Streamlit", "https://streamlit.io/")],
        "编程猫": [("官网", "https://www.codemao.cn"), ("代码岛", "https://box3.codemao.cn")],
    }.items():
        st.markdown(f"#### {g}")
        for n, u in items:
            link(n, u)