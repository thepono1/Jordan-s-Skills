---
name: quant:system-snapshot
description: Complete system state snapshot for debugging
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== SYSTEM SNAPSHOT $(date) ==="

echo ""
echo "--- Local Processes ---"
ps aux | grep -E "python|adaptive_beast|l2_system" | grep -v grep | awk '{print $2, $11}' | head -10

echo ""
echo "--- PID Files ---"
ls -la .*.pid 2>/dev/null || echo "No PID files"

echo ""
echo "--- Database Status ---"
ls -lh efg_paper_trading/*.db efg_paper_trading/state/*.db 2>/dev/null

echo ""
echo "--- Open Positions ---"
sqlite3 efg_paper_trading/trading.db "SELECT COUNT(*) || ' positions' FROM positions WHERE status='OPEN'"

echo ""
echo "--- Recent Trades ---"
sqlite3 efg_paper_trading/trading.db "SELECT COUNT(*) || ' trades today' FROM trades WHERE DATE(timestamp)=DATE('now')"

echo ""
echo "--- L2 Data ---"
sqlite3 efg_paper_trading/state/l2_data.db "SELECT symbol, COUNT(*) as snapshots FROM order_book_snapshots WHERE timestamp > datetime('now', '-5 minutes') GROUP BY symbol"

echo ""
echo "--- VPS Status ---"
ssh quantpod "systemctl is-active unified-alpha-mm enhanced-trader" 2>/dev/null || echo "VPS unreachable"
```
</process>
