# Leaderboard

View the performance leaderboard for Hyperliquid Beast trading pairs.

## Usage

```
/quant:leaderboard [option]
```

Options:
- (none): Show full leaderboard
- `score <SYMBOL>`: Show detailed score for a specific pair
- `check <SYMBOL>`: Check if a pair is allowed to trade

## How Scoring Works

**Goal: MAKE THE MOST MONEY**

Score components:
- **PnL Base**: $1 profit = +10 points, $1 loss = -10 points
- **Time Bonus**: Recent trades (last 1-3 days) weighted 1.5-2x
- **Win Rate Bonus**: +20 points if WR > 60%, +10 if WR > 50%
- **Consistency Bonus**: +10 points for low variance
- **Drawdown Penalty**: -5 points per $1 max drawdown

## Performance Tiers

| Tier | Score | Capital Mult | Kelly Mult | Effect |
|------|-------|--------------|------------|--------|
| CHAMPION | >= 100 | 2.0x | 1.5x | Max rewards |
| ELITE | >= 50 | 1.5x | 1.25x | High performer |
| STANDARD | >= 0 | 1.0x | 1.0x | Normal |
| PROBATION | >= -25 | 0.5x | 0.75x | Underperforming |
| DISABLED | < -50 | 0x | 0x | Auto-disabled (6h cooldown) |

## Redemption

When a pair is disabled:
1. Wait 6 hours (cooldown period)
2. Automatically moves to PROBATION tier
3. Starts with 25% position size
4. Can work back up to higher tiers by making money

## Commands

```bash
# Show leaderboard
ssh quantpod 'cd /opt/alpha_engine/efg_paper_trading && /opt/alpha_engine/venv/bin/python performance_tracker.py leaderboard'

# Check specific pair
ssh quantpod 'cd /opt/alpha_engine/efg_paper_trading && /opt/alpha_engine/venv/bin/python performance_tracker.py check ETH'

# Get detailed score
ssh quantpod 'cd /opt/alpha_engine/efg_paper_trading && /opt/alpha_engine/venv/bin/python performance_tracker.py score JTO'
```

---

$ARGUMENTS
