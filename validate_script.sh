#!/bin/bash
# Comprehensive validation script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           NEWS DOWNLOAD SCRIPT VALIDATION                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Quick download
echo "Test 1: Quick download (3 sources, 2 articles each)..."
timeout 60 python main.py --sources politico nbc abc --max-articles 2 > /tmp/test1.log 2>&1

if [ $? -eq 0 ]; then
    articles=$(grep "Total articles downloaded:" /tmp/test1.log | awk '{print $4}')
    echo "  ✓ PASS - Downloaded $articles articles"
else
    echo "  ✗ FAIL - Script failed or timed out"
    exit 1
fi

# Test 2: Check article content length
echo ""
echo "Test 2: Verify article content length..."
short_count=0
good_count=0

for file in $(find news_md -name "*.md" -mmin -5); do
    chars=$(wc -c < "$file")
    if [ $chars -lt 500 ]; then
        short_count=$((short_count + 1))
    else
        good_count=$((good_count + 1))
    fi
done

echo "  Articles with good content (>500 chars): $good_count"
echo "  Articles with short content (<500 chars): $short_count"

if [ $good_count -gt 0 ]; then
    echo "  ✓ PASS - Found articles with substantial content"
else
    echo "  ✗ FAIL - No articles with substantial content"
    exit 1
fi

# Test 3: Check for hangs
echo ""
echo "Test 3: Test for timeout issues..."
timeout 45 python main.py --sources nbc --max-articles 1 > /tmp/test3.log 2>&1

if [ $? -eq 0 ]; then
    echo "  ✓ PASS - No timeout issues detected"
elif [ $? -eq 124 ]; then
    echo "  ✗ FAIL - Script timed out (hanging)"
    exit 1
else
    echo "  ✗ FAIL - Script error"
    exit 1
fi

# Test 4: Check metadata
echo ""
echo "Test 4: Verify article metadata..."
recent_file=$(find news_md -name "*.md" -mmin -5 | head -1)

if [ -n "$recent_file" ]; then
    has_publication=$(grep -c "^\*\*Publication:\*\*" "$recent_file")
    has_source=$(grep -c "^\*\*Source:\*\*" "$recent_file")
    has_thumbnail=$(grep -c "^\!\[Article Thumbnail\]" "$recent_file")
    has_categories=$(grep -c "^\*\*Categories:\*\*" "$recent_file")
    
    if [ $has_publication -gt 0 ] && [ $has_source -gt 0 ] && [ $has_thumbnail -gt 0 ]; then
        echo "  ✓ PASS - Article has Publication, Source, and Thumbnail"
    else
        echo "  ✗ FAIL - Missing metadata fields"
        exit 1
    fi
else
    echo "  ⚠ SKIP - No recent articles to check"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  VALIDATION SUCCESSFUL                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ All tests passed!"
echo "✅ Script is working correctly"
echo "✅ Content scraping is functional"
echo "✅ No timeout issues detected"
echo ""
