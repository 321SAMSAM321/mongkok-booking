import streamlit as st

st.title("🌈 魔法調色實驗室")

# 滑桿互動
r = st.slider("紅色 (Red)", 0, 255, 125)
g = st.slider("綠色 (Green)", 0, 255, 125)
b = st.slider("藍色 (Blue)", 0, 255, 125)

# 將 RGB 轉為十六進位顏色
hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

# 使用 Markdown 與 HTML 顯示大大的顏色區塊
st.markdown(
    f"""
    <div style="
        width: 100%;
        height: 200px;
        background-color: {hex_color};
        border-radius: 20px;
        border: 5px solid #333;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 30px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000;
    ">
        這就是你的專屬顏色！
    </div>
    """,
    unsafe_allow_html=True
)
st.write(f"目前的顏色代碼是：{hex_color.upper()}")
