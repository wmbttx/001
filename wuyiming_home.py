# -*- coding: utf-8 -*-
"""
Python 创赛营根据地 - 轻量版
依赖：streamlit pillow requests
运行：streamlit run app.py
"""

import os
import io
import random
import platform
from datetime import datetime, timezone, timedelta

import streamlit as st

st.set_page_config(page_title="创赛营根据地", page_icon="🐍", layout="wide")

import requests
from PIL import Image, ImageChops

# ========== 常量 ==========
WORD_FILE = "words_space.txt"
TIMES_FILE = "check_out_times.txt"
REPLY_FILE = "reply.txt"
VISIT_FILE = "visit_count.txt"
VERSION = "7.0.0"

ONE_LINERS = ["代码写得好，头发掉得早。", "报错不可怕，可怕的是不知道错在哪。",
              "今天你学 Python 了吗？", "Bug 是程序员的浪漫。", "创赛营根据地，欢迎回家。"]

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


# ========== 工具 ==========
def now_bj():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Asia/Shanghai"))
    except Exception:
        return datetime.now(timezone.utc) + timedelta(hours=8)


def read(path, default=""):
    try:
        if not os.path.exists(path):
            open(path, "w", encoding="utf-8").write(default)
            return default
        return open(path, "r", encoding="utf-8").read()
    except Exception:
        return default


def write(path, content):
    try:
        open(path, "w", encoding="utf-8").write(content)
    except Exception:
        pass


def bump_visit():
    try:
        n = int(read(VISIT_FILE, "0").strip() or 0) + 1
    except ValueError:
        n = 1
    write(VISIT_FILE, str(n))
    return n


def load_words():
    d = {}
    for line in [x for x in read(WORD_FILE).split("\n") if x.strip()]:
        p = line.split("#")
        if len(p) >= 3:
            try:
                d[p[1]] = [int(p[0]), p[2]]
            except ValueError:
                continue
    return d


def load_times():
    d = {}
    for line in [x for x in read(TIMES_FILE).split("\n") if x.strip()]:
        p = line.split("#")
        if len(p) >= 2:
            try:
                d[int(p[0])] = int(p[1])
            except ValueError:
                continue
    return d


def save_times(d):
    write(TIMES_FILE, "\n".join(f"{k}#{v}" for k, v in d.items()))


def save_words(d):
    write(WORD_FILE, "\n".join(f"{v[0]}#{k}#{v[1]}" for k, v in d.items()))


def link(name, url):
    st.markdown(f"- [{name}]({url})")


# ========== 音乐搜索（简化，失败给手动链接） ==========
def render_music():
    st.subheader("🎵 音乐搜索")
    kw = st.text_input("🔍 歌曲名或歌手", placeholder="例如：周杰伦、晴天")
    if not kw:
        st.info("输入关键词后按回车搜索。")
        return

    songs = None
    try:
        from qqmusic_api import Client
        import asyncio

        async def _s():
            async with Client() as c:
                return await c.search.search_by_type(keyword=kw, num=10)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            res = loop.run_until_complete(_s())
        finally:
            loop.close()

        data = getattr(res, "body", res)
        if isinstance(data, dict):
            for k in ["req_1", "req_0", "data"]:
                if k in data:
                    data = data[k]
            if "body" in data:
                data = data["body"]
            if "song" in data:
                data = data["song"]
            songs = data.get("list") if isinstance(data, dict) else None
    except Exception:
        songs = None

    if not songs:
        st.warning("在线搜索暂不可用，可手动前往音乐平台搜索：")
        st.markdown(f"- [QQ音乐「{kw}」](https://y.qq.com/n/ryqq/search?w={kw})")
        st.markdown(f"- [网易云「{kw}」](https://music.163.com/#/search/m/?s={kw})")
        return

    for s in songs[:10]:
        try:
            name = s.get("name") or s.get("title") or "未知"
            singers = "、".join(x.get("name", "") for x in s.get("singer", [])) or "未知"
            mid = s.get("mid") or s.get("songmid", "")
            c1, c2 = st.columns([4, 1])
            c1.write(f"**{name}** — {singers}")
            if mid:
                c2.markdown(f"[试听](https://y.qq.com/n/ryqq/songDetail/{mid})")
        except Exception:
            continue
    st.caption("受版权限制，页面内不直接播放。")


# ========== 页面 ==========
def render_home():
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


