# -*- coding: utf-8 -*-
import os
from datetime import datetime, timezone, timedelta

WORD_FILE = "words_space.txt"
TIMES_FILE = "check_out_times.txt"
REPLY_FILE = "reply.txt"
VISIT_FILE = "visit_count.txt"
VERSION = "8.0.0"

ONE_LINERS = ["代码写得好，头发掉得早。", "报错不可怕，可怕的是不知道错在哪。",
              "今天你学 Python 了吗？", "Bug 是程序员的浪漫。", "创赛营根据地，欢迎回家。"]


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
    import streamlit as st
    st.markdown(f"- [{name}]({url})")