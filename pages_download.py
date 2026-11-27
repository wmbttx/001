# -*- coding: utf-8 -*-
import streamlit as st


def render():
    st.subheader("📥 下载中心")
    
    # --- 直链下载区 ---
    st.markdown("#### 安装包直链下载")
    st.caption("点击按钮直接下载，或点击代码框右上角的图标复制链接，粘贴到 FDM 等下载工具中。")
    
    ollama_url = "https://cnb.cool/hex/ollama/-/releases/latest/download/OllamaSetup.exe"
    
    # 直接点击下载按钮
    st.link_button(
        "🔗 直接下载 Ollama 安装包 (OllamaSetup.exe)", 
        ollama_url, 
        use_container_width=True
    )
    
    # 用于复制的代码框（自带右上角复制按钮）
    st.code(ollama_url, language="text")
    
    st.markdown("---")

    # --- 官网跳转区 ---
    st.markdown("#### 实用工具（前往官网下载）")
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
