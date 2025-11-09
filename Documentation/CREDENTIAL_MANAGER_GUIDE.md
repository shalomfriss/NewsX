# Credential Manager User Guide

## Overview

The News Aggregator features an improved GUI credential manager that makes it easy to set up API credentials for news sources.

## Key Improvements

### ✅ What's New

1. **Clear Source Identification**
   - Each news source is in its own labeled section
   - Source name prominently displayed as section header
   - Description shows what each source provides
   - Easy-to-spot registration links

2. **Show/Hide API Keys**
   - Each API key field has a "👁️ Show" button
   - Click to toggle between hidden (••••) and visible text
   - Verify you copied the key correctly before saving
   - Button changes to "🔒 Hide" when key is visible

3. **Real-time Feedback**
   - Status messages appear at the top of the window
   - See confirmation when clicking registration links
   - Validation messages before saving
   - Success/error notifications with details

4. **Better Visual Organization**
   - Larger window (900x700) for easier reading
   - Each source in a separate bordered section
   - Placeholder text in input fields
   - Clearer button labels with icons

5. **Helpful Messages**
   - Shows how many sources need credentials
   - Reminds you that 14 sources work without API keys
   - Detailed skip confirmation
   - Success message lists which sources were configured

## How to Use

### Step 1: Launch the Credential Manager

```bash
# First time running the app
python main.py

# Or explicitly setup credentials
python main.py --setup-credentials
```

### Step 2: Understand the Window

When the credential manager opens, you'll see:

```
🔑 API Credentials Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Setting up API credentials for 3 source(s).
💡 Click the blue registration links to sign up and get your free API keys.
👁️  Use the 'Show' buttons to verify your API keys are entered correctly.
📝 Note: 14 other sources work via RSS without any setup!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

╔═══════════════════════════════════════════╗
║  NewsAPI                                  ║
╠═══════════════════════════════════════════╣
║ 📰 Access to 80,000+ news sources worldwide
║ 🔗 Get your API key here: https://newsapi.org/register
║
║ Api Key *  [Paste your API key here    ] [👁️  Show]
╚═══════════════════════════════════════════╝

╔═══════════════════════════════════════════╗
║  The Guardian                             ║
╠═══════════════════════════════════════════╣
║ 📰 Guardian news and content API
║ 🔗 Get your API key here: https://open-platform.theguardian.com/access
║
║ Api Key *  [Paste your API key here    ] [👁️  Show]
╚═══════════════════════════════════════════╝

... (more sources) ...

[⏭️  Skip for Now]                    [💾 Save Credentials]
```

### Step 3: Get Your API Keys

For each source you want to use:

1. **Click the blue registration link**
   - Your browser will open to the registration page
   - The status bar will show: "Opening registration page for [Source Name]..."

2. **Complete the registration**
   - Follow the source-specific instructions
   - See [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md) for detailed steps

3. **Copy your API key**
   - NewsAPI: Shown immediately after signup
   - The Guardian: Sent to your email
   - New York Times: In your app dashboard

### Step 4: Enter Your API Keys

1. **Click in the input field**
   - The placeholder text "Paste your API key here" will disappear
   - The field is ready for your API key

2. **Paste your API key**
   - Right-click → Paste, or Ctrl+V (Cmd+V on Mac)
   - The key will appear as dots (••••••) for security

3. **Verify your key (recommended)**
   - Click the "👁️ Show" button to reveal the key
   - Check that it was pasted correctly
   - Click "🔒 Hide" to hide it again

### Step 5: Save Your Credentials

Once you've entered API keys for at least one source:

1. **Click "💾 Save Credentials"**
   - Status bar shows: "📝 Validating credentials..."
   - Then: "💾 Saving credentials for X source(s)..."

2. **Review the confirmation**
   - A popup will show which sources were configured
   - Example:
     ```
     ✅ Successfully saved credentials for:

       • NewsAPI
       • The Guardian

     2 API source(s) are now configured!
     ```

3. **Click OK**
   - The credential manager will close
   - The app will continue with news fetching

### Skipping Credential Setup

If you want to use only RSS sources (no API keys needed):

1. **Click "⏭️ Skip for Now"**

2. **Confirm the skip dialog**
   - Shows which 14 sources work without API keys
   - Shows which 3 sources won't be available
   - Explains how to add credentials later

