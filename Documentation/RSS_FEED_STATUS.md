# RSS Feed Status

This document tracks the status of RSS feeds for various news sources.

## Working Sources ✓

| Source | Status | Notes |
|--------|--------|-------|
| BBC | ✓ Working | Multiple feeds available |
| NBC | ✓ Working | Politics and news feeds |
| PBS | ✓ Working | NewsHour feeds |
| NPR | ✓ Working | Multiple topic feeds |
| Politico | ✓ Working | Updated to new feed URL |
| The Hill | ✓ Working | Multiple section feeds |
| ABC | ✓ Working | News and politics |
| CBS | ✓ Working | Main and politics RSS |
| Washington Post | ✓ Working | Politics and national |
| The Atlantic | ✓ Working | Main and politics feeds |
| ProPublica | ✓ Working | Main feed |
| Al Jazeera | ✓ Working | Multiple regional feeds |

## Unavailable/Broken Sources ✗

| Source | Status | Issue | Last Checked |
|--------|--------|-------|--------------|
| Reuters | ✗ Broken | All RSS feeds return HTML/blocked by captcha | 2025-12-21 |
| CNN | ✗ Broken | RSS feeds timeout/hang | 2025-12-21 |

## Recent Changes

### 2025-12-21
- **Politico**: Updated feed URL from `politico.com/rss/politics08.xml` to `rss.politico.com/politics-news.xml`
- **Reuters**: All RSS feeds unavailable (returning HTML with captcha)
- **CNN**: RSS feeds cause timeout issues, disabled for stability

## Notes

- Sources marked as ✗ are temporarily disabled to prevent script hanging
- Full content scraping is disabled by default to improve reliability
- Feed URLs are validated periodically and may need updates
