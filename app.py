import streamlit as st

def generate_comprehensive_report(housing_type, prh_waiting_years, monthly_income, has_children, children_level, working_hours, age):
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    
    # 🏠 房屋與生活安全網
    st.write("### 🏠 房屋與生活支援")
    if housing_type == "劏房/板間房" and prh_waiting_years >= 3:
        st.write("✅ **現金津貼試行計劃：** 您輪候公屋已過3年，極可能符合資格領取每月現金租金津貼。")
    if working_hours >= 144: # 假設非單親一般家庭基本工時
        st.write("✅ **在職家庭津貼 (WFA)：** 您的工時達標，建議申請以獲取入息補貼，減輕生活負擔。")
        
    # 📚 教育與功課支援 (針對跨代貧窮)
    if has_children == "係":
        st.write("### 📚 仔女教育與功課支援")
        st.write("✅ **學生資助計劃：** 記得為仔女申請書簿、車船及上網費津貼 (全津/半津)。")
        st.write("✅ **社區客廳功輔班：** 劏房環境狹窄，歡迎即時預約我哋客廳嘅「AI 智多星」功輔班及大專生一對一指導。")
        
        if children_level == "初中 (中一至中三)":
            st.write("✅ **共創明「Teen」計劃：** 您的仔女符合年齡，建議報名獲取專屬友師指導及高達 $10,000 財政支援。")

    # 🩺 醫療與長者福利
    if age >= 65:
        st.write("### 🩺 長者專屬福利")
        st.write("✅ **關愛基金長者牙科：** 您可申請免費鑲活動假牙及其他牙科診療。")
        
    st.markdown('</div>', unsafe_allow_html=True)

# 介面輸入範例 (加入 Streamlit UI 中)
st.subheader("進階家庭狀況評估")
col1, col2 = st.columns(2)
with col1:
    prh_waiting_years = st.number_input("輪候公屋年期 (年)", min_value=0, step=1)
    has_children = st.radio("家中有沒有在學學童？", ["係", "唔係"])
with col2:
    working_hours = st.number_input("家庭每月總工作時數", min_value=0, step=10)
    if has_children == "係":
        children_level = st.selectbox("學童就讀年級", ["幼稚園", "小學", "初中 (中一至中三)", "高中"])
    else:
        children_level = "無"

if st.button("生成全面福利報告"):
    # 假設 housing_type, monthly_income, age 已在其他欄位獲取
    # 這裡直接呼叫函數 (需結合你之前的代碼)
    generate_comprehensive_report("劏房/板間房", prh_waiting_years, 15000, has_children, children_level, working_hours, 45)
