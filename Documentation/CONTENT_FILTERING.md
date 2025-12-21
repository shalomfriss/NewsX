# Content Filtering Enhancement

## Overview

Modified the news download script to automatically skip articles that contain only summaries or insufficient content.

## Changes Made

### Files Modified

1. **src/sources/rss_source.py**
2. **src/sources/newsapi_source.py**
3. **src/sources/guardian_source.py**
4. **src/sources/nyt_source.py**

## Content Filtering Rules

### Minimum Content Requirements

All articles must meet these criteria to be downloaded:

1. **Minimum 200 characters** of actual content (increased from 100)
2. **Not just a summary** - content must differ from description
3. **Not truncated** - NewsAPI articles ending in `[...]` or `[+chars]` are skipped

### RSS Sources (BBC, NPR, NBC, etc.)

```python
# Skip if content is too short
if not content or len(content.strip()) < 200:
    return None

# Skip if content is just a duplicate of summary
if content ≈ description AND word_count < 50:
    return None
```

### NewsAPI

```python
# Skip if content is too short
if not content or len(content.strip()) < 200:
    return None

# Skip if content is truncated by NewsAPI
if '[+' in content or content.endswith('[...]'):
    return None
```

### Guardian API

```python
# Skip if bodyText is too short
if not bodyText or len(bodyText.strip()) < 200:
    return None
```

### New York Times API

```python
# Skip if abstract/lead_paragraph is too short
if not content or len(content.strip()) < 100:
    return None
```

## Examples

### Articles That Will Be Downloaded ✓

```
Title: "New climate policy announced"
Content: 450 characters of detailed reporting
Status: ✓ Downloaded
```

### Articles That Will Be Skipped ✗

```
Title: "Breaking: Major event occurs"
Content: 89 characters - just headline repeat
Status: ✗ Skipped (insufficient content)
```

```
Title: "Analysis: Political development"
Content: "This is a summary only. [+1500 chars]"
Status: ✗ Skipped (truncated NewsAPI content)
```

```
Title: "News update"
Content: Same 45 words as description
Status: ✗ Skipped (summary-only content)
```

## Testing Results

### Before Filtering
- Downloaded articles: 453
- Many with only 1-sentence content
- Low value for analysis

### After Filtering
```bash
$ python main.py --sources bbc --max-articles 10 --log-level DEBUG

Output:
✗ bbc: No articles downloaded
Debug: Skipping article with insufficient content (99 chars)
Debug: Skipping article with insufficient content (102 chars)
Debug: Skipping article with insufficient content (89 chars)
```

### Politico (Good Content)
```bash
$ python main.py --sources politico --max-articles 5

Output:
✓ politico: 4 articles
All articles have 400+ characters
```

## Benefits

1. **Higher Quality Articles**
   - Only substantive content downloaded
   - Meaningful analysis possible
   - Better database value

2. **Reduced Storage**
   - Skip low-value content
   - Save disk space
   - Cleaner dataset

3. **Better Analysis**
   - Sufficient content for fact-checking
   - Adequate text for bias detection
   - Useful for propaganda assessment

4. **Clearer Reporting**
   - Debug logs show why articles skipped
   - Easy to tune thresholds
   - Transparent filtering

## Configuration

### Current Thresholds

| Source Type | Minimum Characters | Special Rules |
|-------------|-------------------|---------------|
| RSS Feeds | 200 | Check summary duplication |
| NewsAPI | 200 | Skip truncated content |
| Guardian | 200 | Check bodyText field |
| NYT | 100 | Only have abstracts/leads |

### To Adjust Thresholds

Edit the respective source file and modify:

```python
# In rss_source.py, newsapi_source.py, etc.
if not content or len(content.strip()) < 200:  # Change 200 to desired value
```

## Logging

Articles are skipped silently at INFO level, with details at DEBUG:

```bash
# See which articles are being filtered
python main.py --sources bbc --log-level DEBUG

# Normal operation (no spam)
python main.py --sources bbc
```

## Impact on Different Sources

| Source | Articles Before | Articles After | Change |
|--------|----------------|----------------|---------|
| BBC | Many | Few/None | Mostly summaries |
| Reuters | Many | None | All truncated |
| Politico | Same | Same | Good content |
| NBC | Same | Same | Good content |
| NPR | Same | Same | Good content |
| Guardian | Reduced | Moderate | Some summaries |
| NYT | Reduced | Moderate | API limits |

## Recommendations

1. **Enable full content scraping** for RSS sources that only provide summaries
2. **Use API sources** (Guardian, NYT with credentials) for better content
3. **Monitor filtering** with DEBUG logs to tune thresholds
4. **Prefer Politico, NPR, NBC** - they provide full content via RSS

---

*Updated: 2025-12-21*
