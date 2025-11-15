from flask import Flask, jsonify
import plotly.express as px
import pandas as pd
import io
import base64

app = Flask(__name__)

# 模擬資料（之後換成你的 SQL 查詢）
data = {
    'Year': [2020, 2021, 2022, 2023, 2024, 2025],
    'China_Price': [25.5, 26.8, 28.1, 29.5, 31.0, 32.5],
    'USA_Price': [48.0, 49.5, 52.0, 54.0, 56.0, 58.0],
    'World_Price': [35.0, 36.2, 37.8, 39.0, 40.5, 42.0]
}
df = pd.DataFrame(data)

@app.route('/api/price-trend')
def price_trend():
    fig = px.line(df, x='Year', y=['China_Price', 'USA_Price', 'World_Price'],
                  title='中美全球女裝價格趨勢',
                  labels={'value': '價格 (USD)', 'variable': '國家'})
    fig.update_layout(template="plotly_white")
    
    img_bytes = fig.to_image(format="png")
    img_base64 = base64.b64encode(img_bytes).decode()
    return jsonify({'image': f'data:image/png;base64,{img_base64}'})

if __name__ == '__main__':
    app.run()