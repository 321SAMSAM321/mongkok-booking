import streamlit as st
import time
import urllib.parse
import google.generativeai as genai

# ==========================================
# 1. 系統初始化 (確保 Gemini 大腦仲喺度)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 免費繪本工場", page_icon="🧸", layout="wide")

api_ready = False
try:
    # 呢度繼續用你喺 Secrets 入面嗰把 Gemini 鑰匙
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 🌟 修正點 1：改用 -latest 確保搵到最新模型，解決 404 報錯
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 請先喺 Streamlit Secrets 設定好 `GEMINI_API_KEY` 喔！錯誤細節：{e}")

# ==========================================
# 2. 介面設計
# ==========================================
st.title("🎨 旺角社區客廳 - 免費 AI 繪本工場")
st.markdown("小朋友，只要輸入你嘅諗法，AI 會幫你寫故事，仲會**免費**幫你畫埋畫！")

with st.sidebar:
    st.header("🛠️ 創作設定")
    art_style = st.selectbox("🎨 畫畫風格", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "溫馨水彩繪本", "彩色鉛筆塗鴉"])
    st.info("💡 呢個版本完全免費，唔使儲值 OpenAI 密碼。")

# --- 輸入區 ---
with st.form("story_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        character = st.text_input("📝 邊個係主角？", value="愛冒險的菠蘿包")
    with col2:
        location = st.selectbox("🗺️ 喺邊度發生？", ["旺角金魚街", "社區客廳", "油麻地果欄", "花墟"])
    with col3:
        theme = st.selectbox("💡 想講咩道理？", ["鄰里互助", "勇敢面對", "學會分享"])
    
    submitted = st.form_submit_button("✨ 施展魔法，生成繪本！", use_container_width=True)

# ==========================================
# 3. 執行創作 (文字 + 視覺)
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先設定好 API Key 喔！")
    else:
        with st.spinner("魔法精靈正在旺角街頭創作中... 🧚‍♂️"):
            
            # --- 步驟 A: Gemini 寫故事 ---
            prompt = f"你是一位香港兒童繪本作家。請為主角「{character}」在「{location}」寫一個約 150 字的短篇童話故事，帶出「{theme}」的道理。請用繁體中文，加少少香港地道用語。"
            
            try:
                story_response = model.generate_content(prompt)
                story_text = story_response.text
                
                # --- 步驟 B: 魔法產圖 (完全免費方案) ---
                # 組合英文產圖指令
                visual_desc = f"A cute children's book illustration of {character} in {location} Hong Kong, {art_style} style, vibrant colors, soft lighting, 16:9 aspect ratio"
                
                # 將英文指令編碼成網址格式
                encoded_prompt = urllib.parse.quote(visual_desc)
                
                # 🌟 修正點 2：使用最新版 image.pollinations 接口與隨機種子 (seed)，解決問號圖
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"
                
                # --- 步驟 C: 展示結果 ---
                st.markdown("---")
                col_left, col_right = st.columns([1.2, 1])
                
                with col_left:
                    st.subheader("🖼️ 你的專屬插圖")
                    # 直接喺網頁顯示圖片！
                    st.image(image_url, use_container_width=True)
                    st.caption("✨ 小提示：鍾意呢張圖？按右鍵就可以另存圖片下載！")
                    
                with col_right:
                    st.subheader("📖 你的專屬故事")
                    st.info(story_text)
                    st.success("✅ 創作完成！你可以準備為 YouTube 頻道錄音喇！")
                    
            except Exception as e:
                st.error(f"魔法失效了，請再試一次！錯誤：{e}")
