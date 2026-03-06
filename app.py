import streamlit as st
import urllib.parse  # 修正：必須匯入這個才能處理中文網址

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 繪畫工廠", page_icon="🎨", layout="wide")

# --- 2. 標題與介紹 ---
st.title("🏭 AI 繪畫自動化生產線")
st.markdown("只要輸入你的靈感，這座工廠就能為你產出精美的藝術作品。")

# --- 3. 側邊欄：工廠控制面板 ---
with st.sidebar:
    st.header("⚙️ 生產參數設定")
    
    art_style = st.selectbox(
        "選擇繪畫風格",
        ["寫實 (Realistic)", "油畫 (Oil Painting)", "賽博龐克 (Cyberpunk)", "吉卜力動漫 (Anime)"]
    )
    
    image_size = st.radio("圖片比例", ["256x256", "512x512", "1024x1024"])
    st.info("提示：目前使用 Pollinations 免費引擎")

# --- 4. 主要輸入區 ---
st.subheader("✍️ 注入靈感 (Prompt)")
user_prompt = st.text_area("請詳細描述你想要生成的畫面：", placeholder="例如：一隻穿著太空衣在火星上喝咖啡的貓...")

# --- 5. 生產邏輯 ---
if st.button("🚀 開始生產圖像"):
    if user_prompt:
        # 使用 spinner 顯示載入中狀態
        with st.spinner("🎨 免費 AI 正在為您構圖..."):
            # 1. 處理網址編碼 (讓中文也能通)
            encoded_prompt = urllib.parse.quote(f"{user_prompt}, {art_style} style")
            
            # 2. 根據選擇的尺寸調整網址 (從介面獲取尺寸)
            width, height = image_size.split('x')
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            # 3. 建立兩欄式佈局來展示結果
            st.success("✅ 生產完成！")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # 顯示真實生成的 AI 圖片
                st.image(image_url, caption=f"生成結果：{user_prompt}", use_container_width=True)
            
            with col2:
                st.write("### 🖼️ 作品資訊")
                st.write(f"- **風格：** {art_style}")
                st.write(f"- **尺寸：** {image_size}")
                
                # 提供一個連結讓使用者直接儲存圖片
                st.markdown(f"[🔗 點我查看原圖]({image_url})")
                st.info("小技巧：右鍵點擊圖片即可「另存圖片」")
                
    else:
        st.warning("⚠️ 請先輸入靈感描述，工廠才能開工喔！")

# --- 6. 頁尾 ---
st.divider()
st.caption("Powered by Streamlit & Code 編程 | 2024")