def render_download():
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


def render_image():
    st.subheader("🌋 图片处理")
    f = st.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
    if not f:
        return
    try:
        img = Image.open(f).convert("RGB")
    except Exception as e:
        st.error(f"读取失败：{e}")
        return

    mode = st.selectbox("处理", ["原图", "通道重排", "灰度", "反色", "水平翻转", "旋转 90°"])
    scale = st.slider("缩放 (%)", 10, 100, 100, 5)

    try:
        if mode == "原图":
            out = img
        elif mode == "通道重排":
            r, g, b = img.split()
            out = Image.merge("RGB", (g, b, r))
        elif mode == "灰度":
            out = img.convert("L").convert("RGB")
        elif mode == "反色":
            out = ImageChops.invert(img)
        elif mode == "水平翻转":
            out = img.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            out = img.rotate(90, expand=True)
        if scale < 100:
            w, h = out.size
            out = out.resize((max(1, int(w * scale / 100)), max(1, int(h * scale / 100))))

        c1, c2 = st.columns(2)
        c1.image(img, caption="原图", use_column_width=True)
        c2.image(out, caption=f"{mode} / {scale}%", use_column_width=True)
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        st.download_button("💾 下载结果", buf.getvalue(), "processed.png", "image/png")
    except Exception as e:
        st.error(f"处理失败：{e}")


def render_dict():
    st.subheader("📖 私人词典")
    words = load_words()
    times = load_times()
    t1, t2, t3 = st.tabs(["查询", "新增", "热词榜"])

    with t1:
        with st.form("q"):
            w = st.text_input("单词")
            ok = st.form_submit_button("🔍 查询")
        if ok and w:
            if w in words:
                wid, meaning = words[w]
                st.success(f"**{w}** — {meaning}")
                times[wid] = times.get(wid, 0) + 1
                save_times(times)
                st.caption(f"查询 {times[wid]} 次")
                if w.lower() == "python":
                    st.code("print('hello world')")
            else:
                st.warning("未收录")

    with t2:
        with st.form("a"):
            nw = st.text_input("新单词")
            nm = st.text_area("解释")
            sub = st.form_submit_button("➕ 添加")
        if sub:
            if not nw or not nm:
                st.error("不能为空")
            elif nw in words:
                st.error("已存在")
            else:
                nid = max((v[0] for v in words.values()), default=0) + 1
                words[nw] = [nid, nm]
                save_words(words)
                st.success(f"已添加 {nw}")

    with t3:
        if times:
            rows = sorted(
                [{"单词": k, "次数": times.get(v[0], 0), "解释": v[1]} for k, v in words.items()],
                key=lambda x: -x["次数"])[:10]
            st.table(rows)
        else:
            st.info("暂无记录")


def render_survey():
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


def render_links():
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


def render_time():
    st.subheader("⏰ 时间（北京时间）")
    if st.button("🔄 刷新"):
        st.rerun()
    st.markdown(f"### {now_bj():%Y-%m-%d %H:%M:%S}")
    st.caption(f"服务器：{platform.system()} {platform.release()}")


def render_about():
    st.subheader("ℹ️ 关于")
    st.write(f"- 版本：**{VERSION}**")
    st.write(f"- Python：**{platform.python_version()}**")
    st.write("- Streamlit 轻量版")


# ========== 路由 ==========
PAGES = {
    "首页": render_home, "下载": render_download, "音乐": render_music,
    "图片处理": render_image, "私人词典": render_dict, "调查": render_survey,
    "导航": render_links, "时间": render_time, "关于": render_about,
}


def main():
    if "dark" not in st.session_state:
        st.session_state["dark"] = False
    st.sidebar.title("🐍 根据地")
    if hasattr(st.sidebar, "toggle"):
        st.sidebar.toggle("🌙 暗黑", key="dark")
    else:
        st.sidebar.checkbox("🌙 暗黑", key="dark")
    page = st.sidebar.radio("导航", list(PAGES))
    st.sidebar.caption(f"v{VERSION}")
    if st.session_state.get("dark"):
        st.markdown(DARK_CSS, unsafe_allow_html=True)
    if "_visited" not in st.session_state:
        st.session_state["_visited"] = bump_visit()
    try:
        PAGES[page]()
    except Exception as e:
        st.error(f"出错：{e}")


if __name__ == "__main__":
    main()
