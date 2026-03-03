import streamlit as st
import pandas as pd
from datetime import date, timedelta

# 網頁基本設定
st.set_page_config(page_title="旺角社區客廳 - 預約系統", page_icon="🏠", layout="centered")

# ==========================================
# 1. 系統初始化 (建立虛擬資料庫)
# ==========================================
# 在真實環境中，這裡會連接 Google Sheets 或資料庫。
# 這裡我們先用 st.session_state 建立一個暫存的預約紀錄表。
if 'bookings' not in st.session_state:
    st.session_state.bookings = pd.DataFrame(columns=['預約日期', '設施名稱', '預約時段', '街坊姓名', '會員編號', '登記時間'])

# 設施與時段設定
FACILITIES = ["洗衣機 A", "洗衣機 B", "共享廚房 (煮食爐)", "淋浴間 A", "淋浴間 B", "縫紉機"]
TIME_SLOTS = [
    "11:00 - 12:00", "12:00 - 13:00", "13:00 - 14:00", 
    "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00",
    "17:00 - 18:00", "18:00 - 19:00", "19:00 - 20:00"
]

# ==========================================
# 2. 左側邊欄：導覽選單
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2590/2590204.png", width=100) # 放一個可愛的預約Icon
st.sidebar.title("🏠 旺角社區客廳")
app_mode = st.sidebar.radio("請選擇服務：", ["📅 預約設施 (街坊專用)", "📋 查看今日時間表", "🔒 管理員後台"])

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：此為獨立的預約系統。如需排班，請前往 [智能排更系統](https://你的排更系統網址.streamlit.app)")

# ==========================================
# 頁面一：預約設施 (街坊專用)
# ==========================================
if app_mode == "📅 預約設施 (街坊專用)":
    st.title("📅 預約中心設施")
    st.markdown("歡迎使用自助預約系統！請選擇您需要的設施與時間。可預約今天起計 **7天內** 的時段。")
    
    # 預約表單
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            # 限制只能預約未來 7 天
            selected_date = st.date_input("1️⃣ 選擇日期", min_value=date.today(), max_value=date.today() + timedelta(days=7))
        with col2:
            selected_facility = st.selectbox("2️⃣ 選擇設施", FACILITIES)
            
        selected_slot = st.selectbox("3️⃣ 選擇時段", TIME_SLOTS)
        
        st.markdown("---")
        st.markdown("📝 **登記資料**")
        col3, col4 = st.columns(2)
        with col3:
            user_name = st.text_input("街坊姓名 (例如：陳大文)")
        with col4:
            user_id = st.text_input("會員編號 / 聯絡電話末4碼")
            
        submitted = st.form_submit_button("✅ 確認預約", use_container_width=True)
        
        if submitted:
            if not user_name or not user_id:
                st.error("⚠️ 請填寫姓名及會員編號！")
            else:
                # 檢查是否「撞期」 (這個設施在這個時段有沒有人約了)
                conflict = st.session_state.bookings[
                    (st.session_state.bookings['預約日期'] == str(selected_date)) & 
                    (st.session_state.bookings['設施名稱'] == selected_facility) & 
                    (st.session_state.bookings['預約時段'] == selected_slot)
                ]
                
                if not conflict.empty:
                    st.error(f"❌ 抱歉，【{selected_facility}】在 {selected_slot} 已經被預約了，請選擇其他時段！")
                else:
                    # 新增預約紀錄
                    new_booking = pd.DataFrame([{
                        '預約日期': str(selected_date),
                        '設施名稱': selected_facility,
                        '預約時段': selected_slot,
                        '街坊姓名': user_name,
                        '會員編號': user_id,
                        '登記時間': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    st.session_state.bookings = pd.concat([st.session_state.bookings, new_booking], ignore_index=True)
                    st.success(f"🎉 預約成功！{user_name}，您已成功預約 {str(selected_date)} 的 {selected_facility} ({selected_slot})。請準時到達！")
                    st.balloons()

# ==========================================
# 頁面二：查看今日時間表
# ==========================================
elif app_mode == "📋 查看今日時間表":
    st.title("📋 設施使用時間表")
    st.markdown("街坊可以在這裡查看哪部機有空，避免白走一趟！")
    
    view_date = st.date_input("選擇日期查詢", date.today())
    
    # 過濾出選擇日期的預約
    daily_bookings = st.session_state.bookings[st.session_state.bookings['預約日期'] == str(view_date)]
    
    if daily_bookings.empty:
        st.info("✨ 這天目前還沒有任何預約，所有設施都空著喔！")
    else:
        # 將資料表整理成容易閱讀的格式
        display_df = daily_bookings[['設施名稱', '預約時段', '街坊姓名']].sort_values(by=['設施名稱', '預約時段'])
        # 為了保護私隱，把名字隱藏一部分 (例如：陳大文 -> 陳*文)
        display_df['街坊姓名'] = display_df['街坊姓名'].apply(lambda x: x[0] + "*" * (len(x)-2) + x[-1] if len(x)>2 else x[0] + "*")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ==========================================
# 頁面三：管理員後台 (前線同事專用)
# ==========================================
elif app_mode == "🔒 管理員後台":
    st.title("🔒 管理員後台")
    st.markdown("前線同事可以在此查看完整預約名單、取消違規預約，以及匯出報表。")
    
    # 簡單的密碼保護
    password = st.text_input("請輸入管理員密碼 (測試密碼: 1234)", type="password")
    
    if password == "1234":
        st.success("✅ 登入成功！")
        
        if st.session_state.bookings.empty:
            st.info("目前系統尚無任何預約紀錄。")
        else:
            # 讓管理員可以編輯或刪除預約
            st.markdown("### 📝 完整預約紀錄 (可直接修改或刪除)")
            edited_bookings = st.data_editor(st.session_state.bookings, num_rows="dynamic", use_container_width=True)
            
            # 儲存修改按鈕
            if st.button("💾 儲存修改"):
                st.session_state.bookings = edited_bookings
                st.success("紀錄已更新！")
                
            # 下載報表功能
            st.markdown("### 📥 匯出統計報表")
            csv = st.session_state.bookings.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="下載完整預約紀錄 (CSV)",
                data=csv,
                file_name=f"旺角社區客廳_預約紀錄_{date.today()}.csv",
                mime="text/csv",
            )
    elif password != "":
        st.error("❌ 密碼錯誤！")
