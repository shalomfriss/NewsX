# API Credentials Setup Guide

This guide walks you through obtaining and configuring API credentials for the News Aggregator application.

## Overview

The News Aggregator supports **17 news sources**:

- **3 require API keys** (free tiers available): NewsAPI, The Guardian, New York Times
- **14 work without API keys** via RSS: BBC, Reuters, AP, Politico, The Hill, NPR, CNN, ABC, CBS, NBC, PBS, Washington Post, The Atlantic, ProPublica

## Two Ways to Provide Credentials

### Option 1: Environment Variables (Recommended for Production)

Set credentials in your `.env` file or system environment:

```bash
NEWSAPI_API_KEY=your_actual_key_here
GUARDIAN_API_KEY=your_actual_key_here
NYT_API_KEY=your_actual_key_here
```

**Advantages:**
- Industry standard practice
- Works in containerized environments (Docker, Kubernetes)
- Easy to manage in CI/CD pipelines
- No GUI required for headless servers
- Priority over GUI-stored credentials

### Option 2: GUI Credential Manager

Run the credential setup wizard:

```bash
python main.py --setup-credentials
```

**Advantages:**
- User-friendly visual interface
- Clickable links to registration pages
- Credentials encrypted with Fernet
- Stored securely in `~/.news_aggregator/credentials.enc`
- Great for desktop/development environments

## How to Get API Keys

### 1. NewsAPI

**Registration URL:** https://newsapi.org/register

**Free Tier:**
- 100 requests per day
- Access to 80,000+ news sources worldwide
- No credit card required

**Step-by-Step:**

1. Navigate to https://newsapi.org/register
2. Fill in the registration form:
   - First Name
   - Email Address
   - Password
3. Click "Submit" button
4. You'll see your API key immediately on the confirmation page
5. Alternatively, log in to your dashboard at https://newsapi.org/account to view your key

**API Key Format:** 32-character hexadecimal string (e.g., `1234567890abcdef1234567890abcdef`)

**Testing Your Key:**

```bash
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
```

### 2. The Guardian

**Registration URL:** https://open-platform.theguardian.com/access

**Free Tier:**
- 5,000 requests per day
- 12 requests per second
- Access to Guardian content dating back to 1999
- No credit card required

**Step-by-Step:**

1. Navigate to https://open-platform.theguardian.com/access
2. Fill in the registration form:
   - Name
   - Email address
   - Reason for access (e.g., "Personal news aggregation project")
3. Click "Register" button
4. Check your email inbox for the API key
   - Subject line: "Guardian Open Platform registration"
   - The key will be included in the email body
5. Save the key securely

**API Key Format:** Long alphanumeric string

**Testing Your Key:**

```bash
curl "https://content.guardianapis.com/search?api-key=YOUR_API_KEY"
```

**Documentation:** https://open-platform.theguardian.com/documentation/

### 3. New York Times

**Registration URL:** https://developer.nytimes.com/get-started

**Free Tier:**
- 500 requests per day
- 5 requests per minute
- Access to article metadata (full text not available)
- No credit card required

**Step-by-Step:**

1. Navigate to https://developer.nytimes.com/get-started
2. Click "Get Started" or "Create Account"
3. Fill in your details:
   - Email address
   - Name
   - Password
4. Verify your email address
5. Log in to the developer portal
6. Go to **"My Apps"** section
7. Click **"+ New App"** button
8. Fill in app details:
   - App Name (e.g., "News Aggregator")
   - Description (e.g., "Personal news aggregation project")
9. Enable the APIs you want to use:
   - **Top Stories API** (recommended)
   - **Article Search API** (recommended)
   - Most Popular API
   - Archive API
10. Click "Create" or "Save"
11. Copy your API key from the app details page

**API Key Format:** Long alphanumeric string with hyphens

**Testing Your Key:**

```bash
curl "https://api.nytimes.com/svc/topstories/v2/home.json?api-key=YOUR_API_KEY"
```

**Documentation:** https://developer.nytimes.com/docs

**Important Notes:**
- Full article text is NOT available through the API
- API provides article metadata, headlines, abstracts, and links
- For noncommercial use only

## Configuration Methods

### Method 1: Using .env File (Recommended)

1. Copy the example environment file:

```bash
cd /Users/206845153/Documents/repos/news/backend
cp .env.example .env
```

2. Open `.env` in your text editor:

```bash
nano .env
# or
code .env
# or
vim .env
```

3. Find the API credentials section and uncomment the lines:

