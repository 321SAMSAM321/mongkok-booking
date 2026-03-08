import streamlit as st
import streamlit.components.v1 as components

# 設置網頁標題
st.set_page_config(page_title="旺角社區客廳 - 福利一叮", layout="centered")

st.title("🤖 福利一叮：資助初審機")
st.write("這是專為旺角區「社區資源諮詢站」設計的初步篩選工具。")

# 定義 HTML 內容 (即是你之前的代碼)
html_code = """
<div id="welfare-tool" style="font-family: '微軟正黑體', sans-serif; background: white; padding: 20px; border-radius: 15px; border: 1px solid #ddd;">
    <div style="margin-bottom: 15px;">
        <label><b>1. 您是否居住於油尖旺區的「劏房」？</b></label>
        <select id="isSubdivided" style="width:100%; padding:10px; margin-top:5px;">
            <option value="yes">係 (Yes)</option>
            <option value="no">唔係 (No)</option>
        </select>
    </div>

    <div style="margin-bottom: 15px;">
        <label><b>2. 您的年齡是？</b></label>
        <input type="number" id="age" placeholder="例如：65" style="width:100%; padding:10px; margin-top:5px;">
    </div>

    <div style="margin-bottom: 15px;">
        <label><b>3. 您的家庭每月總入息是否低於限額？</b></label>
        <select id="lowIncome" style="width:100%; padding:10px; margin-top:5px;">
            <option value="yes">係 (Yes)</option>
            <option value="no">唔係 (No)</option>
        </select>
    </div>

    <button onclick="checkEligibility()" style="width: 100%; padding: 15px; background-color: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 18px;">即刻叮一叮！</button>

    <div id="result" style="margin-top: 20px; display: none; padding: 15px; border-top: 2px dashed #27ae60;">
        <h3 style="color: #27ae60;">叮！您可能有機會申請：</h3>
        <div id="list"></div>
    </div>
</div>

<script>
function checkEligibility() {
    const isSubdivided = document.getElementById('isSubdivided').value;
    const age = parseInt(document.getElementById('age').value);
    const lowIncome = document.getElementById('lowIncome').value;
    const list = document.getElementById('list');
    
    list.innerHTML = "";
    
    if (isSubdivided === 'yes' && lowIncome === 'yes') {
        addResult("✅ 旺角社區客廳會籍：免費用設施、平價洗衫、功導");
    }
    if (isSubdivided === 'yes') {
        addResult("✅ 中電「基層家庭電費補助」：可獲 $1,000 補貼");
    } else if (lowIncome === 'yes') {
        addResult("✅ 中電「基層家庭電費補助」：一般低收入戶可獲 $600 補貼");
    }
    if (age >= 65) {
        addResult("✅ 長者醫療券獎賞先導計劃：最高可獲 $1,500 額外獎賞");
    }
    addResult("✅ 油尖旺地區康健中心：免費「三高」篩查及健康評估");

    document.getElementById('result').style.display = 'block';
}

function addResult(text) {
    const div = document.createElement('div');
    div.style.cssText = "background: #e8f5e9; padding: 10px; margin-bottom: 8px; border-left: 5px solid #27ae60;";
    div.innerText = text;
    document.getElementById('list').appendChild(div);
}
</script>
"""

# 在 Streamlit 中嵌入 HTML
components.html(html_code, height=600, scrolling=True)

st.info("💡 提示：請帶備租約、電費單及入息證明，與諮詢站社工核實。")
