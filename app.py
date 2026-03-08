<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>旺角社區客廳 - 福利一叮</title>
    <style>
        body { font-family: '微軟正黑體', sans-serif; background-color: #f4f7f6; padding: 20px; }
        .container { max-width: 600px; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: auto; }
        h2 { color: #2c3e50; text-align: center; }
        .question { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        select, input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 15px; background-color: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 18px; margin-top: 20px; }
        button:hover { background-color: #219150; }
        #result { margin-top: 30px; display: none; padding: 20px; border-top: 2px dashed #27ae60; }
        .eligible-item { background: #e8f5e9; padding: 10px; margin-bottom: 10px; border-left: 5px solid #27ae60; }
    </style>
</head>
<body>

<div class="container">
    <h2>🤖 福利一叮：資助初審機</h2>
    <p style="text-align:center; color: #666;">（專為旺角區街坊設計）</p>

    <div class="question">
        <label>1. 您是否居住於油尖旺區的「劏房」？</label>
        <select id="isSubdivided">
            <option value="yes">係 (Yes)</option>
            <option value="no">唔係 (No)</option>
        </select>
    </div>

    <div class="question">
        <label>2. 您的年齡是？</label>
        <input type="number" id="age" placeholder="例如：65">
    </div>

    <div class="question">
        <label>3. 您的家庭每月總入息是否低於限額？ (例如二人家庭少於 $20,000)</label>
        <select id="lowIncome">
            <option value="yes">係 (Yes)</option>
            <option value="no">唔係 (No)</option>
        </select>
    </div>

    <button onclick="checkEligibility()">即刻叮一叮！</button>

    <div id="result">
        <h3 style="color: #27ae60;">叮！您可能有機會申請：</h3>
        <div id="list"></div>
        <p style="font-size: 0.9em; color: #888; margin-top: 20px;">* 以上結果僅供參考，請帶備文件搵「旺角區社區客廳」社工核實。</p>
    </div>
</div>

<script>
function checkEligibility() {
    const isSubdivided = document.getElementById('isSubdivided').value;
    const age = parseInt(document.getElementById('age').value);
    const lowIncome = document.getElementById('lowIncome').value;
    const list = document.getElementById('list');
    
    list.innerHTML = ""; // 清空舊結果
    let found = false;

    // 邏輯 1: 社區客廳會籍
    if (isSubdivided === 'yes' && lowIncome === 'yes') {
        addResult("旺角社區客廳會籍：免費用設施、平價洗衫、功導");
        found = true;
    }

    // 邏輯 2: 中電電力補助
    if (isSubdivided === 'yes') {
        addResult("中電「基層家庭電費補助」：可獲 $1,000 補貼");
    } else if (lowIncome === 'yes') {
        addResult("中電「基層家庭電費補助」：一般低收入戶可獲 $600 補貼");
    }

    // 邏輯 3: 長者醫療券獎賞
    if (age >= 65) {
        addResult("長者醫療券獎賞先導計劃：最高可獲 $1,500 額外獎賞");
        found = true;
    }

    // 邏輯 4: 地區康健站
    addResult("油尖旺地區康健中心：免費「三高」篩查及健康評估");

    document.getElementById('result').style.display = 'block';
}

function addResult(text) {
    const div = document.createElement('div');
    div.className = 'eligible-item';
    div.innerText = text;
    document.getElementById('list').appendChild(div);
}
</script>

</body>
</html>
