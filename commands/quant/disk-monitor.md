---
name: quant:disk-monitor
description: Monitor disk space and prevent disk full issues
allowed-tools:
  - Bash
---

<objective>
Prevent disk full situations. Monitor space usage and identify large files.
</objective>

<process>

## 1. Check Disk Space

```bash
echo "=== DISK SPACE ==="
df -h / /Users 2>/dev/null | head -5
```

## 2. Check Quant Directory Size

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== QUANT DIRECTORY SIZE ==="
du -sh . 2>/dev/null
echo ""
echo "Top subdirectories:"
du -sh */ 2>/dev/null | sort -rh | head -10
```

## 3. Find Large Files

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== LARGE FILES (>100MB) ==="
find . -type f -size +100M 2>/dev/null | head -10 | while read f; do
  size=$(ls -lh "$f" | awk '{print $5}')
  echo "$size $f"
done
```

## 4. Database Sizes

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== DATABASE SIZES ==="
find . -name "*.db" -type f 2>/dev/null | while read db; do
  size=$(ls -lh "$db" 2>/dev/null | awk '{print $5}')
  echo "$size $db"
done | sort -rh | head -10
```

## 5. Log File Sizes

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== LOG FILES ==="
find . -name "*.log" -type f 2>/dev/null | while read log; do
  size=$(ls -lh "$log" 2>/dev/null | awk '{print $5}')
  echo "$size $log"
done | sort -rh | head -10
```

## 6. Cleanup Recommendations

```bash
cd ~/Developer/quant_master/quant_v4
echo ""
echo "=== CLEANUP RECOMMENDATIONS ==="

# Old backups
old_backups=$(find backups -type d -mtime +7 2>/dev/null | wc -l)
echo "Old backups (>7d): $old_backups directories"

# Large logs
large_logs=$(find . -name "*.log" -size +50M 2>/dev/null | wc -l)
echo "Large logs (>50MB): $large_logs files"

# Cache files
cache_size=$(du -sh data/*cache* 2>/dev/null | awk '{sum+=$1} END {print sum}')
echo "Cache files: ${cache_size:-0}KB total"
```

## 7. Present Results

```
# Disk Monitor

## Space Usage
- Root: [X]% used
- Available: [X]GB

## Quant Directory
- Total Size: [X]GB
- Databases: [X]MB
- Logs: [X]MB
- Backups: [X]MB

## Status
- [OK/WARNING/CRITICAL]

## Cleanup Options
- Old backups: [N] (safe to delete)
- Large logs: [N] (can truncate)
- Cache files: [X]MB
```

</process>

<success_criteria>
- [ ] Space usage checked
- [ ] Large files identified
- [ ] Cleanup options provided
- [ ] Status determined
</success_criteria>
