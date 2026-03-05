import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 初始化 (修正 404 報錯)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 繪本工場", page_icon="🧸", layout="wide")

try:
    # 讀取 Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用目前最穩定的型號命名格式
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 金鑰設定錯誤，請檢查 Secrets 是否有雙引號。")
    api_ready = False

# ==========================================
# 2. 介面設計
# ==========================================
st.title("🧸 旺角社區客廳 - 免費 AI 繪本工場")

with st.sidebar:
    st.header("🎨 創作設定")
    art_style = st.selectbox("選擇風格", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "溫馨水彩繪本"])
    st.info("💡 此版本完全免費，不需儲值。")

with st.form("story_form"):
    col1, col2, col3 = st.columns(3)
    with col1: character = st.text_input("📝 主角", value="愛冒險的菠蘿包")
    with col2: location = st.selectbox("🗺️ 地點", ["油麻地果欄", "旺角金魚街", "社區客廳"])
    with col3: theme = st.selectbox("💡 道理", ["學會分享", "鄰里互助"])
    submitted = st.form_submit_button("✨ 生成繪本！", use_container_width=True)

# ==========================================
# 3. 核心邏輯 (修正問號圖問題)
# ==========================================
if submitted and api_ready:
    with st.spinner("魔法創作中..."):
        # 讓 AI 同時生成故事與乾淨的英文指令
        prompt = f"為主角「{character}」在「{location}」寫一個 150 字童話故事，結尾帶出「{theme}」。最後另起一行只寫英文畫圖指令：IMAGE_PROMPT: A cute illustration of {character} in {location}, {art_style} style, 8k"
        
        try:
            response = model.generate_content(prompt)
            full_text = response.text
            
            # 拆分故事與指令
            parts = full_text.split("IMAGE_PROMPT:")
            story_text = parts[0].strip()
            visual_prompt = parts[1].strip() if len(parts) > 1 else f"{character} in {location}, {art_style}"

            # 🌟 視覺修復關鍵：清理所有非英文字元並進行 URL 編碼
            clean_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_prompt)
            encoded_prompt = urllib.parse.quote(clean_prompt)
            
            # 使用穩定的 Pollinations 接口並加入隨機種子
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"

            # 展示成果
            st.markdown("---")
            col_l, col_r = st.columns([1.2, 1])
            with col_l:
                st.subheader("🖼️ 你的專屬插圖")
                st.image(image_url, use_container_width=True) #
            with col_r:
                st.subheader("📖 你的專屬故事")
                st.info(story_text)
                st.success("✅ 完成！")
        except Exception as e:
            st.error(f"魔法失敗：{e}")
