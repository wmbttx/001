# -*- coding: utf-8 -*-
"""
Python 创赛营根据地 - Streamlit 首页（稳定版）
运行：streamlit run app.py
"""

import os
import time
import json
import platform
import random
import io

import streamlit as st

# ========== 必须：set_page_config 放在最顶部，且只调用一次 ==========
st.set_page_config(page_title="Python 创赛营根据地", page_icon="🐍", layout="wide")

import numpy as np
import pandas as pd
import requests
from PIL import Image

# ============================================================
# 常量
# ============================================================
PCL_FILE = "./PCL.exe"
TODESK_FILE = "./ToDesk(远程桌面) 安装包.exe"
HAIGUI2_URL = ("https://static.codemao.cn/turtle/client/release/"
               "%E6%B5%B7%E9%BE%9F%E7%BC%96%E8%BE%91%E5%99%A82-x64-2.4.0.exe")
CLASSIN_URL = "https://download.eeo.cn/client/classin_win_install_5.1.1.54_x64.exe"

WORD_FILE = "words_space.txt"
TIMES_FILE = "check_out_times.txt"
MESSAGE_FILE = "leave_messages.txt"
REPLY_FILE = "reply.txt"
VISIT_FILE = "visit_count.txt"

APP_VERSION = "5.2.0"
ROLES = {"阿短": "🌞", "编程猫": "🍥", "小黑子": "🐔", "路人甲": "👤"}

ONE_LINERS = [
    "代码写得好，头发掉得早。",
    "报错不可怕，可怕的是不知道错在哪。",
    "今天你学 Python 了吗？",
    "Bug 是程序员的浪漫。",
    "创赛营根据地，欢迎回家。",
    "多写一行注释，少熬一个通宵。",
    "Ctrl+S 是程序员的安全感。",
]

# ============================================================
# 暗黑模式 CSS
# ============================================================
DARK_CSS = """
<style>
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #0e1117 !important;
    color: #e6e6e6 !important;
}
[data-testid="stSidebar"] { background-color: #161b22 !important; }
[data-testid="stSidebar"] * { color: #e6e6e6 !important; }
h1, h2, h3, h4, h5, h6, p, span, label, div { color: #e6e6e6 !important; }
input, textarea, [data-baseweb="input"], [data-baseweb="textarea"],
[data-baseweb="select"] > div {
    background-color: #1c2128 !important;
    color: #e6e6e6 !important;
    border-color: #30363d !important;
}
.stButton > button, .stDownloadButton > button,
[data-testid="stFormSubmitButton"] > button {
    background-color: #21262d !important;
    color: #e6e6e6 !important;
    border: 1px solid #30363d !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #30363d !important;
}
[data-testid="stMetric"] {
    background-color: #161b22 !important;
    padding: 8px; border-radius: 8px;
}
[data-testid="stChatMessage"] { background-color: #161b22 !important; }
code, pre { background-color: #1c2128 !important; color: #7ee787 !important; }
hr { border-color: #30363d !important; }
[data-testid="stExpander"] details { background-color: #161b22 !important; }
button[data-baseweb="tab"] { color: #e6e6e6 !important; }
</style>
"""


# ============================================================
# 安全工具（全部 try/except，单点失败不影响整体）
# ============================================================
def safe_read(path, default=""):
    try:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(default)
            return default
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return default


def safe_write(path, content):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False


def img_change(img, rc, gc, bc):
    arr = np.array(img.convert("RGB"))
    return Image.fromarray(arr[:, :, [rc, gc, bc]])


@st.cache_data(show_spinner=False)
def fetch_bytes(url):
    return requests.get(url, timeout=60).content


@st.cache_data(show_spinner=False)
def load_words():
    words_dict = {}
    for item in [w for w in safe_read(WORD_FILE).split("\n") if w.strip()]:
        parts = item.split("#")
        if len(parts) >= 3:
            try:
                words_dict[parts[1]] = [int(parts[0]), parts[2]]
            except ValueError:
                continue
    return words_dict


@st.cache_data(show_spinner=False)
def load_times():
    times_dict = {}
    for line in [x for x in safe_read(TIMES_FILE).split("\n") if x.strip()]:
        parts = line.split("#")
        if len(parts) >= 2:
            try:
                times_dict[int(parts[0])] = int(parts[1])
            except ValueError:
                continue
    return times_dict


def save_times(d):
    safe_write(TIMES_FILE, "\n".join(f"{k}#{v}" for k, v in d.items()))


def save_words(d):
    safe_write(WORD_FILE, "\n".join(f"{v[0]}#{k}#{v[1]}" for k, v in d.items()))


def bump_visit():
    try:
        cnt = int(safe_read(VISIT_FILE, "0").strip() or 0) + 1
    except ValueError:
        cnt = 1
    safe_write(VISIT_FILE, str(cnt))
    return cnt


