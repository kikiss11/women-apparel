from ai_news_impact import app as ai_app
from flask import Flask, jsonify, request
import base64
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Keep your original price trend chart
@app.route('/api/price-trend')
def price_trend():
    df = pd.DataFrame({
        'Year': [2020,2021,2022,2023,2024,2025],
        'China_Price_Index': [25, 27, 29, 31, 33, 35],
        'USA_Price_Index': [48, 50, 53, 56, 59, 62]
    })
    fig = px.line(df, x='Year', y=['China_Price_Index','USA_Price_Index'],
                  title='Women Apparel Price Forecast 2020-2025',
                  labels={'value': 'Price Index', 'variable': 'Region'})
    fig.update_layout(template="plotly_white")
    img = fig.to_image(format="png")
    b64 = base64.b64encode(img).decode()
    return jsonify({"image": f"data:image/png;base64,{b64}"})

# Mount AI news analysis
app.register_blueprint(ai_app, url_prefix='')

@app.route('/')
def home():
    return "Women Apparel AI Platform API - Running!"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
