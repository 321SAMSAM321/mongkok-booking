import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# ==========================================
# 1. 系統初始化 (解決之前截圖見到嘅 404 錯誤)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 免費繪本工場", page_icon="🧸", layout="wide")

api_ready = False
try:
    # 讀取 Secrets 入面嘅金鑰
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 2026 年建議使用最新穩定版模型，避免舊型號過期報錯
    model = genai.GenerativeModel('gemini-1.5-flash') 
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 系統金鑰設定有問題：{e}")

# ==========================================
# 2. 介面設計 (維持你原本嘅風格)
# ==========================================
st.title("🧸 旺角社區客廳 - 免費 AI 繪本工場")
st.markdown("小朋友，輸入你嘅想法，AI 會幫你寫故事，仲會**免費**畫埋畫！")

with st.sidebar:
    st.header("🎨 畫畫風格")
    art_style = st.selectbox("選擇你鍾意嘅風格", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "溫馨水彩繪本", "彩色鉛筆塗鴉"])
    st.info("💡 呢個版本完全免費，唔使儲值 OpenAI 密碼。")

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
# 3. 核心邏輯：修復產圖網址 (關鍵部分)
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先設定好 API Key 喔！")
    else:
        with st.spinner("魔法精靈正在創作中... 🧚‍♂️"):
            # 讓 Gemini 生成「乾淨」嘅故事同畫圖指令
            prompt = f"""
            你是一位著名兒童繪本作家。請為「{character}」在「{location}」寫一個約 150 字的短篇童話故事。
            結尾要帶出「{theme}」。請用繁體中文，加少少香港地道用語。
            
            最後請另起一行，只提供一段英文畫圖指令，格式如下：
            IMAGE_DESCRIPTION: A cute illustration of {character} in {location}, {art_style} style, vibrant colors
            """
            
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # 分離故事同指令
                if "IMAGE_DESCRIPTION:" in full_text:
                    story_part = full_text.split("IMAGE_DESCRIPTION:")[0].strip()
                    visual_part = full_text.split("IMAGE_DESCRIPTION:")[1].strip()
                else:
                    story_part = full_text
                    visual_part = f"A cute illustration of {character} in {location}, {art_style}"

                # --- 🎨 視覺自動化修復重點 ---
                # 1. 使用 urllib.parse.quote 確保網址唔會因為空格或符號斷開
                encoded_prompt = urllib.parse.quote(visual_part)
                
                # 2. 使用新版穩定的 Pollinations 接口
                # 加埋 seed={int(time.time())} 係為咗確保次次都有新圖睇
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"

                # 展示成果
                st.markdown("---")
                col_left, col_right = st.columns([1.2, 1])
                
                with col_left:
                    st.subheader("🖼️ 你的專屬插圖")
                    # 使用 st.image 並加上錯誤處理
                    st.image(image_url, use_container_width=True)
                    st.caption(f"故事封面：{character} 在 {location}")
                    st.info("💡 貼士：如果見到問號，請嘗試重新撳一次按鈕。")
                    
                with col_right:
                    st.subheader("📖 你的專屬故事")
                    st.info(story_part)
                    st.success("✅ 創作完成！")
                    
            except Exception as e:
                st.error(f"魔法施展失敗：{e}")
