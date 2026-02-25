---
name: quant:data-export
description: Export trading data to CSV
argument-hint: [trades|positions|snapshots]
allowed-tools:
  - Bash
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
echo "=== DATA EXPORT OPTIONS ==="
echo "Export trades:"
echo "  sqlite3 -header -csv efg_paper_trading/trading.db 'SELECT * FROM trades' > trades.csv"
echo ""
echo "Export positions:"
echo "  sqlite3 -header -csv efg_paper_trading/trading.db 'SELECT * FROM positions' > positions.csv"
echo ""
echo "Export L2 snapshots (last hour):"
echo "  sqlite3 -header -csv efg_paper_trading/state/l2_data.db \"SELECT * FROM order_book_snapshots WHERE timestamp > datetime('now', '-1 hour')\" > l2_snapshots.csv"
```
</process>
