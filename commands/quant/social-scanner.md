---
name: quant:social-scanner
description: Scan Twitter/Reddit for sentiment spikes
argument-hint: [twitter|reddit|all]
allowed-tools:
  - Bash
  - Read
  - mcp__reddit__fetch_reddit_hot_threads
---

<objective>
Detect social media sentiment spikes.
</objective>

<process>

## Reddit Crypto Sentiment

Use mcp__reddit__fetch_reddit_hot_threads with subreddit "cryptocurrency" or "ethtrader"

## Check Cache

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SOCIAL SENTIMENT CACHE ==="
if [ -f "data/social_sentiment.db" ]; then
  sqlite3 data/social_sentiment.db "
  SELECT source, sentiment_score, datetime(timestamp, 'unixepoch', 'localtime')
  FROM sentiment_sources
  ORDER BY timestamp DESC
  LIMIT 10"
fi
```

</process>
