---
name: quant:cost-report
description: Track trading and infrastructure costs
argument-hint: [trading|infra|total]
allowed-tools:
  - Bash
  - Read
---

<objective>
Weekly cost report covering trading fees, infrastructure, and data costs.
</objective>

<process>

## 1. Trading Costs

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== TRADING COSTS ==="

# Estimate fees (Kraken: ~0.16% maker, 0.26% taker)
sqlite3 efg_paper_trading/trading.db "
SELECT
  'This Week' as period,
  COUNT(*) as trades,
  ROUND(SUM(quantity * price), 2) as volume,
  ROUND(SUM(quantity * price) * 0.002, 2) as estimated_fees
FROM trades
WHERE timestamp > strftime('%s', 'now', '-7 days')" 2>/dev/null
```

## 2. Infrastructure Costs

```bash
echo ""
echo "=== INFRASTRUCTURE COSTS (Monthly) ==="

cat << EOF
VPS (quantpod): ~$50/mo
RunPod GPU (variable): ~$20-100/mo
Domain/SSL: ~$5/mo
---
Base: ~$75/mo

Data Savings (DIY vs Commercial):
- Alternative data: $9,000/mo saved
- Market data: $500/mo saved
---
Net Monthly Benefit: +$9,425/mo
EOF
```

## 3. Data Provider Costs

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DATA COSTS ==="

# Count active integrations
integration_count=$(ls integrations/*.py 2>/dev/null | wc -l | tr -d ' ')
echo "Active DIY integrations: $integration_count"
echo "Commercial equivalent: ~\$250-300/integration/mo"
echo "DIY approach: \$0 (self-maintained)"
echo "Savings: ~\$$(($integration_count * 250))/mo"
```

## 4. Cost Summary

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== COST SUMMARY ==="

# Get week's trading volume
volume=$(sqlite3 efg_paper_trading/trading.db "SELECT COALESCE(SUM(quantity * price), 0) FROM trades WHERE timestamp > strftime('%s', 'now', '-7 days')" 2>/dev/null || echo "0")
fees=$(python3 -c "print(f'{$volume * 0.002:.2f}')")

cat << EOF
Weekly Trading Fees: \$$fees
Monthly Infra: ~\$75
Monthly Data Savings: ~\$9,500

Net Position: Highly Positive
EOF
```

## 5. Present Results

```
# Cost Report

## Trading (This Week)
- Volume: $[X]
- Est. Fees: $[X]
- Fee Rate: 0.2%

## Infrastructure (Monthly)
| Item | Cost |
|------|------|
| VPS | $50 |
| GPU | $20-100 |
| Other | $5 |
| **Total** | **$75-155** |

## DIY Savings (Monthly)
- Data integrations: $9,000+
- Net benefit: Very positive

## ROI
- Break-even trades: [N]
- Current efficiency: [X]%
```

</process>

<success_criteria>
- [ ] Trading costs calculated
- [ ] Infra costs listed
- [ ] Savings quantified
- [ ] Net position clear
</success_criteria>
