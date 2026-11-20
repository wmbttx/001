# -*- coding: utf-8 -*-
import asyncio
from urllib.parse import quote

import streamlit as st


def render():
    st.subheader("🎵 音乐搜索")
    kw = st.text_input("🔍 歌曲名或歌手", placeholder="例如：See You Again")
    if not kw:
        st.info("输入关键词后按回车搜索。")
        return

    songs = None
    variants = [kw, kw.replace(" ", ""), "+".join(kw.split())]
    for variant in variants:
        try:
            from qqmusic_api import Client

            async def _s(keyword=variant):
                async with Client() as c:
                    return await c.search.search_by_type(keyword=keyword, num=10)

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
            if songs:
                break
        except Exception:
            songs = None

    if not songs:
        st.warning("在线搜索暂不可用，可手动前往音乐平台搜索：")
        enc = quote(kw)
        st.markdown(f"- [QQ音乐「{kw}」](https://y.qq.com/n/ryqq/search?w={enc})")
        st.markdown(f"- [网易云「{kw}」](https://music.163.com/#/search/m/?s={enc})")
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