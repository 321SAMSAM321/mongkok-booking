import streamlit as st
import urllib.parse
import requests  # 新增：用來在背景下載圖片

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
        # 加上提示，讓使用者知道這次需要等一下
        with st.spinner("🎨 免費 AI 正在為您構圖... (約需 10~20 秒，請耐心等候)"):
            
            # 1. 處理網址編碼
            encoded_prompt = urllib.parse.quote(f"{user_prompt}, {art_style} style")
            width, height = image_size.split('x')
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
            
            try:
                # 2. 讓 Python 去請求網址，並等待伺服器把圖畫完 (設定最多等 60 秒)
                response = requests.get(image_url, timeout=60)
                response.raise_for_status() # 檢查是否有錯誤
                
                # 3. 成功拿到圖片的二進位資料！
                image_bytes = response.content
                
                st.success("✅ 生產完成！")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 這次我們直接給 st.image 真正的「圖片資料」，而不是網址
                    st.image(image_bytes, caption=f"生成結果：{user_prompt}", use_container_width=True)
                
                with col2:
                    st.write("### 🖼️ 作品資訊")
                    st.write(f"- **風格：** {art_style}")
                    st.write(f"- **尺寸：** {image_size}")
                    
                    # 既然我們已經有了圖片資料，可以直接做一個真正的下載按鈕！
                    st.download_button(
                        label="💾 點我下載作品",
                        data=image_bytes,
                        file_name="ai_artwork.png",
                        mime="image/png"
                    )
            
            except Exception as e:
                # 如果超時或伺服器出錯，給予友善提示
                st.error("❌ 抱歉，免費伺服器目前太擁擠或連線超時，請再試一次！")
                st.caption(f"錯誤細節: {e}")
                
    else:
        st.warning("⚠️ 請先輸入靈感描述，工廠才能開工喔！")

# --- 6. 頁尾 ---
st.divider()
st.caption("Powered by Streamlit & Code 編程 | 2024")
