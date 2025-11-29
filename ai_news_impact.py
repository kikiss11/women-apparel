from flask import Flask, jsonify
import requests
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)

# Your NewsAPI Key
NEWS_API_KEY = "bd920f04fb234fe980de8d079b351b26"

# Load Chinese FinBERT sentiment model (excellent for trade/finance news)
model_name = "yiyanghkust/finbert-tone-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Impact keywords (fine-tuned for apparel trade)
NEGATIVE_KEYWORDS = ["tariff", "duty", "quota", "trade war", "Section 301", "anti-dumping", "restriction", "ban", "sanction"]
POSITIVE_KEYWORDS = ["tax cut", "FTA", "RCEP", "CPTPP", "demand", "trend", "sustainable", "recycled", "organic"]
CHINA_EXPORT_RELATED = ["China", "Chinese", "Vietnam shift", "Bangladesh", "Turkey", "Indonesia", "Cambodia"]
US_IMPORT_RELATED = ["US", "USA", "United States", "Europe", "EU", "import"]

def calculate_impact_score(text):
    score = 3  # neutral base
    text_lower = text.lower()
    if any(k in text_lower for k in [k.lower() for k in NEGATIVE_KEYWORDS]): score -= 2
    if any(k in text_lower for k in [k.lower() for k in POSITIVE_KEYWORDS]): score += 1.5
    if any(k in text_lower for k in [k.lower() for k in CHINA_EXPORT_RELATED]): score -= 1
    if any(k in text_lower for k in [k.lower() for k in US_IMPORT_RELATED]): score += 1
    return max(1, min(5, int(score)))

def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    labels = ["Neutral", "Positive", "Negative"]
    return labels[probs.argmax().item()]

@app.route('/api/news-impact')
def news_impact():
    query = '(women apparel OR female clothing) AND (tariff OR trade OR import OR export OR fashion week OR sustainable)'
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=15&apiKey={NEWS_API_KEY}"
    
    try:
        articles = requests.get(url, timeout=10).json().get('articles', [])[:10]
        results = []
        
        for item in articles:
            title = item['title']
            desc = item.get('description') or ''
            full_text = title + " " + desc
            
            impact_level = calculate_impact_score(full_text)
            stars = "★" * impact_level + "☆" * (5 - impact_level)
            sentiment = get_sentiment(full_text)
            
            # AI one-sentence summary
            if any(k.lower() in full_text.lower() for k in ["tariff", "duty", "trade war"]):
                summary = f"Negative impact on China apparel exports"
            elif any(k in full_text.lower() for k in ["sustainable", "recycled", "organic"]):
                summary = "Positive for premium sustainable apparel exports"
            elif "fashion week" in full_text.lower():
                summary = "Boosts import demand in US/Europe"
            else:
                summary = f"{sentiment} impact on global trade"
            
            results.append({
                "title": title,
                "impact": stars,
                "sentiment": sentiment,
                "summary": summary,
                "date": datetime.strptime(item['publishedAt'][:10], "%Y-%m-%d").strftime("%b %d"),
                "source": item['source']['name'],
                "url": item['url']
            })
        
        # Daily AI conclusion
        avg_impact = sum(calculate_impact_score(a['title'] + " " + (a.get('description') or '')) for a in articles[:10]) / 10
        if avg_impact >= 4:
            conclusion = "Strong headwind for China exports. Recommend pivot to EU sustainable segment."
        elif avg_impact <= 2:
            conclusion = "Favorable conditions. Increase production for US/EU markets."
        else:
            conclusion = "Neutral environment. Monitor December tariff negotiations."
            
        return jsonify({
            "daily_conclusion": conclusion,
            "analyzed_count": len(results),
            "news": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
