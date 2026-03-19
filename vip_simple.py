import streamlit as st
import webbrowser

# 只使用第一个接口
API_URL = "https://jx.aidouer.net/?url="

st.set_page_config(page_title="质心视频解析", page_icon="🎬", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎬 质心视频解析</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>输入链接，点击按钮直接跳转</p>", unsafe_allow_html=True)

# 输入框
video_url = st.text_input("", placeholder="例如：https://v.qq.com/x/cover/xxx.html", label_visibility="collapsed")

# 按钮
if st.button("⚡ 解析并播放", type="primary", use_container_width=True):
    if not video_url:
        st.error("请输入视频链接")
    else:
        full_url = API_URL + video_url
        # 生成一个链接，让用户点击（或者直接用 JavaScript 跳转）
        st.markdown(f'### [👉 点击此处播放]({full_url})')
        # 可选：自动用新窗口打开（但可能会被浏览器拦截）
        # 使用 JavaScript 自动跳转（但需要用户允许弹窗）
        js = f"window.open('{full_url}', '_blank');"
        st.components.v1.html(f"<script>{js}</script>", height=0)
        st.success("✅ 如果未自动跳转，请点击上面的链接。")

# 说明
st.markdown("---")
st.caption("⚠️ 本工具使用第三方接口，可能有广告，建议安装广告拦截插件（如 uBlock Origin）。只作学习用。。。。几你太美-------")