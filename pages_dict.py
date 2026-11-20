# -*- coding: utf-8 -*-
from urllib.parse import quote

import streamlit as st
from common import load_words, load_times, save_times, save_words


def render():
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
                st.warning("本地词典未收录，可在线查询：")
                enc = quote(w)
                st.markdown(f"👉 [汉典「{w}」](https://www.zdic.net/hans/{enc})")
                st.markdown(f"👉 [百度百科「{w}」](https://baike.baidu.com/item/{enc})")

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