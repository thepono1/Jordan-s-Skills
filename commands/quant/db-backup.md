---
name: quant:db-backup
description: Backup trading databases
argument-hint: [all|trading|alpha|quick]
allowed-tools:
  - Bash
---

<objective>
Backup critical trading databases. Automate or forget.
</objective>

<context>
Databases to backup:
- efg_paper_trading/trading.db
- data/unified_alpha_v4.db
- data/strategy_validation.db
- data/circuit_breaker.db
- data/social_sentiment.db
</context>

<process>

## 1. Parse Scope

Default: all

Options:
- `all` - Backup all databases
- `trading` - Just trading.db
- `alpha` - Alpha engine db
- `quick` - Trading + positions only

## 2. Create Backup Directory

```bash
cd ~/Developer/quant_master/quant_v4
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "Backup directory: $BACKUP_DIR"
```

## 3. Execute Backup

### all
```bash
cd ~/Developer/quant_master/quant_v4
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Trading DB
sqlite3 efg_paper_trading/trading.db ".backup '$BACKUP_DIR/trading.db'" && echo "trading.db: OK" || echo "trading.db: FAILED"

# Alpha DB
sqlite3 data/unified_alpha_v4.db ".backup '$BACKUP_DIR/unified_alpha_v4.db'" 2>/dev/null && echo "unified_alpha_v4.db: OK" || echo "unified_alpha_v4.db: SKIPPED"

# Strategy Validation
sqlite3 data/strategy_validation.db ".backup '$BACKUP_DIR/strategy_validation.db'" 2>/dev/null && echo "strategy_validation.db: OK" || echo "strategy_validation.db: SKIPPED"

# Circuit Breaker
sqlite3 data/circuit_breaker.db ".backup '$BACKUP_DIR/circuit_breaker.db'" 2>/dev/null && echo "circuit_breaker.db: OK" || echo "circuit_breaker.db: SKIPPED"

# Sentiment
sqlite3 data/social_sentiment.db ".backup '$BACKUP_DIR/social_sentiment.db'" 2>/dev/null && echo "social_sentiment.db: OK" || echo "social_sentiment.db: SKIPPED"

# Summary
echo ""
echo "=== BACKUP COMPLETE ==="
ls -lh "$BACKUP_DIR"
du -sh "$BACKUP_DIR"
```

### trading
```bash
cd ~/Developer/quant_master/quant_v4
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
sqlite3 efg_paper_trading/trading.db ".backup '$BACKUP_DIR/trading.db'"
echo "Backed up to: $BACKUP_DIR/trading.db"
ls -lh "$BACKUP_DIR/trading.db"
```

## 4. Cleanup Old Backups

Keep last 7 days:
```bash
cd ~/Developer/quant_master/quant_v4
find backups -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null
echo "Cleaned up backups older than 7 days"
```

## 5. Present Results

```
# Database Backup

## Backed Up
| Database | Size | Status |
|----------|------|--------|
| trading.db | 2.1M | OK |
| unified_alpha_v4.db | 5.3M | OK |

## Location
[backup path]

## Total Size
[size]
```

</process>

<success_criteria>
- [ ] All requested DBs backed up
- [ ] Backup integrity verified
- [ ] Old backups cleaned
- [ ] Location reported
</success_criteria>
