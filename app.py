from flask import Flask, jsonify
import plotly.express as px
import pandas as pd
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Women Apparel API is running!",
        "endpoints": ["/api/price-trend"],
        "status": "active"
    })

@app.route('/api/price-trend')
def price_trend():
    # 模擬資料（之後可換成 MySQL 查詢）
    df = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024, 2025],
        'China_Price': [25.5, 26.8, 28.1, 29.5, 31.0, 32.5],
        'USA_Price': [48.0, 49.5, 52.0, 54.0, 56.0, 58.0],
        'World_Price': [35.0, 36.2, 37.8, 39.0, 40.5, 42.0]
    })

    fig = px.line(
        df, 
        x='Year', 
        y=['China_Price', 'USA_Price', 'World_Price'],
        title='中美全球女裝價格趨勢',
        labels={'value': '價格 (USD)', 'variable': '地區'}
    )
    fig.update_layout(
        template="plotly_white", 
        height=500,
        legend_title="地區"
    )

    # 轉成 Base64 圖片
    img_bytes = fig.to_image(format="png")
    img_b64 = base64.b64encode(img_bytes).decode()
    return jsonify({'image': f'data:image/png;base64,{img_b64}'})

# 關鍵：綁定 0.0.0.0 + 動態 PORT
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render 會自動注入 PORT
    app.run(host='0.0.0.0', port=port, debug=False)
