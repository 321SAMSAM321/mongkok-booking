import streamlit as st
import urllib.parse
import google.generativeai as genai
import time

# ==========================================
# 1. 系統初始化 (確保金鑰安全性)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 繪本工場", page_icon="🧸", layout="wide")

api_ready = False
try:
    # 從 Secrets 讀取金鑰
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 確保使用最新活躍模型，避免 404 錯誤
    model = genai.GenerativeModel('gemini-2.5-flash')
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 系統初始化失敗：{e}。請檢查 Streamlit Secrets 設定。")

# ==========================================
# 2. 介面設計 (小朋友與街坊操作區)
# ==========================================
st.title("🧸 旺角社區客廳 - 免費 AI 繪本工場")
st.markdown("小朋友，只要輸入你嘅大膽諗法，AI 會幫你寫故事，仲會**免費**畫埋畫！ [Image of a tablet showing a colorful AI-generated storybook in a community center]")

# 左側設定
with st.sidebar:
    st.header("🎨 畫畫風格")
    art_style = st.selectbox("選擇你鍾意嘅風格", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "溫馨水彩繪本", "彩色鉛筆塗鴉"])
    st.markdown("---")
    st.info("💡 呢個版本完全免費，唔使儲值 OpenAI 密碼。")

# 主輸入區
with st.form("story_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        character = st.text_input("📝 邊個係主角？", value="愛冒險的菠蘿包")
    with col2:
        location = st.selectbox("🗺️ 喺邊度發生？", ["旺角金魚街", "社區客廳", "油麻地果欄", "花墟", "彌敦道"])
    with col3:
        theme = st.selectbox("💡 想講咩道理？", ["鄰里互助 (互相幫忙)", "勇敢面對困難", "學會分享", "環保愛地球"])
    
    submitted = st.form_submit_button("✨ 施展魔法，生成繪本！", use_container_width=True)

# ==========================================
# 3. 核心邏輯：文字生成 + 視覺自動化
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先設定好 API Key 喔！")
    else:
        with st.spinner("魔法精靈正在旺角街頭創作中... 🧚‍♂️"):
            
            # 讓 Gemini 同時生成「中文故事」同「英文畫圖指令」
            prompt = f"""
            你是一位著名的香港兒童繪本作家。
            請為主角「{character}」在「{location}」寫一個約 150 字的短篇童話故事。
            故事主題：{theme}
            請在故事最後，獨立提供一行英文的插圖描述指令 (Image Prompt)，格式如下：
            [IMAGE_PROMPT: A cute children's book illustration of {character} in {location}, Hong Kong, {art_style} style, vibrant colors, wide angle]
            """
            
            try:
                # 呼叫 Gemini 寫故事
                response = model.generate_content(prompt)
                full_text = response.text
                
                # 分離故事同畫圖指令
                if "[IMAGE_PROMPT:" in full_text:
                    story_text = full_text.split("[IMAGE_PROMPT:")[0].strip()
                    raw_image_prompt = full_text.split("[IMAGE_PROMPT:")[1].split("]")[0].strip()
                else:
                    story_text = full_text
                    raw_image_prompt = f"A cute children's book illustration of {character} in {location} Hong Kong, {art_style}"

                # --- 視覺自動化核心：修復圖片顯示問題 ---
                # 1. 確保指令入面冇奇怪符號，並進行 URL 編碼
                encoded_prompt = urllib.parse.quote(raw_image_prompt)
                
                # 2. 使用最穩定嘅 Pollinations 新版接口
                # 設定 16:9 比例 (1024x576)，方便之後做 YouTube 片
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true&seed={int(time.time())}"

                # --- 展示成果 ---
                st.markdown("---")
                col_left, col_right = st.columns([1.3, 1])
                
                with col_left:
                    st.subheader("🖼️ 你的專屬插圖")
                    # 直接渲染圖片，確保寬度自動適應
                    st.image(image_url, caption=f"故事封面：{character} 在 {location}", use_container_width=True)
                    st.caption("✨ 提示：對圖片按右鍵選擇「另存圖片」就可以下載落嚟做 YouTube 封面喇！")
                    
                with col_right:
                    st.subheader("📖 你的專屬故事")
                    st.info(story_text)
                    st.success("✅ 創作完成！錄埋音就可以擺上 YouTube 喇！")
                    
            except Exception as e:
                st.error(f"魔法施展失敗：{e}")
