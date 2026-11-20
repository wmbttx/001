# -*- coding: utf-8 -*-
import streamlit as st


def render():
    st.subheader("📥 下载中心")
    st.markdown("#### 实用工具（官网下载）")
    tools = [
        ("CPU-Z", "https://www.cpuid.com/softwares/cpu-z.html"),
        ("GPU-Z", "https://www.techpowerup.com/download/techpowerup-gpu-z/"),
        ("CrystalDiskInfo", "https://crystalmark.info/en/software/crystaldiskinfo/"),
        ("PyCharm", "https://www.jetbrains.com/pycharm/download/"),
        ("PDFgear", "https://www.pdfgear.com/"),
        ("Pixpin", "https://pixpin.cn/"),
        ("Free Download Manager", "https://www.freedownloadmanager.org/zh/download.htm"),
        ("PotPlayer", "https://potplayer.daum.net/"),
        ("网易云音乐", "https://music.163.com/"),
        ("Microsoft Edge", "https://www.microsoft.com/zh-cn/edge/download"),
    ]
    for n, u in tools:
        st.link_button(f"🔗 {n}", u, use_container_width=True)

    st.markdown("#### 远程安装包（官网入口）")
    st.markdown("- [ClassIn 官网下载](https://www.classin.com/)")
    st.markdown("- [海龟编辑器2 官网](https://www.codemao.cn/)")