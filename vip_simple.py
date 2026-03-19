import streamlit as st
import yt_dlp
import tempfile
import os

# 页面配置
st.set_page_config(page_title="质心视频解析", page_icon="🎬", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎬 VIP视频解析</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>输入链接，点击按钮，自动跳转播放</p>", unsafe_allow_html=True)

# 侧边栏（上传cookie，仅VIP需要）
with st.sidebar:
    st.markdown("### 🔑 Cookie（可选）")
    st.caption("仅当解析VIP视频时需要，免费视频无需上传。")
    uploaded = st.file_uploader("上传 cookies.txt", type=['txt'])
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            tmp.write(uploaded.getvalue())
            st.session_state['cookie_file'] = tmp.name
        st.success("✅ Cookie已上传")

# 主界面
url = st.text_input("", placeholder="例如：https://v.qq.com/x/cover/xxx.html", label_visibility="collapsed")

if st.button("⚡ 解析并播放", type="primary", use_container_width=True):
    if not url:
        st.error("请输入视频链接")
    else:
        with st.spinner("解析中，请稍候..."):
            ydl_opts = {'quiet': True, 'no_download': True}
            if 'cookie_file' in st.session_state and os.path.exists(st.session_state['cookie_file']):
                ydl_opts['cookiefile'] = st.session_state['cookie_file']
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    # 获取最佳画质的播放地址
                    formats = info.get('formats', [])
                    video_formats = [f for f in formats if f.get('vcodec') != 'none']
                    if video_formats:
                        video_formats.sort(key=lambda f: f.get('height', 0) or 0, reverse=True)
                        play_url = video_formats[0]['url']
                    else:
                        play_url = info.get('url')
                    if play_url:
                        # 自动跳转（使用JavaScript）
                        js = f"window.location.href = '{play_url}';"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
                        st.success("✅ 解析成功，正在跳转...")
                    else:
                        st.error("未找到可播放的地址")
            except Exception as e:
                st.error(f"解析失败: {e}")
                st.caption("可能原因：链接无效、需要登录（请上传cookie）、网站不支持或网络问题。")

# 简单说明
st.markdown("---")
st.caption("💡 免费视频直接解析；VIP视频需在左侧上传一次cookies（浏览器扩展导出）。")