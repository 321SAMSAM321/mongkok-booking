import streamlit as st
import time
import google.generativeai as genai

# 網頁基本設定
st.set_page_config(page_title="旺角社區客廳 - 童話創客", page_icon="🧸", layout="centered")

# ==========================================
# 系統初始化與 API 設定
# ==========================================
# 嘗試從 Streamlit Secrets 讀取金鑰
api_ready = False
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 設定使用 Gemini 模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    api_ready = True
except KeyError:
    st.error("⚠️ 系統找不到 API 金鑰。請確認是否已在 Streamlit 的 Settings -> Secrets 中設定 `GEMINI_API_KEY`。")
except Exception as e:
    st.error(f"發生未知的錯誤：{e}")

# ==========================================
# 標題與前言
# ==========================================
st.title("🧸 童話社區創客 (AI 實裝版)")
st.markdown("小朋友，歡迎來到魔法故事屋！✨\n請選擇你喜歡的角色和地點，AI 魔法精靈會立刻幫你變出一個專屬的香港童話故事喔！")
st.markdown("---")

# ==========================================
# 互動輸入區
# ==========================================
with st.form("story_form"):
    st.subheader("🖍️ 第一步：設定你的故事要素")
    col1, col2 = st.columns(2)
    with col1:
        character = st.text_input("📝 故事主角是誰？", value="貪吃的菠蘿包小怪獸")
        location = st.selectbox("🗺️ 故事發生在哪裡？", ["旺角金魚街", "社區客廳", "油麻地果欄", "尖沙咀鐘樓", "彩虹邨"])
    with col2:
        theme = st.selectbox("💡 故事想說什麼道理？", ["鄰里互助 (互相幫忙)", "勇敢面對困難", "學會分享", "保護環境"])
        art_style = st.selectbox("🎨 插圖畫風", ["吉卜力動畫風 (Ghibli)", "迪士尼 3D 風 (Pixar)", "溫馨水彩繪本", "彩色鉛筆塗鴉"])

    st.markdown("---")
    submitted = st.form_submit_button("✨ 施展魔法，生成專屬故事！", use_container_width=True)

# ==========================================
# 呼叫 Gemini API 生成內容
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先完成 API 金鑰設定才能施展魔法喔！")
    else:
        with st.spinner("魔法精靈正在旺角街頭為你尋找靈感... 🧚‍♂️✨ (大約需要 3-5 秒)"):
            
            # 給 AI 的超級指令 (Prompt)
            prompt = f"""
            你現在是一位受歡迎的香港兒童繪本作家。請寫一個約 300 字的短篇童話故事。
            故事主角：{character}
            故事場景：{location} (請加入香港本土特色描述)
            故事主題想帶出的道理：{theme}
            寫作要求：
            1. 故事必須生動有趣、充滿童真，適合 5-10 歲兒童閱讀。
            2. 在結尾溫暖地帶出主題道理。
            3. 使用繁體中文，可以適當加入一點點香港日常用語讓故事更親切。
            """
            
            try:
                # 真正呼叫 Gemini 大腦！
                response = model.generate_content(prompt)
                
                st.success("🎉 太棒了！你的專屬繪本故事出爐啦！")
                
                # 顯示故事
                st.markdown("### 📖 故事大綱 (準備好你的聲音，我們要錄音囉！)")
                st.info(response.text)
                
                # 顯示畫圖指令
                st.markdown("### 🎨 AI 畫家專用指令 (Prompt)")
                st.markdown("*(同事請將以下英文指令複製到 Midjourney 或 DALL-E 3 來產出插圖)*")
                image_prompt = f"A cute children's book illustration of {character} in {location}, Hong Kong, {art_style} style, warm lighting, vibrant colors, detailed background, heartwarming atmosphere --ar 16:9"
                st.code(image_prompt)
                
            except Exception as e:
                st.error(f"魔法施展失敗了！錯誤代碼：{e}")
