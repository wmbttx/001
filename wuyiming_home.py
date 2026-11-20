# -*- coding: utf-8 -*-
"""
创赛营根据地 - 按需导入版
依赖：streamlit requests qqmusic-api-python
运行：streamlit run wuyiming_home.py
"""

import streamlit as st

st.set_page_config(page_title="创赛营根据地", page_icon="🐍", layout="wide")

DARK_CSS = """<style>
.stApp,[data-testid="stAppViewContainer"]{background:#0e1117!important;color:#e6e6e6!important}
[data-testid="stSidebar"]{background:#161b22!important}
[data-testid="stSidebar"] *{color:#e6e6e6!important}
h1,h2,h3,h4,h5,h6,p,span,label,div{color:#e6e6e6!important}
input,textarea,[data-baseweb="input"],[data-baseweb="textarea"]{background:#1c2128!important;color:#e6e6e6!important}
.stButton>button,.stDownloadButton>button{background:#21262d!important;color:#e6e6e6!important;border:1px solid #30363d!important}
code,pre{background:#1c2128!important;color:#7ee787!important}
hr{border-color:#30363d!important}
</style>"""

PAGES = ["首页", "下载", "音乐", "私人词典", "调查", "导航", "时间", "关于"]


def main():
    if "dark" not in st.session_state:
        st.session_state["dark"] = False
    st.sidebar.title("🐍 根据地")
    if hasattr(st.sidebar, "toggle"):
        st.sidebar.toggle("🌙 暗黑", key="dark")
    else:
        st.sidebar.checkbox("🌙 暗黑", key="dark")
    page = st.sidebar.radio("导航", PAGES)
    st.sidebar.caption("v9.18.8.1.3.0")

    if st.session_state.get("dark"):
        st.markdown(DARK_CSS, unsafe_allow_html=True)

    from common import bump_visit
    if "_visited" not in st.session_state:
        st.session_state["_visited"] = bump_visit()

    try:
        if page == "首页":
            import pages_home
            pages_home.render()
        elif page == "下载":
            import pages_download
            pages_download.render()
        elif page == "音乐":
            import pages_music
            pages_music.render()
        elif page == "私人词典":
            import pages_dict
            pages_dict.render()
        elif page == "调查":
            import pages_survey
            pages_survey.render()
        elif page == "导航":
            import pages_links
            pages_links.render()
        elif page == "时间":
            import pages_time
            pages_time.render()
        elif page == "关于":
            import pages_about
            pages_about.render()
    except Exception as e:
        st.error(f"出错：{e}")


if __name__ == "__main__":
    main()
