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
    model = genai.GenerativeModel('gemini-2.5-flash')
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
# 呼叫 Gemini 寫故事 ＆ 免費 API 生成插圖
# ==========================================
if submitted:
    if not api_ready:
        st.warning("請先完成 Gemini API 金鑰設定才能施展魔法喔！")
    else:
        with st.spinner("魔法精靈正在旺角街頭為你尋找靈感... 🧚‍♂️✨"):
            
            # 1. 讓 Gemini 寫出本土故事，並特別要求它給出一句「英文畫圖指令」
            prompt = f"""
            你是一位香港兒童繪本作家。請寫一個約 150 字的短篇童話故事。
            故事主角：{character}
            故事場景：{location}
            故事主題：{theme}
            
            請在故事最後，獨立提供一行英文的插圖描述指令 (Image Prompt)，格式如下：
            [Image Prompt: A cute children's book illustration of {character} in {location}, Hong Kong, {art_style} style, vibrant colors]
            """
            
            try:
                # 呼叫 Gemini 大腦
                response = model.generate_content(prompt)
                full_response = response.text
                
                # 簡單地將「中文故事」與「英文畫圖指令」分開
                if "[Image Prompt:" in full_response:
                    story_text = full_response.split("[Image Prompt:")[0].strip()
                    # 擷取出英文指令並清理多餘符號
                    image_prompt = full_response.split("[Image Prompt:")[1].replace("]", "").strip()
                else:
                    story_text = full_response
                    # 萬一 AI 忘記給，我們自己組合一個備用的
                    image_prompt = f"A cute illustration of {character} in {location}, Hong Kong, {art_style}"

                # 2. 啟動視覺自動化：將英文指令轉換為圖片網址 (完全免費免金鑰)
                # 將指令進行 URL 編碼，避免空白或特殊符號造成錯誤
                encoded_prompt = urllib.parse.quote(image_prompt)
                # 使用寬高比 16:9 (width=1024&height=576) 適合 YouTube 影片格式
                image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=576&nologo=true"

                # 3. 成果華麗展示
                st.success("🎉 太棒了！你的專屬繪本出爐啦！")
                
                # 將畫面分為左右兩邊：左邊看大圖，右邊讀故事
                col_img, col_text = st.columns([1.2, 1])
                
                with col_img:
                    st.markdown("### 🖼️ 你的專屬插圖")
                    # 直接在網頁上渲染這張圖片！
                    st.image(image_url, use_container_width=True)
                    st.caption("✨ 提示：對圖片按右鍵即可「另存圖片」下載喔！")
                    
                with col_text:
                    st.markdown("### 📖 故事大綱")
                    st.info(story_text)
                    
            except Exception as e:
                st.error(f"魔法施展失敗了！錯誤代碼：{e}")
