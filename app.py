import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 初始化與大腦尋找 (解決 404/找不到模型)
# ==========================================
st.set_page_config(page_title="旺角 AI 繪本工場 - 終極修復", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 請在 Secrets 設定 GEMINI_API_KEY")
    st.stop()

@st.cache_resource
def init_ai():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 嘗試清單：從最先進到最通用
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m_name in models_to_try:
        try:
            m = genai.GenerativeModel(m_name)
            # 測試是否真的能用
            m.generate_content("test", safety_settings={'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE'})
            return m, m_name
        except Exception as e:
            continue
    return None, None

model, active_model_name = init_ai()

# ==========================================
# 2. 介面
# ==========================================
st.title("🧸 旺角社區客廳 - AI 繪本工場")
st.markdown(f"**系統狀態：** {'✅ 已連接 ' + active_model_name if model else '❌ 連接失敗'}")

with st.sidebar:
    art_style = st.selectbox("🎨 風格", ["吉卜力風 (Ghibli)", "迪士尼 3D 風", "水彩風"])
    if st.button("♻️ 強制重啟系統"):
        st.rerun()

with st.form("story_form"):
    col1, col2, col3 = st.columns(3)
    with col1: character = st.text_input("📝 主角", value="愛冒險的菠蘿包")
    with col2: location = st.selectbox("🗺️ 地點", ["旺角金魚街", "社區客廳", "油麻地果欄"])
    with col3: theme = st.selectbox("💡 道理", ["學會分享", "鄰里互助", "勇氣"])
    submitted = st.form_submit_button("✨ 施展魔法", use_container_width=True)

# ==========================================
# 3. 生成與顯示 (修復藍色問號)
# ==========================================
if submitted:
    if not model:
        st.error("❌ AI 暫時無法連線，請確認你的 API Key 沒過期且 Secrets 設定正確。")
    else:
        with st.spinner("魔法生成中..."):
            try:
                # 寫故事
                prompt = f"你是香港童書作家，請為「{character}」在「{location}」寫一個150字故事。最後一行只寫：IMAGE: A cute illustration of {character} in {location}, {art_style} style"
                res = model.generate_content(prompt)
                full_text = res.text
                
                story = full_text.split("IMAGE:")[0].strip()
                img_desc = full_text.split("IMAGE:")[1].strip() if "IMAGE:" in full_text else f"{character} in {location}"

                # 🌟 解決問號圖：清理所有非英文與空格
                clean_img_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', img_desc)
                encoded_url = urllib.parse.quote(clean_img_prompt)
                
                # 使用最穩定的 Pollinations 網址
                image_url = f"https://image.pollinations.ai/prompt/{encoded_url}?width=1024&height=576&seed={int(time.time())}"

                st.divider()
                c1, c2 = st.columns([1.2, 1])
                with c1:
                    st.image(image_url, use_container_width=True)
                with c2:
                    st.info(story)
                    st.success("✅ 魔法成功了！")
            except Exception as e:
                st.error(f"魔法失敗：{e}")
