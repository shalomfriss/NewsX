# Quick Start Guide

Get up and running with the News Aggregator in 5 minutes!

## Installation

1. **Install Python dependencies**:
   ```bash
   cd /Users/206845153/Documents/repos/news/backend
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

## First Run

When you run the application for the first time:

1. **The app will detect missing credentials** and ask if you want to set them up
2. **A GUI window will appear** with a list of news sources
3. **Click the blue links** to open registration pages in your browser
4. **Copy your API keys** from each service
5. **Paste them into the GUI** and click "Save Credentials"

That's it! The app will start fetching news.

## Essential Commands

```bash
# Fetch news (with automatic credential setup)
python main.py

# Setup credentials manually
python main.py --setup-credentials

# View statistics
python main.py --stats

# Fetch from specific sources only
python main.py --sources bbc reuters npr

# Fetch from last 3 days
python main.py --days 3

# Custom search
python main.py --query "senate bills"
```

## Where Are My Articles?

By default, articles are saved in the `news_md/` directory as markdown files, organized by source:

```
news_md/
├── newsapi/
├── guardian/
├── bbc/
├── reuters/
└── ...
```

## Getting API Keys (Quick Links)

### NewsAPI (Free - 100 requests/day)
1. Go to: https://newsapi.org/register
2. Sign up with email
3. Copy API key from dashboard
4. Paste into credential manager

### The Guardian (Free)
1. Go to: https://open-platform.theguardian.com/access/
2. Register for a developer key
3. Copy the API key
4. Paste into credential manager

### New York Times (Free - 1000 requests/day)
1. Go to: https://developer.nytimes.com/get-started
2. Create an account
3. Create an app
4. Copy the API key
5. Paste into credential manager

### No API Key Needed
These sources work immediately without any setup:
- BBC, Reuters, Politico, The Hill
- NPR, CNN, ABC, CBS, NBC, PBS
- Washington Post, The Atlantic, ProPublica

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize settings in `.env` file (copy from `.env.example`)
- Try database storage for better querying
- Explore command-line options with `python main.py --help`

## Troubleshooting

**GUI doesn't appear?**
- Make sure tkinter is installed (included with most Python installations)
- On Linux: `sudo apt-get install python3-tk`

**No articles fetched?**
- Check your API keys are correct
- Run with debug: `python main.py --log-level DEBUG`
- Some sources may be temporarily unavailable

**Rate limit errors?**
- Free tiers have limits (NewsAPI: 100/day, NYT: 1000/day)
- Use fewer sources or upgrade to paid tier

## Example Workflow

```bash
# 1. First time setup
python main.py --setup-credentials

# 2. Fetch today's political news
python main.py --query "politics"

# 3. Check what was saved
python main.py --stats

# 4. View articles in news_md/ directory
ls -la news_md/newsapi/

# 5. Read an article
cat news_md/newsapi/20251107_*.md
```

Happy news aggregating!
