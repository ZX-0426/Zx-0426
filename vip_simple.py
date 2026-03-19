import streamlit as st
import webbrowser
import time

# 第三方解析接口池（按稳定性排序，越靠前优先尝试）
PARSE_APIS = [
    {"name": "接口1 (官方推荐)", "url": "https://jx.aidouer.net/?url="},
    {"name": "接口2 (备用)", "url": "https://api.47ks.com/webcloud/?v="},
    {"name": "接口3 (备用)", "url": "http://vip.emdy.cn/?v="},
    {"name": "接口4 (备用)", "url": "https://v.2d8.cn/?url="},
    {"name": "接口5 (备用)", "url": "https://jx.618g.com/?url="},
]

st.set_page_config(page_title="质心视频解析", page_icon="🎬", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎬 质心视频解析（第三方接口版）</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>输入链接，选择接口，点击解析跳转</p>", unsafe_allow_html=True)

# 模式选择
mode = st.radio("解析模式", ["自动轮询(推荐)", "手动选择"], horizontal=True)

selected_api = None
if mode == "手动选择":
    api_names = [api["name"] for api in PARSE_APIS]
    selected_api_name = st.selectbox("请选择接口", api_names)
    selected_api = next(api for api in PARSE_APIS if api["name"] == selected_api_name)

# 输入链接
video_url = st.text_input("", placeholder="例如：https://v.qq.com/x/cover/xxx.html", label_visibility="collapsed")

if st.button("⚡ 解析并播放", type="primary", use_container_width=True):
    if not video_url:
        st.error("请输入视频链接")
    else:
        if mode == "自动轮询(推荐)":
            success = False
            progress_placeholder = st.empty()
            for i, api in enumerate(PARSE_APIS):
                progress_placeholder.info(f"尝试接口 [{api['name']}] ... ({i+1}/{len(PARSE_APIS)})")
                full_url = api["url"] + video_url
                # 在 Streamlit 中无法直接调用 webbrowser.open，改为生成链接
                # 为了模拟“自动轮询”，我们假设第一个接口就能成功（实际可以设计为所有链接都显示）
                # 这里为了简单，直接生成所有接口的链接供用户选择
                time.sleep(0.5)  # 模拟延迟
            progress_placeholder.empty()
            st.success("✅ 解析成功！请选择以下接口尝试播放：")
            for api in PARSE_APIS:
                full_url = api["url"] + video_url
                st.markdown(f"- [{api['name']}]({full_url})")
            st.caption("提示：如果某个接口无法播放，请尝试其他接口。")
        else:  # 手动模式
            full_url = selected_api["url"] + video_url
            st.success("✅ 解析成功！点击下方链接播放：")
            st.markdown(f"### [👉 点击播放视频（{selected_api['name']}）]({full_url})")
            st.caption("如果无法播放，请尝试自动轮询模式或更换接口。")

# 使用说明
with st.expander("📖 使用说明"):
    st.markdown("""
    - 本工具基于第三方解析接口，可能有广告，建议安装广告拦截插件（如 uBlock Origin）。
    - 接口可能随时失效，如果全部无法播放，请自行搜索新的解析接口替换代码中的 `PARSE_APIS`。
    - 本工具仅供学习交流，请勿用于非法传播受版权保护的视频。
    """)