```bash
# Before:
# NEWSAPI_API_KEY=your_newsapi_key_here

# After:
NEWSAPI_API_KEY=1234567890abcdef1234567890abcdef
```

4. Add your actual API keys:

```bash
NEWSAPI_API_KEY=1234567890abcdef1234567890abcdef
GUARDIAN_API_KEY=your-guardian-key-from-email
NYT_API_KEY=your-nyt-key-with-hyphens
```

5. Save the file

6. **Important:** Never commit `.env` to version control
   - The `.gitignore` file already excludes it
   - `.env.example` is safe to commit (no real keys)

### Method 2: Using System Environment Variables

**Linux/macOS:**

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
export NEWSAPI_API_KEY="your_key_here"
export GUARDIAN_API_KEY="your_key_here"
export NYT_API_KEY="your_key_here"
```

Reload your shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

**Windows (PowerShell):**

```powershell
$env:NEWSAPI_API_KEY="your_key_here"
$env:GUARDIAN_API_KEY="your_key_here"
$env:NYT_API_KEY="your_key_here"
```

For persistent variables, use System Properties > Environment Variables.

**Windows (Command Prompt):**

```cmd
set NEWSAPI_API_KEY=your_key_here
set GUARDIAN_API_KEY=your_key_here
set NYT_API_KEY=your_key_here
```

### Method 3: Using GUI Credential Manager

1. Run the setup command:

```bash
python main.py --setup-credentials
```

2. A GUI window will appear with a form
3. For each service:
   - Click the blue registration link to open the signup page in your browser
   - Complete the registration process
   - Copy your API key
   - Paste it into the corresponding field in the GUI
4. Click "Save Credentials"
5. Credentials are encrypted and saved to `~/.news_aggregator/credentials.enc`

### Method 4: Automatic Prompt on First Run

If you run the app without credentials:

```bash
python main.py
```

The app will automatically detect missing credentials and show the GUI credential manager.

## Verifying Your Setup

### Check if Credentials are Loaded

```bash
python main.py --stats
```

This will show which sources have credentials configured.

### Test Fetching from a Specific Source

```bash
# Test NewsAPI
python main.py --sources newsapi

# Test The Guardian
python main.py --sources guardian

# Test New York Times
python main.py --sources nyt
```

If credentials are missing or invalid, you'll see error messages.

## Credential Priority

When the app looks for credentials, it checks in this order:

1. **Environment variables** (highest priority)
   - Format: `{SOURCE}_API_KEY`
   - Example: `NEWSAPI_API_KEY`

2. **Encrypted credential store** (GUI-saved credentials)
   - Location: `~/.news_aggregator/credentials.enc`
   - Encrypted with Fernet

If an environment variable is set, it will override the GUI-stored credential.

## Security Best Practices

### Do's

- Use environment variables in production
- Add `.env` to `.gitignore` (already done)
- Use separate API keys for different environments (dev, staging, prod)
- Rotate API keys periodically
- Store credentials in a password manager
- Use the encrypted credential store for desktop use

### Don'ts

- Never commit API keys to version control
- Never share API keys publicly
- Never hardcode API keys in source code
- Never include real keys in screenshots or documentation
- Never use production keys in development

## Troubleshooting

### "Invalid API Key" Error

**Symptoms:**
```
ERROR: Failed to fetch from newsapi: Invalid API key
```

**Solutions:**
1. Verify the key is copied correctly (no extra spaces)
2. Check if the key is activated (some services require email verification)
3. Ensure you're not exceeding rate limits
4. Test the key with curl (see testing commands above)

### "No Credentials Found" Warning

**Symptoms:**
```
WARNING: No credentials found for newsapi
```

**Solutions:**
1. Check that environment variables are set:
   ```bash
   echo $NEWSAPI_API_KEY
   ```
2. Verify `.env` file exists and is in the correct directory
3. Ensure the `.env` file is being loaded (check for `python-dotenv` in requirements)
4. Try using the GUI credential manager instead

### Environment Variables Not Loading

**Symptoms:**
- Keys are in `.env` but app says "No credentials found"

**Solutions:**
1. Verify `.env` file location:
   ```bash
   ls -la .env
   ```
2. Check file format (no spaces around `=`):
   ```bash
   # Correct:
   NEWSAPI_API_KEY=abc123

   # Wrong:
   NEWSAPI_API_KEY = abc123
   ```
3. Ensure `python-dotenv` is installed:
   ```bash
   pip install python-dotenv
   ```
4. Restart your terminal/shell

### Rate Limit Exceeded

**Symptoms:**
```
ERROR: Rate limit exceeded for newsapi
```

**Solutions:**
1. Wait for the rate limit to reset (usually 24 hours)
2. Reduce the number of articles fetched:
   ```bash
   python main.py --sources newsapi --max-articles 10
   ```
3. Use RSS sources instead (no rate limits)
4. Upgrade to a paid tier (if available)

### GUI Credential Manager Not Appearing

**Symptoms:**
- Run `--setup-credentials` but no window appears

**Solutions:**
1. Check if tkinter is installed:
   ```python
   python -c "import tkinter"
   ```
2. On Linux, install tkinter:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk

   # Fedora
   sudo dnf install python3-tkinter
   ```
