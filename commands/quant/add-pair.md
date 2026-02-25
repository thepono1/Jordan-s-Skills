---
name: quant:add-pair
description: Validate a new pair on Kraken, add to config, restart system, and commit
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

<objective>
Safely add a new trading pair to the hybrid trader. Validate it exists on Kraken, check liquidity, add to config, restart the system, and commit changes.
</objective>

<arguments>
- pair: Trading pair to add (e.g., "PEPE/USD", "ARB/USD")
- capital: Capital to allocate (default: $100)
- bb_std: Bollinger Band standard deviation (default: 2.0, use 2.5 for high vol)
</arguments>

<process>

## 1. Validate Pair on Kraken

```bash
cd ~/Developer/quant_master/quant_v4/efg_paper_trading

# Check if pair exists
python3 -c "
import ccxt
kraken = ccxt.kraken()
markets = kraken.load_markets()
pair = '{pair}'
if pair in markets:
    m = markets[pair]
    print(f'✅ {pair} exists on Kraken')
    print(f'   Min order: {m.get(\"limits\", {}).get(\"amount\", {}).get(\"min\", \"?\")}')
    print(f'   Price precision: {m.get(\"precision\", {}).get(\"price\", \"?\")}')
else:
    print(f'❌ {pair} NOT FOUND on Kraken')
    print('Available similar:', [p for p in markets if pair.split('/')[0] in p][:5])
"
```

## 2. Check Current Volatility

```bash
python3 -c "
import ccxt
kraken = ccxt.kraken()
ohlcv = kraken.fetch_ohlcv('{pair}', '1h', limit=24)
closes = [c[4] for c in ohlcv]
returns = [(closes[i] - closes[i-1]) / closes[i-1] * 100 for i in range(1, len(closes))]
vol = (sum(r**2 for r in returns) / len(returns)) ** 0.5
print(f'24h Volatility: {vol:.2f}%')
print(f'Recommended BB std: {2.5 if vol > 2.0 else 2.0}')
"
```

## 3. Add to Hybrid Trader Config

Edit `hybrid_trader.py` PAIRS list:

```python
{'symbol': '{pair}', 'bb_std': {bb_std}, 'capital': {capital}},
```

## 4. Restart System

```bash
cd ~/Developer/quant_master/quant_v4/efg_paper_trading

# Kill and restart
pkill -f "hybrid_trader" 2>/dev/null
sleep 2

# Restart via supervisor (it will pick up the new config)
pkill -f "supervisor.py" 2>/dev/null
sleep 2
nohup python3 supervisor.py > logs/supervisor.log 2>&1 &

sleep 15

# Verify new pair is being tracked
grep "{pair}" logs/HybridTrader.log | tail -3
```

## 5. Commit Changes

```bash
cd ~/Developer/quant_master/quant_v4
git add efg_paper_trading/hybrid_trader.py
git commit -m "feat: Add {pair} to hybrid trader

- Capital: ${capital}
- BB std: {bb_std}
- 24h vol: [X]%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

git push origin main
```

## 6. Update Obsidian

Add the new pair to the pairs table in `weekend-hybrid-trading-system.md`.

</process>

<success_criteria>
- [ ] Pair validated on Kraken
- [ ] Volatility checked
- [ ] Config updated
- [ ] System restarted
- [ ] Pair appearing in logs
- [ ] Changes committed
- [ ] Obsidian updated
</success_criteria>
