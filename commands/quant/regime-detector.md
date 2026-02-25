---
name: quant:regime-detector
description: Detect current market regime and sentiment
argument-hint: [current|history|details]
allowed-tools:
  - Bash
  - Read
---

<objective>
Get instant read on current market regime from emotion engine. Used for position sizing and strategy selection.
</objective>

<context>
Regimes:
- EUPHORIA: 50% position reduction
- OPTIMISM: Normal sizing
- NEUTRAL: Normal sizing
- ANXIETY: 25% reduction
- PANIC: Opportunistic buys

Database: data/social_sentiment.db
</context>

<process>

## 1. Parse Command

Default: current regime

Commands:
- `current` - Current regime and confidence
- `history` - Regime changes over time
- `details` - Full sentiment breakdown

## 2. Execute Command

### current
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CURRENT MARKET REGIME ==="

# Check emotion engine state
sqlite3 data/social_sentiment.db "
SELECT
  regime,
  confidence,
  datetime(timestamp, 'unixepoch', 'localtime') as last_update
FROM regime_state
ORDER BY timestamp DESC
LIMIT 1" 2>/dev/null || echo "Regime data not available"

# Check state machine if available
if [ -f emotion_engine/state_machine.py ]; then
  python3 -c "
import sys
sys.path.insert(0, 'emotion_engine')
try:
    from state_machine import get_current_regime
    regime = get_current_regime()
    print(f'Live Regime: {regime}')
except:
    pass
" 2>/dev/null
fi

# Position sizing recommendation
echo ""
echo "=== POSITION SIZING ==="
sqlite3 data/social_sentiment.db "
SELECT
  regime,
  CASE regime
    WHEN 'EUPHORIA' THEN '50% reduction'
    WHEN 'OPTIMISM' THEN 'Normal (100%)'
    WHEN 'NEUTRAL' THEN 'Normal (100%)'
    WHEN 'ANXIETY' THEN '25% reduction'
    WHEN 'PANIC' THEN 'Opportunistic buys'
    ELSE 'Unknown'
  END as sizing_recommendation
FROM regime_state
ORDER BY timestamp DESC
LIMIT 1" 2>/dev/null
```

### history
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== REGIME HISTORY (24h) ==="
sqlite3 -header -column data/social_sentiment.db "
SELECT
  datetime(timestamp, 'unixepoch', 'localtime') as time,
  regime,
  confidence,
  ROUND(sentiment_score, 2) as sentiment
FROM regime_state
WHERE timestamp > strftime('%s', 'now', '-24 hours')
ORDER BY timestamp DESC" 2>/dev/null || echo "No history available"
```

### details
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SENTIMENT BREAKDOWN ==="
sqlite3 -header -column data/social_sentiment.db "
SELECT
  source,
  ROUND(sentiment_score, 2) as score,
  ROUND(confidence, 2) as confidence,
  datetime(timestamp, 'unixepoch', 'localtime') as updated
FROM sentiment_sources
ORDER BY timestamp DESC" 2>/dev/null || echo "No sentiment sources"

echo ""
echo "=== AGGREGATED METRICS ==="
sqlite3 data/social_sentiment.db "
SELECT
  ROUND(AVG(sentiment_score), 2) as avg_sentiment,
  ROUND(AVG(confidence), 2) as avg_confidence,
  COUNT(DISTINCT source) as sources
FROM sentiment_sources
WHERE timestamp > strftime('%s', 'now', '-1 hour')" 2>/dev/null
```

## 3. Present Results

```
# Market Regime

## Current State
- Regime: [EUPHORIA/OPTIMISM/NEUTRAL/ANXIETY/PANIC]
- Confidence: [X]%
- Last Update: [time]

## Position Sizing
- Recommendation: [sizing adjustment]
- Reason: [regime-based logic]

## Sentiment Sources
| Source | Score | Weight |
|--------|-------|--------|
| Twitter | 0.6 | 30% |
| Reddit | 0.4 | 20% |
```

</process>

<success_criteria>
- [ ] Current regime identified
- [ ] Confidence level reported
- [ ] Sizing recommendation provided
- [ ] Source breakdown available
</success_criteria>
