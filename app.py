import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 系統初始化 (修正模型連接與 404 報錯)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 繪本工場", page_icon="🧸", layout="wide")

# 檢查保險箱金鑰
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 請先在 Streamlit Secrets 設定 GEMINI_API_KEY (記得加雙引號)")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 鎖定 2026 年最穩定且免費的 Flash 模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 大腦連接失敗：{e}")
    api_ready = False

# ==========================================
# 2. 介面設計 (小朋友友善介面)
# ==========================================
st.title("🎨 旺角社區客廳 - AI 免費繪本工場")
st.markdown("小朋友，輸入你的創意，AI 會立刻為你寫故事並畫出精美插圖！")

# 左側側邊欄：風格設定
with st.sidebar:
    st.header("🎨 視覺風格設定")
    art_style = st.selectbox(
        "選擇插圖畫風", 
        ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "暖心水彩繪本", "彩色鉛筆塗鴉"]
    )
    st.divider()
    st.info("💡 此版本完全免費，不需儲值 OpenAI 帳戶。")

# 主畫面：故事要素輸入
with st.form("story_maker"):
    col1, col2, col3 = st.columns(3)
    with col1:
        character = st.text_input("📝 主角是誰？", value="愛冒險的菠蘿包")
    with col2:
        location = st.selectbox("🗺️ 發生在哪裡？", ["旺角金魚街", "油麻地果欄", "社區客廳", "花墟"])
    with col3:
        theme = st.selectbox("💡 想講什麼道理？", ["鄰里互助", "勇敢面對", "學會分享", "愛護環境"])
    
    submitted = st.form_submit_button("✨ 施展魔法，生成專屬繪本！", use_container_width=True)

# ==========================================
# 3. 核心魔法邏輯 (解決圖片問號問題)
# ==========================================


if submitted and api_ready:
    with st.spinner("✨ 魔法精靈正在構思故事並繪製插圖..."):
        
        # --- 步驟 A: 讓 Gemini 寫故事並產出畫圖指令 ---
        prompt = f"""
        你是一位受歡迎的香港兒童繪本作家。
        請為主角「{character}」在「{location}」寫一個約 200 字的短篇童話故事，主題是「{theme}」。
        請使用繁體中文，語氣溫暖，並加入一點香港地道生活感。
        
        最後，請另起一行，只提供一段用於產圖的英文指令，格式如下：
        IMAGE_PROMPT: A high-quality children's book illustration of {character} in {location}, {art_style} style, vibrant colors, heartwarming atmosphere.
        """
        
        try:
            response = model.generate_content(prompt)
            full_text = response.text
            
            # 拆分文字與指令
            if "IMAGE_PROMPT:" in full_text:
                story_content = full_text.split("IMAGE_PROMPT:")[0].strip()
                raw_visual_prompt = full_text.split("IMAGE_PROMPT:")[1].strip()
            else:
                story_content = full_text
                raw_visual_prompt = f"A cute illustration of {character} in {location}, {art_style}"

            # --- 步驟 B: 視覺自動化 (修正編碼，防止藍色問號) ---
            # 1. 移除非英文字元，確保網址乾淨
            clean_visual_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', raw_visual_prompt)
            # 2. 進行 URL 安全編碼
            encoded_prompt = urllib.parse.quote(clean_visual_prompt)
            # 3. 生成 16:9 高清插圖網址 (適合做 YouTube)
            # 加入隨機種子 (seed) 確保每次產圖都有驚喜
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={int(time.time())}"

            # --- 步驟 C: 華麗成果展示 ---
            st.divider()
            col_l, col_r = st.columns([1.3, 1])
            
            with col_l:
                st.subheader("🖼️ 你的專屬插圖")
                # 直接渲染生成出的圖片
                st.image(image_url, caption=f"故事封面：{character} 在 {location}", use_container_width=True)
                st.caption("✨ 小提示：按右鍵選擇「另存圖片」即可下載做 YouTube 封面！")
                
            with col_r:
                st.subheader("📖 你的專屬故事")
                st.info(story_content)
                st.success("🎉 創作完成！快讀給小朋友聽吧！")

        except Exception as e:
            st.error(f"魔法失效了！錯誤原因：{e}")
