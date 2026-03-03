import streamlit as st
import time

st.set_page_config(page_title="旺角社區客廳 - AI 創意發動機", page_icon="🎨", layout="wide")

# ==========================================
# 左側選單
# ==========================================
st.sidebar.title("🎨 創意發動機")
app_mode = st.sidebar.radio("選擇創作工具：", ["📖 兒童繪本工場 (YouTube 素材)", "🚀 開幕宣傳與主題曲引擎"])
st.sidebar.markdown("---")
st.sidebar.info("💡 提示：此系統協助前線同事快速生成故事草稿、海報文案及 AI 生成工具的專屬指令 (Prompts)。")

# ==========================================
# 工具一：兒童繪本工場
# ==========================================
if app_mode == "📖 兒童繪本工場 (YouTube 素材)":
    st.title("📖 AI 兒童繪本工場")
    st.markdown("讓小朋友輸入幾個簡單的詞彙，快速生成充滿本土特色的故事與插圖指令！")
    
    with st.form("storybook_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            character = st.text_input("主角是誰？", value="一隻戴著黑框眼鏡的唐狗")
        with col2:
            location = st.selectbox("故事地點", ["旺角金魚街", "社區客廳", "彌敦道", "花墟", "油麻地果欄"])
        with col3:
            moral = st.selectbox("想帶出的道理", ["分享的快樂", "勇敢面對困難", "環保愛地球", "尊重長者"])
            
        submitted = st.form_submit_button("✨ 讓 AI 寫故事！", use_container_width=True)
        
        if submitted:
            with st.spinner("AI 正在旺角街頭尋找靈感..."):
                time.sleep(1.5) # 模擬運算時間
                
                st.success("🎉 故事大綱與畫面指令生成完畢！")
                
                st.markdown("### 📝 故事大綱 (可直接用於 YouTube 配音)")
                st.write(f"在熱鬧的**{location}**，住著**{character}**。有一天，社區客廳舉辦了一場大食會，但突然停電了！大家都好驚慌。{character} 利用自己靈敏的嗅覺，在黑暗中找出了備用電筒，還把自己的零食分給了害怕的小朋友。最後燈亮了，大家都明白到**{moral}**的重要性。")
                
                st.markdown("### 🎨 圖片生成指令 (直接複製到 Midjourney / 圖像生成 AI)")
                st.code(f"A cute cartoon style illustration of {character} in {location} Hong Kong, colorful, warm lighting, Ghibli style, detailed background, happy atmosphere --ar 16:9")

# ==========================================
# 工具二：開幕宣傳與主題曲引擎
# ==========================================
elif app_mode == "🚀 開幕宣傳與主題曲引擎":
    st.title("🚀 開幕宣傳與主題曲引擎")
    st.markdown("輸入活動核心理念，一秒產出精準的 Facebook 宣傳文案，以及用來生成主題曲的音樂設定檔！")
    
    # 預設帶入精準的專業字眼，確保同事產出的文案不會有錯字
    default_promo_text = """宣傳重點：
1. 旺角全新 AI 主題社區客廳正式開幕。
2. 中電撥款 5,000 萬港元延續電費補助計劃，合資格街坊可現場登記。
3. 辦理手續請務必攜帶申請人身份證正本。"""

    promo_info = st.text_area("✍️ 輸入活動資訊與細節：", value=default_promo_text, height=120)
    
    music_vibe = st.selectbox("🎵 期望的主題曲氛圍", ["溫馨感人 (適合大合唱)", "充滿活力 (適合開幕剪綵)", "輕鬆愉快 (適合背景音樂)"])
    
    if st.button("✨ 生成宣傳海報文案與音樂指令", type="primary", use_container_width=True):
        with st.spinner("AI 正在撰寫文案與編曲提示..."):
            time.sleep(1.5)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("### 📱 Facebook / 海報宣傳文案")
                st.info("""🎉 **【旺角全新地標】AI 主題社區客廳盛大開幕！** 🎉\n\n各位街坊，準備好迎接充滿科技感的新空間了嗎？我們誠邀您參與開幕日！\n\n⚡ **特別放送：中電電費補助計劃**\n好消息！中電撥款 5,000 萬港元延續電費補助計劃。合資格的街坊，開幕當天可以直接在現場辦理登記！\n\n📌 **溫馨提示：** 請務必攜帶 **「申請人身份證」** 正本，以加快處理流程喔！\n\n期待與您在全新的社區客廳相見！""")
                
            with col_b:
                st.markdown("### 🎼 主題曲生成指令 (音樂 AI 專用)")
                st.write("將以下設定複製到音樂生成工具 (如 Lyria 或 Suno) 中：")
                
                if music_vibe == "充滿活力 (適合開幕剪綵)":
                    st.code("Tempo: Upbeat and energetic (120 BPM)\nGenre: Cantopop / Modern Pop\nEmotional Mood: Hopeful, exciting, welcoming\nInstruments: Acoustic guitar, bright piano, light electronic beats\nLyrics theme: New beginnings, community support, technology bringing people together in Mong Kok.")
                elif music_vibe == "溫馨感人 (適合大合唱)":
                    st.code("Tempo: Slow and touching (70 BPM)\nGenre: Acoustic Cantopop ballad\nEmotional Mood: Warm, empathetic, united\nInstruments: Grand piano, soft strings, acoustic guitar\nLyrics theme: Helping hands, a safe harbor, neighborly love in Hong Kong.")
                else:
                    st.code("Tempo: Mid-tempo and breezy (90 BPM)\nGenre: Lo-Fi / Acoustic Indie\nEmotional Mood: Relaxing, cheerful, comfortable\nInstruments: Ukulele, soft percussion, gentle bass\nLyrics theme: A living room for everyone, relaxing afternoon, sharing smiles.")