def link_item(name, url):
    st.markdown(f"- [{name}]({url})")


# ============================================================
# 页面：首页
# ============================================================
def render_home():
    st.markdown("## :orange[:sunglasses: Python 创赛营根据地 :sunglasses:]")
    st.markdown("### :red[欢] :sunglasses: :blue[迎] :sunglasses: :green[~]")

    c1, c2, c3 = st.columns(3)
    c1.metric("当前时间", time.strftime("%H:%M:%S"))
    c2.metric("访客累计", st.session_state.get("_visited", 0))
    c3.metric("模式", "🌙 暗黑" if st.session_state.get("dark_mode") else "☀️ 亮色")
    st.info(f"💬 {random.choice(ONE_LINERS)}")
    st.write("---")
    st.text("""这里是 Python 创赛营根据地，由各位优秀的同学们一起建设。
你是否为了程序的报错而抓耳挠腮？或者是为找不到小黑子而烦恼呢？
那这里，你都可以解决这些。""")
    st.snow()

    name = st.text_input("请输入你的名字：", value=st.session_state.get("user_name", ""))
    if name:
        st.session_state["user_name"] = name
        st.success(f"你好呀，{name} 👋 欢迎来到根据地！")


# ============================================================
# 页面：下载
# ============================================================
def render_download():
    st.subheader("📥 软件下载中心")
    st.markdown("#### 本地文件下载")
    for label, path, fname in [
        ("我的世界 PCL 启动器", PCL_FILE, "PCL我的世界启动器.exe"),
        ("ToDesk 远程桌面", TODESK_FILE, "ToDesk安装包.exe"),
    ]:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    st.download_button(f"下载 {label}", f.read(), file_name=fname,
                                       mime="application/octet-stream", key=f"local_{fname}")
            except Exception as e:
                st.warning(f"读取 {label} 失败：{e}")
        else:
            st.warning(f"⚠️ 未找到 `{path}`，请将文件放入项目目录")

    st.markdown("#### 远程安装包下载")
    for label, url, fname in [
        ("ClassIn 安装包 (64位)", CLASSIN_URL, "classin_install_x64.exe"),
        ("海龟编辑器2 安装包 (64位)", HAIGUI2_URL, "haigui2_x64.exe"),
    ]:
        if st.button(f"获取 {label}", key=f"fetch_{fname}"):
            with st.spinner("正在拉取文件..."):
                try:
                    st.session_state[f"remote_{fname}"] = fetch_bytes(url)
                    st.success("拉取成功，请点击下方按钮保存")
                except Exception as e:
                    st.error(f"下载失败：{e}")
        if st.session_state.get(f"remote_{fname}"):
            st.download_button(f"💾 保存 {label}", st.session_state[f"remote_{fname}"],
                               file_name=fname, mime="application/octet-stream",
                               key=f"save_{fname}")

    st.info("下载打开后如果出错，请移动到其他文件夹并以管理员权限运行！！！")
    if os.path.exists("001.png"):
        st.image("001.png", caption="使用说明")
    st.snow()


# ============================================================
# 页面：音乐
# ============================================================
SONGS = [
    ("纯音乐", "Void", "Void.mp3"),
    ("纯音乐", "【FREE】lucky", "FREElucky.mp3"),
    ("纯音乐", "Daylight", "Daylight.mp3"),
    ("英文歌", "See You Again", "SeeYouAgain.mp3"),
    ("英文歌", "Love is gone", "loveisgone.mp3"),
    ("英文歌", "Stay", "stay.mp3"),
]


def render_music():
    st.subheader("🎵 音乐厅")
    keyword = st.text_input("🔍 搜索歌曲", "").strip().lower()
    current_cat = None
    for cat, title, path in SONGS:
        if keyword and keyword not in title.lower() and keyword not in cat.lower():
            continue
        if cat != current_cat:
            st.markdown(f"### {cat}")
            current_cat = cat
        st.write(f"**{title}**")
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3", start_time=0)
            except Exception:
                st.caption(f"⚠️ 无法播放 `{path}`")
        else:
            st.caption(f"⚠️ 缺少文件 `{path}`")
    st.write("---")
    st.caption("*下载音乐后如为文件，请直接用 Windows 音频播放器或 QQ 音乐播放即可！*")


