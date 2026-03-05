import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 系統初始化 (解決 IMG_0306 的 404 報錯)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 免費繪本工場", page_icon="🧸", layout="wide")

api_ready = False
try:
    # 確保你喺 Secrets 已經入咗 GEMINI_API_KEY
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用目前最穩定嘅 1.5 系列模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    st.error("⚠️ 系統金鑰設定失敗。請檢查 Streamlit Secrets 是否已加上雙引號。")

# ==========================================
# 2. 介面設計
# ==========================================
st.title("🧸 旺角社區客廳 - 免費 AI 繪本工場")
st.markdown("小朋友，輸入你嘅諗法，AI 會幫你寫故事，仲會**免費**畫埋畫！")

with st.sidebar:
    st.header("🎨 畫畫風格")
    art_style = st.selectbox("選擇你鍾意嘅風格", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "溫馨水彩繪本", "彩色鉛筆塗鴉"])
    st.info("💡 呢個版本完全免費，唔使儲值密碼。")

with st.form("story_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        character = st.text_input("📝 邊個係主角？", value="愛冒險的菠蘿包")
    with col2:
        location = st.selectbox("🗺️ 喺邊度發生？", ["油麻地果欄", "旺角金魚街", "社區客廳", "花墟"])
    with col3:
        theme = st.selectbox("💡 想講咩道理？", ["學會分享", "鄰里互助", "勇敢面對", "愛護環境"])
    
    submitted = st.form_submit_button("✨ 施展魔法，生成繪本！", use_container_width=True)

# ==========================================
# 3. 核心邏輯：修正圖片顯示 (解決 IMG_0303 藍色問號)
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先設定好 API Key 喔！")
    else:
        with st.spinner("魔法精靈正在創作中... 🧚‍♂️"):
            # 讓 Gemini 生成故事同「乾淨」嘅英文畫圖描述
            prompt = f"""
            你是一位著名兒童繪本作家。請為主角「{character}」在「{location}」寫一個約 150 字的短篇童話故事。
            結尾要帶出「{theme}」。請用繁體中文，可以加地道用語。
            
            最後請另起一行，只提供一段英文畫圖描述，格式如下：
            IMAGE_DESCRIPTION: A cute illustration of {character} in {location}, {art_style} style, vibrant colors
            """
            
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # 分離故事同畫圖指令
                if "IMAGE_DESCRIPTION:" in full_text:
                    story_part = full_text.split("IMAGE_DESCRIPTION:")[0].strip()
                    visual_part = full_text.split("IMAGE_DESCRIPTION:")[1].strip()
                else:
                    story_part = full_text
                    visual_part = f"A cute illustration of {character} in {location}, {art_style}"

                # --- 🎨 視覺自動化修復重點 ---
                # 1. 清理指令，只保留字母、數字同空格，防止網址因為奇怪符號而斷開
                clean_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_part)
                # 2. 進行 URL 編碼
                encoded_prompt = urllib.parse.quote(clean_prompt)
                
                # 3. 使用最新穩定嘅 Pollinations 接口
                # 加入 seed 確保每次撳掣都有新圖，比例設定為 16:9 方便做片
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"

                # 展示成果
                st.markdown("---")
                col_left, col_right = st.columns([1.2, 1])
                
                with col_left:
                    st.subheader("🖼️ 你的專屬插圖")
                    # 顯示圖片，並確保寬度自動適應
                    st.image(image_url, use_container_width=True)
                    st.caption(f"✨ 角色：{character} | 場景：{location}")
                    
                with col_right:
                    st.subheader("📖 你的專屬故事")
                    st.info(story_part)
                    st.success("✅ 創作完成！圖片按右鍵即可儲存。")
                    
            except Exception as e:
                st.error(f"魔法施展失敗：{e}")
