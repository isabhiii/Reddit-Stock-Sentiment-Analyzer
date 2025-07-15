from flask import Flask, render_template, request, jsonify
from reddit_sentiment import RedditSentimentAnalyzer
from stock_data import StockDataFetcher
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize analyzers
sentiment_analyzer = RedditSentimentAnalyzer()
stock_fetcher = StockDataFetcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get stock symbol and parameters from form
        stock_symbol = request.form.get('stock_symbol', '').upper()
        time_filter = request.form.get('time_filter', 'month')
        limit = int(request.form.get('limit', 100))
        max_comments = int(request.form.get('max_comments', 10))
        
        # Get Reddit sentiment with parameters
        sentiment_data = sentiment_analyzer.analyze_sentiment(
            stock_symbol,
            time_filter=time_filter,
            limit=limit,
            max_comments=max_comments
        )
        
        # Get stock data
        stock_data = stock_fetcher.get_stock_data(stock_symbol)
        
        # Combine the data
        result = {
            'stock_symbol': stock_symbol,
            'sentiment': sentiment_data,
            'stock_data': stock_data,
            'analysis_parameters': {
                'time_filter': time_filter,
                'posts_limit': limit,
                'comments_per_post': max_comments
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)