# ============================================================
# 页面：图片处理
# ============================================================
def render_image():
    st.subheader("🌋 图片处理小程序")
    uploaded = st.file_uploader("上传图片", type=["png", "jpeg", "jpg"])
    if not uploaded:
        return
    try:
        img = Image.open(uploaded).convert("RGB")
    except Exception as e:
        st.error(f"图片读取失败：{e}")
        return

    mode = st.selectbox("处理方式", ["原图", "通道重排 (R←G, G←B, B←R)",
                                    "灰度", "反色", "水平翻转", "旋转 90°"])
    scale = st.slider("缩放 (%)", 10, 100, 100, 5)

    try:
        if mode == "原图":
            out = img
        elif mode.startswith("通道重排"):
            out = img_change(img, 1, 2, 0)
        elif mode == "灰度":
            out = img.convert("L").convert("RGB")
        elif mode == "反色":
            out = Image.fromarray(255 - np.array(img))
        elif mode == "水平翻转":
            out = img.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            out = img.rotate(90, expand=True)

        if scale < 100:
            w, h = out.size
            out = out.resize((max(1, int(w * scale / 100)), max(1, int(h * scale / 100))))

        c1, c2 = st.columns(2)
        c1.image(img, caption="原图", use_column_width=True)
        c2.image(out, caption=f"处理后：{mode} / {scale}%", use_column_width=True)

        buf = io.BytesIO()
        out.save(buf, format="PNG")
        st.download_button("💾 下载处理结果", buf.getvalue(),
                           file_name="processed.png", mime="image/png")
    except Exception as e:
        st.error(f"处理失败：{e}")


# ============================================================
# 页面：私人词典
# ============================================================
def render_dict():
    st.subheader("📖 我的私人词典")
    words_dict = load_words()
    times_dict = load_times()
    tab1, tab2, tab3 = st.tabs(["查询", "新增单词", "热词榜"])

    with tab1:
        word = st.text_input("请输入要查询的单词", key="dict_query")
        if word:
            if word in words_dict:
                wid, meaning = words_dict[word]
                st.success(f"**{word}** — {meaning}")
                times_dict[wid] = times_dict.get(wid, 0) + 1
                save_times(times_dict)
                st.caption(f"该词累计查询 {times_dict[wid]} 次")
                if word.lower() == "python":
                    st.code("# 恭喜触发彩蛋：\nprint('hello world')", language="python")
            else:
                st.warning(f"未收录 `{word}`，去「新增单词」页添加吧")

    with tab2:
        with st.form("add_word"):
            nw = st.text_input("单词")
            nm = st.text_area("解释")
            sub = st.form_submit_button("➕ 添加")
        if sub:
            if not nw or not nm:
                st.error("单词和解释都不能为空")
            elif nw in words_dict:
                st.error("该单词已存在")
            else:
                nid = max((v[0] for v in words_dict.values()), default=0) + 1
                words_dict[nw] = [nid, nm]
                save_words(words_dict)
                st.cache_data.clear()
                st.success(f"已添加：{nw}")

    with tab3:
        if times_dict:
            df = pd.DataFrame(
                [{"单词": k, "查询次数": times_dict.get(v[0], 0), "解释": v[1]}
                 for k, v in words_dict.items()]
            ).sort_values("查询次数", ascending=False).head(10)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("暂无查询记录")


# ============================================================
# 页面：留言区
# ============================================================
def load_messages():
    result = []
    for x in [i for i in safe_read(MESSAGE_FILE).split("\n") if i.strip()]:
        parts = x.split("#")
        if len(parts) >= 3:
            result.append([parts[0], parts[1], "#".join(parts[2:])])
    return result


def save_messages(msgs):
    safe_write(MESSAGE_FILE, "\n".join("#".join(i) for i in msgs))


def render_messages():
    st.subheader("💬 我的留言区")
    messages = load_messages()
    st.caption(f"共 {len(messages)} 条留言" if messages else "还没有留言，快来抢沙发～")

    for idx, (mid, role, msg) in enumerate(messages):
        col_msg, col_del = st.columns([9, 1])
        with col_msg:
            with st.chat_message(ROLES.get(role, "👤")):
                st.write(f"**{role}**：{msg}")
                st.caption(f"#{mid}")
        with col_del:
            st.write("")
            if st.button("🗑️", key=f"del_{mid}_{idx}", help="删除这条留言"):
                st.session_state["pending_delete"] = idx
                st.rerun()

    if st.session_state.get("pending_delete") is not None:
        idx = st.session_state["pending_delete"]
        if 0 <= idx < len(messages):
            t = messages[idx]
            st.warning(f"确定删除 `#{t[0]} {t[1]}` 的留言？")
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("✅ 确认删除", key="confirm_del"):
                messages.pop(idx)
                save_messages(messages)
                st.session_state["pending_delete"] = None
                st.success("已删除")
                st.rerun()
            if c2.button("❌ 取消", key="cancel_del"):
                st.session_state["pending_delete"] = None
                st.rerun()

    st.write("---")
    with st.form("leave_msg", clear_on_submit=True):
        name = st.selectbox("我是……", list(ROLES.keys()))
        msg = st.text_input("想要说的话……")
        sub = st.form_submit_button("留言")
    if sub:
        if not msg.strip():
            st.error("留言不能为空")
        else:
            last_id = int(messages[-1][0]) if messages else 0
            messages.append([str(last_id + 1), name, msg])
            save_messages(messages)
            st.success("留言成功")
            st.rerun()

    if messages and st.button("🧹 清空所有留言"):
        st.session_state["confirm_clear"] = True
    if st.session_state.get("confirm_clear"):
        st.error("⚠️ 确定清空所有留言？不可撤销！")
        c1, c2, _ = st.columns([1, 1, 6])
        if c1.button("确认清空", key="yes_clear"):
            save_messages([])
            st.session_state["confirm_clear"] = False
            st.success("已清空")
            st.rerun()
        if c2.button("取消", key="no_clear"):
            st.session_state["confirm_clear"] = False
            st.rerun()