3. **Click Yes to confirm**
   - The app will continue with RSS sources only

## Understanding the Status Messages

| Status | Meaning |
|--------|---------|
| "Opening registration page for [Source]..." | Browser opened to registration page |
| "📝 Validating credentials..." | Checking what you entered |
| "💾 Saving credentials for X source(s)..." | Encrypting and saving to disk |
| "✅ Credentials saved successfully!" | All credentials saved |
| "⚠️ No credentials entered" | No API keys were entered |
| "❌ Failed to save credentials" | An error occurred (see error dialog) |
| "⏭️ Skipping credential setup" | Skipped, using RSS sources only |

## What Happens After Saving?

Your credentials are:

1. **Encrypted with Fernet encryption**
   - Industry-standard symmetric encryption
   - Encryption key stored separately

2. **Saved to your home directory**
   - Location: `~/.news_aggregator/credentials.enc`
   - File permissions: 600 (read/write by you only)

3. **Used automatically**
   - The app loads them on next run
   - No need to re-enter unless you want to update

## Updating Credentials Later

To change or add credentials:

```bash
python main.py --setup-credentials
```

- Existing credentials will be preserved
- You can add new ones or replace old ones
- Empty fields won't overwrite existing credentials

## Troubleshooting

### "The window is blank or not showing fields"

**Solution:** The window might be too small. Try:
- Resize the window (drag the corner)
- Scroll down with the scrollbar on the right
- The window should be at least 700x500 pixels

### "I clicked Save but nothing happened"

**Possible causes:**
1. No credentials were entered
   - Make sure to paste API keys in the fields
   - Don't leave the placeholder text

2. All fields had placeholder text
   - Click in each field and paste a real API key
   - The placeholder "Paste your API key here" is ignored

**What you'll see:**
- Status bar: "⚠️ No credentials entered"
- Dialog asking if you want to skip

### "I can't see what I'm typing"

**Solution:** The API key field is masked for security

1. Type or paste normally (you won't see it)
2. Click "👁️ Show" to reveal the text
3. Verify it's correct
4. Click "🔒 Hide" to mask it again

### "Error Saving Credentials"

**Possible causes:**
1. Permission issues with `~/.news_aggregator/`
2. Disk full
3. Invalid characters in API key

**Solutions:**
1. Check the error dialog for specific error message
2. Ensure `~/.news_aggregator/` directory is writable
3. Try re-copying the API key from the source

### "I clicked the link but nothing happened"

**Solutions:**
1. Make sure you have a default browser set
2. Check if a browser window opened in the background
3. Copy the URL manually:
   - NewsAPI: https://newsapi.org/register
   - Guardian: https://open-platform.theguardian.com/access
   - NYT: https://developer.nytimes.com/get-started

## Alternative: Environment Variables

If you prefer not to use the GUI, you can set credentials via environment variables:

```bash
# Edit your .env file
nano .env

# Add your API keys:
NEWSAPI_API_KEY=your_key_here
GUARDIAN_API_KEY=your_key_here
NYT_API_KEY=your_key_here
```

See [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md) for complete instructions.

## Security Notes

✅ **Safe:**
- Credentials are encrypted before storage
- API keys are masked by default in the UI
- File permissions prevent other users from reading

⚠️ **Be Careful:**
- Don't share screenshots with API keys visible
- Don't commit the credentials file to Git
- Close the window when done if in a shared environment

❌ **Never:**
- Share your API keys with others
- Post credentials in public forums or chat
- Use production API keys in development

## Quick Reference

| Action | How To |
|--------|--------|
| Show API key | Click "👁️ Show" button next to field |
| Hide API key | Click "🔒 Hide" button next to field |
| Open registration page | Click blue underlined URL |
| Save credentials | Click "💾 Save Credentials" button |
| Skip setup | Click "⏭️ Skip for Now" button |
| Update credentials | Run `python main.py --setup-credentials` |
| Use env vars instead | Edit `.env` file, see CREDENTIALS_SETUP.md |

## Getting Help

- **Detailed credential instructions:** [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md)
- **Architecture details:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Main README:** [README.md](../README.md)
- **Quick start:** [QUICKSTART.md](QUICKSTART.md)

---

**Remember:** You only need to set up the sources you want to use. The app works perfectly fine with just the free RSS sources (no API keys needed)!
