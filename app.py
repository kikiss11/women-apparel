from flask import Flask, jsonify
import plotly.express as px
import pandas as pd
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Women Apparel API is running!"})

@app.route('/ping')
def ping():
    return "pong", 200  # 喚醒用

@app.route('/api/price-trend')
def price_trend():
    df = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023, 2024, 2025],
        'China_Price': [25.5, 26.8, 28.1, 29.5, 31.0, 32.5],
        'USA_Price': [48.0, 49.5, 52.0, 54.0, 56.0, 58.0],
    })
    fig = px.line(df, x='Year', y=['China_Price', 'USA_Price'], title='Price Trend')
    img_bytes = fig.to_image(format="png")
    img_b64 = base64.b64encode(img_bytes).decode()
    return jsonify({'image': f'data:image/png;base64,{img_b64}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