# ============================================================
# 页面：调查 / 导航 / 时间 / 关于
# ============================================================
def render_survey():
    st.subheader("📋 调查问卷")
    with st.form("survey_form"):
        q1 = st.text_input("1. 你对这个网页的评价：")
        q2 = st.text_input("2. 你还想添加些什么？")
        q3 = st.text_input("3. 我们哪里可以优化：")
        q4 = st.text_input("4. 音乐还可以添加什么：")
        q5 = st.text_input("5. 你喜欢什么游戏：")
        sub = st.form_submit_button("提交")
    if sub:
        try:
            with open(REPLY_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n"
                        f"1. {q1}\n2. {q2}\n3. {q3}\n4. {q4}\n5. {q5}\n---\n")
            st.success("提交成功，感谢反馈！")
        except Exception as e:
            st.error(f"保存失败：{e}")
    with st.expander("查看历史反馈"):
        st.text(safe_read(REPLY_FILE) or "暂无历史反馈")


def render_links():
    st.subheader("🧭 网页导航")
    groups = {
        "🔍 搜索": [("百度", "https://www.baidu.com"),
                    ("Edge 搜索", "https://cn.bing.com/"),
                    ("百度翻译", "https://fanyi.baidu.com")],
        "🎬 娱乐": [("哔哩哔哩", "https://www.bilibili.com"),
                    ("抖音", "https://www.douyin.com"),
                    ("爱奇艺", "https://www.iqiyi.com")],
        "💻 开发": [("GitHub", "https://github.com"),
                    ("Streamlit 官网", "https://streamlit.io/")],
        "🛒 生活": [("淘宝", "https://www.taobao.com")],
        "🐢 编程猫系": [("我的世界中文网", "https://www.minecraftzw.com"),
                        ("编程猫官网", "https://www.codemao.cn"),
                        ("编程猫神奇代码岛", "https://box3.codemao.cn")],
    }
    for g, items in groups.items():
        st.markdown(f"#### {g}")
        for name, url in items:
            link_item(name, url)
        st.write("")


def render_time():
    st.subheader("⏰ 当前时间")
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=1000, key="clock")
    except ImportError:
        st.caption("未安装 streamlit-autorefresh，时间不会自动刷新")
    st.markdown(f"### {time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption(f"系统：{platform.system()} {platform.release()}")


def render_about():
    st.subheader("ℹ️ 关于本站")
    st.write(f"- 网页版本：**{APP_VERSION}**")
    st.write(f"- Python：**{platform.python_version()}**")
    st.write(f"- 平台：**{platform.system()} {platform.release()}**")
    st.write("- 使用 Python + Streamlit 搭建")
    st.markdown("感谢大家的支持！ 🙏")


# ============================================================
# 路由 + 主函数
# ============================================================
PAGES = {
    "首页": render_home,
    "下载": render_download,
    "音乐": render_music,
    "图片处理": render_image,
    "我的私人词典": render_dict,
    "留言区": render_messages,
    "调查": render_survey,
    "网页导航": render_links,
    "时间": render_time,
    "关于": render_about,
}


def main():
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False

    st.sidebar.title("🐍 创赛营根据地")

    # 兼容低版本 Streamlit：没有 toggle 就用 checkbox
    if hasattr(st.sidebar, "toggle"):
        st.sidebar.toggle("🌙 暗黑模式", key="dark_mode")
    else:
        st.sidebar.checkbox("🌙 暗黑模式", key="dark_mode")

    page = st.sidebar.radio("导航", list(PAGES.keys()))
    st.sidebar.markdown("---")
    st.sidebar.caption(f"v{APP_VERSION}")

    if st.session_state.get("dark_mode"):
        st.markdown(DARK_CSS, unsafe_allow_html=True)

    if st.session_state.get("_visited") is None:
        st.session_state["_visited"] = bump_visit()

    try:
        PAGES[page]()
    except Exception as e:
        st.error(f"页面渲染出错：{e}")
        st.exception(e)


if __name__ == "__main__":
    main()
