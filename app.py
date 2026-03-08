import streamlit as st

st.set_page_config(page_title="旺角社區客廳：資源導航系統", page_icon="🏢")

# 自定義 CSS 優化視覺
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2E7D32; color: white; }
    .status-box { padding: 20px; border-radius: 10px; background-color: #E8F5E9; border-left: 5px solid #2E7D32; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ 旺角基層資源導航系統")
st.caption("專業社工視角：精準匹配資源，緩解生活壓力")

# 使用 Tabs 分頁
tab1, tab2, tab3 = st.tabs(["🏠 居住與基本資料", "🩺 健康與家庭", "💰 資源叮一叮"])

with tab1:
    st.header("第一步：了解您的居住環境")
    district = st.selectbox("居住區域", ["旺角/大角咀", "油麻地", "尖沙咀", "其他"])
    housing_type = st.radio("居住類型", ["劏房/板間房", "公共屋邨", "私人樓宇", "無固定居所"])
    monthly_income = st.number_input("家庭每月總入息 (HKD)", min_value=0, step=500)
    
with tab2:
    st.header("第二步：您的身心健康")
    age = st.slider("您的年齡", 0, 100, 45)
    stress_level = st.select_slider("自覺生活壓力指數", options=["輕微", "適中", "沉重", "爆煲"])
    health_needs = st.multiselect("目前最需要的支援 (多選)", ["免費洗衫乾衣", "共享廚房煮食", "功課輔導", "身體檢查", "法律諮詢"])

with tab3:
    if st.button("生成專業建議報告"):
        st.success("計算完成！請查看以下建議：")
        
        # 深度邏輯判斷
        with st.container():
            st.markdown('<div class="status-box">', unsafe_allow_html=True)
            
            # 1. 社區客廳
            if housing_type == "劏房/板間房" and monthly_income <= 20000: # 假設限額
                st.write("### 📍 社區客廳優先會員")
                st.write("- 您符合資格享受**免費淋浴、平價洗衣及共享客廳**服務。")
            
            # 2. 電費補貼
            if housing_type == "劏房/板間房":
                st.write("### ⚡ 電力補貼預警")
                st.write("- **建議申請：** 中電「基層家庭電費補助」，可獲 **$1,000**。")
            
            # 3. 醫療券
            if age >= 65:
                st.write("### 🩺 長者專屬優惠")
                st.write("- 記得領取年度 **$500** 醫療券獎賞。")
            
            # 4. 健康風險
            st.write("### 🍎 健康管理建議")
            st.write("- 請前往**油尖旺地區康健中心**進行免費篩查。")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("💡 下一步：請截圖並預約諮詢站社工面見，我們將協助您正式遞交申請。")
