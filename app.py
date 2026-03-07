import streamlit as st

st.title("👾 我的虛擬小怪獸")

# 初始化寵物狀態
if 'hunger' not in st.session_state:
    st.session_state.hunger = 50
if 'happiness' not in st.session_state:
    st.session_state.happiness = 50

# 顯示寵物狀態與表情
if st.session_state.hunger <= 20:
    mood = "😫 (好餓喔...)"
elif st.session_state.happiness >= 80:
    mood = "🤩 (超級開心！)"
else:
    mood = "😊 (感覺不錯)"

st.header(f"小怪獸目前心情：{mood}")

# 顯示狀態條
st.write("飽食度")
st.progress(st.session_state.hunger / 100)
st.write("開心值")
st.progress(st.session_state.happiness / 100)

# 互動按鈕
col1, col2 = st.columns(2)
with col1:
    if st.button("🍖 餵牠吃肉肉"):
        st.session_state.hunger = min(100, st.session_state.hunger + 10)
        st.toast("好吃！飽飽的！") # 小小的彈出提示

with col2:
    if st.button("🧸 陪牠玩遊戲"):
        st.session_state.happiness = min(100, st.session_state.happiness + 15)
        st.session_state.hunger = max(0, st.session_state.hunger - 5)
        st.balloons() # 玩得開心就噴氣球！
