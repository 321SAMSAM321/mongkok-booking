import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 智能初始化 (自動解決 404 報錯)
# ==========================================
st.set_page_config(page_title="旺角社區客廳 - 繪本工場", page_icon="🧸", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 請在 Secrets 設定 GEMINI_API_KEY (需加雙引號)")
    st.stop()

# 智能找大腦函數
def get_working_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 嘗試清單：從最新到最穩
    for m_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(m_name)
            # 測試一下能不能說話
            m.generate_content("Hi", safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE'})
            return m
        except:
            continue
    return None

model = get_working_model()

# ==========================================
# 2. 介面設計
# ==========================================
st.title("🎨 旺角社區客廳 - AI 繪本工場 (終極修復版)")
st.markdown("小朋友，只要輸入想法，AI 會幫你寫故事並畫圖！")

with st.sidebar:
    art_style = st.selectbox("🎨 畫畫風格", ["吉卜力動畫風", "迪士尼 3D 風", "暖心水彩繪本"])
    st.info("💡 此版本已強化圖片顯示功能。")

with st.form("story_form"):
    col1, col2, col3 = st.columns(3)
    with col1: character = st.text_input("📝 主角", value="愛冒險的菠蘿包")
    with col2: location = st.selectbox("🗺️ 地點", ["旺角金魚街", "社區客廳", "油麻地果欄"])
    with col3: theme = st.selectbox("💡 道理", ["鄰里互助", "學會分享", "勇敢面對"])
    submitted = st.form_submit_button("✨ 施展魔法，生成繪本！", use_container_width=True)

# ==========================================
# 3. 核心邏輯 (解決藍色問號)
# ==========================================


if submitted:
    if model is None:
        st.error("❌ 找不到可用的 AI 模型，請檢查 API Key 是否有效。")
    else:
        with st.spinner("魔法精靈正在創作中... 🧚‍♂️"):
            prompt = f"你是香港繪本作家，請為「{character}」在「{location}」寫一個150字故事，道理是「{theme}」。最後一行只寫：IMAGE_PROMPT: A cute illustration of {character} in {location}, {art_style} style."
            
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # 拆分故事與指令
                parts = full_text.split("IMAGE_PROMPT:")
                story_text = parts[0].strip()
                visual_desc = parts[1].strip() if len(parts) > 1 else f"{character} in {location}"

                # 🌟 徹底解決藍色問號：清理網址指令
                clean_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_desc)
                encoded_prompt = urllib.parse.quote(clean_prompt)
                
                # 使用最新產圖路徑
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"

                # 展示結果
                st.divider()
                col_l, col_r = st.columns([1.2, 1])
                with col_l:
                    st.subheader("🖼️ 你的專屬插圖")
                    st.image(image_url, use_container_width=True)
                with col_r:
                    st.subheader("📖 你的專屬故事")
                    st.info(story_text)
                    st.success("✅ 魔法成功！")
            except Exception as e:
                st.error(f"魔法失敗：{e}")
