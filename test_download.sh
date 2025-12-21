#!/bin/bash
# Test download with timeout protection

echo "Testing news download with 60-second timeout..."
timeout 60 python main.py --sources abc nbc politico --max-articles 2 

if [ $? -eq 124 ]; then
    echo ""
    echo "ERROR: Download timed out after 60 seconds"
    echo "This usually means content scraping is hanging"
    exit 1
else
    echo ""
    echo "SUCCESS: Download completed"
fi
