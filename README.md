# Reddit Stock Sentiment Analyzer

A web application that analyzes Reddit sentiment and stock data for any given stock symbol. It fetches posts and comments from multiple subreddits, performs sentiment analysis using TextBlob, and visualizes the results with interactive charts and dashboards.

## Features
- Analyze sentiment from Reddit posts **and comments**
- Supports multiple subreddits: `stocks`, `investing`, `wallstreetbets`, `pennystocks`, `cryptostreetbets`, `options`, `SecurityAnalysis`, `StockMarket`
- Configurable time duration (hour, day, week, month, year, all)
- Adjustable number of posts and comments per post
- Sentiment analysis for both posts and comments
- Stock data integration (via Yahoo Finance)
- Modern, responsive dashboard UI with dark/light mode
- Visualizations: sentiment distribution, trends, post quality, and more

## Getting Started

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/reddit-stock-sentiment.git
   cd reddit-stock-sentiment/stock
   ```
2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
3. **Set up Reddit API credentials:**
   - Create a Reddit app at [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
   - Add the following to your `.env` file:
     ```env
     REDDIT_CLIENT_ID=your_client_id
     REDDIT_CLIENT_SECRET=your_client_secret
     REDDIT_USER_AGENT=StockAnalyzer:v1.0
     ```
     
## Usage
1. **Run the application:**
   ```bash
   python3 src/app.py
   ```
2. **Open your browser:**
   - Go to [http://localhost:5000](http://localhost:5000)
3. **Enter a stock symbol** (e.g., `AAPL`, `TSLA`, `PLTR`), select time duration, post/comment limits, and analyze.

## Configuration Options
- **Stock Symbol:** The ticker to analyze (e.g., `AAPL`)
- **Time Duration:** hour, day, week, month, year, all
- **Posts Limit:** Number of Reddit posts to fetch (default: 100)
- **Comments per Post:** Number of top comments to analyze per post (default: 10)

## Project Structure
```
stock/
├── .env
├── README.md
├── requirements.txt
├── src/
│   ├── app.py
│   ├── reddit_sentiment.py
│   ├── stock_data.py
│   ├── templates/
│   │   └── index.html
│   └── visualization/
│       └── plotter.py
└── stock_sentiment.py
```

## Notes
- The first analysis for a symbol may take longer due to Reddit API rate limits and comment fetching.
- For best results, use valid Reddit API credentials and moderate post/comment limits.
- You can customize the UI further in `src/templates/index.html`.#

# Attribution & Credits

This project is based on the original work by [TiffinTech's Reddit stock analysis](https://github.com/TiffinTech/stock). I would like to thank her for making the source code available and inspiring this project.

I have made significant modifications and enhancements, including:
- Expanding data sources (more subreddits, Reddit comments, etc.)
- Adding Twitter/StockTwits integration (if applicable)
- Improving the UI/UX and dashboard features
- Making the analysis parameters configurable
- Additional bug fixes and optimizations

If you are interested in the original version, please check out her repository [here](https://github.com/TiffinTech/stock).

---

*This project is for educational and research purposes. All credit for the original concept and code structure goes to the original creator.*
