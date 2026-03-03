import streamlit as st
import time

# 網頁基本設定 (加上可愛的泰迪熊 Icon)
st.set_page_config(page_title="旺角社區客廳 - 童話創客", page_icon="🧸", layout="centered")

# ==========================================
# 標題與前言
# ==========================================
st.title("🧸 童話社區創客 (繪本生成器)")
st.markdown("小朋友，歡迎來到魔法故事屋！✨\n請選擇你喜歡的角色和地點，AI 魔法精靈會立刻幫你變出一個專屬的香港童話故事喔！這可是我們未來 **YouTube 頻道** 的大作呢！🎬")

st.markdown("---")

# ==========================================
# 互動輸入區 (專為小朋友設計的超大表單)
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
    # 超大顆的魔法按鈕
    submitted = st.form_submit_button("✨ 施展魔法，生成專屬故事！", use_container_width=True)

# ==========================================
# AI 生成結果區 (目前為模擬展示)
# ==========================================
if submitted:
    # 模擬 AI 思考的載入動畫，增加期待感
    with st.spinner("魔法精靈正在旺角街頭為你尋找靈感... 🧚‍♂️✨"):
        time.sleep(2) # 假裝運算 2 秒鐘
        
        st.success("🎉 太棒了！你的專屬繪本故事出爐啦！")
        
        # 1. 故事劇本區 (用來給小朋友配音)
        st.markdown("### 📖 故事大綱 (準備好你的聲音，我們要錄音囉！)")
        
        # 這裡未來會替換成真正的 Gemini API 回應，現在先用變數組合來模擬
        story_text = f"在熱鬧的**{location}**，住著一隻可愛的**{character}**。有一天，社區突然停電了，大家都看不見路，覺得好害怕。**{character}**雖然一開始也嚇了一跳，但牠想起了平時街坊們的照顧，決定挺身而出！\n\n牠利用自己身上發光的小道具，帶領街坊們一步一步安全地回到了社區客廳。大家一起點起蠟燭唱歌，度過了一個溫馨的夜晚。這個故事告訴我們，只要大家**{theme}**，再大的困難都不怕！"
        
        st.info(story_text)
        
        # 2. 插圖指令區 (給前線同事去產圖)
        st.markdown("### 🎨 AI 畫家專用指令 (Prompt)")
        st.markdown("*(同事請將以下英文指令複製到 Midjourney 或 DALL-E 3，就能變出超靚的繪本插圖！)*")
        
        prompt = f"A cute children's book illustration of {character} helping neighbors in {location}, Hong Kong, {art_style} style, warm lighting, vibrant colors, detailed background, heartwarming atmosphere --ar 16:9"
        st.code(prompt)
        
        # 3. 邁向 YouTube 的下一步
        st.markdown("---")
        st.markdown("### 🎙️ 下一步：錄製 YouTube 影片啦！")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🔴 開啟麥克風 (小朋友配音)", use_container_width=True):
                st.toast("未來的進階功能：可以直接在這裡錄下小朋友的聲音喔！", icon="🎤")
                st.balloons()
        with col4:
            if st.button("💾 儲存故事劇本到資料庫", use_container_width=True):
                st.toast("故事已存檔！", icon="✅")
