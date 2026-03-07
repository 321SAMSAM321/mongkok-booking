import streamlit as st
import requests
import io

# --- 1. 頁面設定 ---
st.set_page_config(page_title="AI 繪畫工廠", page_icon="🎨", layout="wide")

# --- 2. 標題與介紹 ---
st.title("🏭 AI 繪畫自動化生產線 (Stable Diffusion 版)")
st.markdown("只要輸入你的靈感，這座工廠就能為你產出精美的藝術作品。")

# --- 3. 側邊欄：工廠控制面板 ---
with st.sidebar:
    st.header("⚙️ 生產參數設定")
    art_style = st.selectbox(
        "選擇繪畫風格",
        ["寫實 (Realistic)", "油畫 (Oil Painting)", "賽博龐克 (Cyberpunk)", "吉卜力動漫 (Anime)"]
    )
    st.info("💡 提示：目前已升級為 Hugging Face 穩定版引擎")

# --- 4. 主要輸入區 ---
st.subheader("✍️ 注入靈感 (Prompt)")
user_prompt = st.text_area("請詳細描述你想要生成的畫面 (建議使用英文效果更好)：", placeholder="例如：A cat astronaut drinking coffee on Mars...")

# --- 5. 生產邏輯 ---
# 設定 Hugging Face API 資訊
API_URL = "https://api-inference.huggingface.co/models/stabilityai/sdxl-turbo"

# 安全地讀取我們剛才設定的金鑰
try:
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
except FileNotFoundError:
    st.error("❌ 找不到 API 金鑰！請確認您已經在 Streamlit Secrets 中設定了 HF_TOKEN。")
    st.stop()

if st.button("🚀 開始生產圖像"):
    if user_prompt:
        with st.spinner("🎨 高階 AI 正在努力渲染中... (約需 10-30 秒)"):
            
            # 組合 Prompt，把風格加進去
            final_prompt = f"{user_prompt}, {art_style} style, high quality, highly detailed"
            
            try:
                # 呼叫 Hugging Face API
                response = requests.post(API_URL, headers=headers, json={"inputs": final_prompt}, timeout=60)
                
                # 如果伺服器回傳錯誤，會拋出例外
                response.raise_for_status()
                
                # 取得圖片的二進位資料
                image_bytes = response.content
                
                st.success("✅ 生產完成！")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 顯示生成的圖片
                    st.image(image_bytes, caption=f"生成結果：{user_prompt}", use_container_width=True)
                
                with col2:
                    st.write("### 🖼️ 作品資訊")
                    st.write(f"- **風格：** {art_style}")
                    st.write("- **模型：** Stable Diffusion XL")
                    
                    st.download_button(
                        label="💾 點我下載作品",
                        data=image_bytes,
                        file_name="hf_artwork.png",
                        mime="image/png"
                    )
                    
            except requests.exceptions.HTTPError as err:
                st.error("❌ 模型正在載入中或發生錯誤，請稍等 30 秒後再試一次！")
                st.caption(f"伺服器回應: {err}")
            except Exception as e:
                st.error("❌ 發生未知錯誤！")
                st.caption(f"錯誤細節: {e}")
                
    else:
        st.warning("⚠️ 請先輸入靈感描述，工廠才能開工喔！")

# --- 6. 頁尾 ---
st.divider()
st.caption("Powered by Streamlit & Code 編程 | 2024")
