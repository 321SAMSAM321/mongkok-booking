import streamlit as st
import google.generativeai as genai
import urllib.parse
import time
import re

# ==========================================
# 1. 系統初始化 (解決 Screen 3/4 的 404 報錯)
# ==========================================
st.set_page_config(page_title="旺角 AI 客廳 - 免費繪本工場", page_icon="🧸", layout="wide")

api_ready = False
try:
    # 讀取 Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 使用 gemini-1.5-flash，這是目前最穩定且免費的型號
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except Exception as e:
    st.error(f"⚠️ 系統金鑰設定有問題，請檢查 Secrets 是否已加雙引號。")

# ==========================================
# 2. 介面設計
# ==========================================
st.title("🧸 旺角社區客廳 - 免費 AI 繪本工場")
st.markdown("小朋友，輸入你嘅諗法，AI 會幫你寫故事，仲會**免費**畫埋畫！")

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
# 3. 核心邏輯：修正圖片顯示 (解決 IMG_0303 問號圖)
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先設定好 API Key 喔！")
    else:
        with st.spinner("魔法精靈正在旺角街頭創作中... 🧚‍♂️"):
            # 讓 Gemini 同時生成故事和繪圖描述
            prompt = f"""
            你是一位著名兒童繪本作家。請為「{character}」在「{location}」寫一個約 200 字的短篇童話故事。
            結尾帶出「{theme}」。請用繁體中文，加少少香港地道用語。
            
            最後請另起一行，只提供一段英文畫圖指令，格式如下：
            IMAGE_DESC: A high-quality children's book illustration of {character} in {location}, {art_style} style, vibrant colors.
            """
            
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # 分離故事與指令
                if "IMAGE_DESC:" in full_text:
                    story_part = full_text.split("IMAGE_DESC:")[0].strip()
                    visual_part = full_text.split("IMAGE_DESC:")[1].strip()
                else:
                    story_part = full_text
                    visual_part = f"A cute illustration of {character} in {location}, {art_style} style"

                # --- 🎨 視覺自動化修正重點 ---
                # 1. 清理指令，只保留字母同數字，防止網址斷開
                clean_prompt = re.sub(r'[^a-zA-Z0-9\s,]', '', visual_part)
                encoded_prompt = urllib.parse.quote(clean_prompt)
                
                # 2. 使用官方最穩定的 Pollinations 路徑
                # 加入 seed={int(time.time())} 確保每次生成的圖片都不同
                image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=576&seed={int(time.time())}"

                # 展示成果
                st.markdown("---")
                col_left, col_right = st.columns([1.2, 1])
                
                with col_left:
                    st.subheader("🖼️ 你的專屬插圖")
                    # 使用 st.image 並確保圖片加載
                    st.image(image_url, use_container_width=True)
                    st.caption(f"✨ 角色：{character} | 風格：{art_style}")
                    # 新增：手動刷新按鈕
                    if st.button("🖼️ 換一張圖試試"):
                        st.rerun()
                    
                with col_right:
                    st.subheader("📖 你的專屬故事")
                    st.info(story_part)
                    st.success("✅ 創作完成！")
                    
            except Exception as e:
                st.error(f"魔法施展失敗：{e}")