3. On macOS, tkinter should be included with Python
4. Use environment variables instead (Method 1)

## Managing Multiple Configurations

### Development vs Production

**Development `.env`:**
```bash
NEWSAPI_API_KEY=dev_key_here
GUARDIAN_API_KEY=dev_key_here
NYT_API_KEY=dev_key_here
MAX_ARTICLES_PER_SOURCE=10
```

**Production `.env`:**
```bash
NEWSAPI_API_KEY=prod_key_here
GUARDIAN_API_KEY=prod_key_here
NYT_API_KEY=prod_key_here
MAX_ARTICLES_PER_SOURCE=50
```

### Using Docker

**Dockerfile:**
```dockerfile
ENV NEWSAPI_API_KEY=${NEWSAPI_API_KEY}
ENV GUARDIAN_API_KEY=${GUARDIAN_API_KEY}
ENV NYT_API_KEY=${NYT_API_KEY}
```

**docker-compose.yml:**
```yaml
services:
  news-aggregator:
    environment:
      - NEWSAPI_API_KEY=${NEWSAPI_API_KEY}
      - GUARDIAN_API_KEY=${GUARDIAN_API_KEY}
      - NYT_API_KEY=${NYT_API_KEY}
    env_file:
      - .env
```

### CI/CD Pipelines

**GitHub Actions:**
```yaml
env:
  NEWSAPI_API_KEY: ${{ secrets.NEWSAPI_API_KEY }}
  GUARDIAN_API_KEY: ${{ secrets.GUARDIAN_API_KEY }}
  NYT_API_KEY: ${{ secrets.NYT_API_KEY }}
```

Store keys in GitHub Secrets: Settings > Secrets and variables > Actions

## Rate Limits Summary

| Source | Requests/Day | Requests/Minute | Requests/Second | Notes |
|--------|--------------|-----------------|-----------------|-------|
| NewsAPI | 100 | ~1 | ~0.02 | Free tier, development only |
| The Guardian | 5,000 | 83 | 12 | Very generous free tier |
| New York Times | 500 | 5 | ~0.08 | Per API (Top Stories, Search, etc.) |
| RSS Sources | Unlimited* | Unlimited* | Unlimited* | Respect robots.txt, be courteous |

*RSS sources don't have hard limits but should be used responsibly.

## Additional Resources

### Official Documentation

- **NewsAPI:** https://newsapi.org/docs
- **The Guardian:** https://open-platform.theguardian.com/documentation/
- **New York Times:** https://developer.nytimes.com/docs

### Support

- **NewsAPI:** support@newsapi.org
- **The Guardian:** https://groups.google.com/g/guardian-api-talk
- **New York Times:** code@nytimes.com

### API Status Pages

Check if services are experiencing outages:

- **NewsAPI:** https://status.newsapi.org/ (if available)
- **The Guardian:** Check https://www.theguardian.com/
- **New York Times:** Check https://www.nytimes.com/

## Summary Checklist

Before running the News Aggregator, ensure:

- [ ] You've registered for API keys at:
  - [ ] https://newsapi.org/register
  - [ ] https://open-platform.theguardian.com/access
  - [ ] https://developer.nytimes.com/get-started
- [ ] You've chosen a credential method:
  - [ ] Environment variables in `.env` file, OR
  - [ ] GUI credential manager, OR
  - [ ] System environment variables
- [ ] You've tested your credentials with the provided curl commands
- [ ] You've verified credentials are loaded (`python main.py --stats`)
- [ ] You understand the rate limits for each service
- [ ] Your `.env` file is in `.gitignore` (already done)

## Quick Start Command

Once credentials are configured:

```bash
# Fetch from all sources
python main.py

# Fetch from specific sources
python main.py --sources newsapi guardian nyt

# Fetch without API sources (RSS only)
python main.py --sources bbc reuters politico npr
```

Enjoy aggregating news from 17 reputable sources!
