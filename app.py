import streamlit as st

st.set_page_config(page_title="我的童話書", page_icon="📖")

st.title("📖 創意小作家")

# 使用 columns 讓版面漂亮一點
col1, col2 = st.columns(2)

with col1:
    hero = st.text_input("誰是主角？", placeholder="例如：勇敢的小貓")
    location = st.text_input("他們在哪裡？", placeholder="例如：糖果森林")

with col2:
    action = st.text_input("他在做什麼？", placeholder="例如：尋找寶藏")
    food = st.selectbox("他最喜歡吃什麼？", ["巧克力", "草莓", "彩虹糖"])

if st.button("生成我的故事！"):
    # 這裡可以用簡單的字串組合，也可以串接 OpenAI API (進階)
    story = f"從前從前，有一隻{hero}住在{location}。有一天，他決定去{action}，路上一邊吃著他最愛的{food}，感覺非常幸福！"
    
    st.info(story)
    st.snow() # 灑下雪花特效！
