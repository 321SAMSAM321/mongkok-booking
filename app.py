import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 系統初始化 (物理級防禦 404 報錯)
# ==========================================
st.set_page_config(page_title="旺角社區客廳 - AI 繪本工場", page_icon="🧸", layout="wide")

# 直接鎖定模型名稱，避免路徑錯誤
MODEL_NAME = 'gemini-1.5-flash'

try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ 請在 Secrets 設定 GEMINI_API_KEY")
        st.stop()
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 連接失敗：{e}")
    api_ready = False

# ==========================================
# 2. 介面設計
# ==========================================
st.title("🎨 旺角社區客廳 - AI 免費繪本工場")
st.markdown("小朋友，只要輸入諗法，AI 會幫你寫故事，仲會畫埋畫！")

with st.sidebar:
    art_style = st.selectbox("🎨 畫畫風格", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "暖心水彩繪本"])
    st.divider()
    st.info("💡 呢個版本專門修復了圖片顯示問題。")

with st.form("story_maker"):
    col1, col2, col3 = st.columns(3)
    with col1: character = st.text_input("📝 主角", value="愛冒險的菠蘿包")
    with col2: location = st.selectbox("🗺️ 地點", ["旺角金魚街", "社區客廳", "油麻地果欄"])
    with col3: theme = st.selectbox("💡 道理", ["鄰里互助", "學會分享", "勇敢面對"])
    submitted = st.form_submit_button("✨ 施展魔法，生成繪本！", use_container_width=True)

# ==========================================
# 3. 核心邏輯 (解決 404 與 藍色問號)
# ==========================================


if submitted and api_ready:
    with st.spinner("魔法精靈正在趕路中... 🧚‍♂️"):
        # 讓 AI 產出故事並分段給出產圖指令
        prompt = f"你是一位兒童書作家，請為「{character}」在「{location}」寫一個 150 字故事，道理是「{theme}」。最後一行只寫：IMAGE_PROMPT: A cute illustration of {character} in {location}, {art_style} style, vibrant colors."
        
        try:
            response = model.generate_content(prompt)
            full_text = response.text
            
            # 拆分故事與指令
            parts = full_text.split("IMAGE_PROMPT:")
            story_text = parts[0].strip()
            # 如果 AI 沒給指令，我們手動補一個
            visual_desc = parts[1].strip() if len(parts) > 1 else f"{character} in {location}, {art_style}"

            # 🌟 解決藍色問號的關鍵：移除所有奇怪標點，只留英文、數字同空格
            clean_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_desc)
            # 強制進行 URL 編碼
            encoded_prompt = urllib.parse.quote(clean_prompt)
            
            # 使用更穩定的 16:9 生成接口，並加隨機種子 (seed)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"

            # 展示
            st.divider()
            col_l, col_r = st.columns([1.3, 1])
            with col_l:
                st.subheader("🖼️ 你的專屬插圖")
                # 使用 st.image 渲染圖片，這是視覺自動化的核心
                st.image(image_url, use_container_width=True)
                st.caption("✨ 小提示：按右鍵「另存圖片」就可以做 YouTube 封面喇！")
            with col_r:
                st.subheader("📖 你的專屬故事")
                st.info(story_text)
                st.success("✅ 魔法成功！")
        except Exception as e:
            st.error(f"魔法失敗了 (404 或連線問題)：{e}")
