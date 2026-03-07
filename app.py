import streamlit as st
from PIL import Image, ImageOps

st.title("🔍 小小偵探相機")

# 開啟相機
img_file = st.camera_input("拍一張偵探照吧！")

if img_file:
    # 讀取圖片
    img = Image.open(img_file)
    
    # 讓小朋友選一個濾鏡
    effect = st.radio("想要什麼特效？", ["原圖", "黑白老照片", "左右翻轉"])
    
    if effect == "黑白老照片":
        img = ImageOps.grayscale(img)
    elif effect == "左右翻轉":
        img = ImageOps.mirror(img)
        
    st.image(img, caption="這是你的特務照片！")
    st.success("照片處理完成，快給爸爸媽媽看！")
