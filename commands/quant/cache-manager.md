---
name: quant:cache-manager
description: Clear stale caches and manage cache lifecycle
argument-hint: [status|clear|refresh]
allowed-tools:
  - Bash
---

<objective>
Manage data caches - check freshness, clear stale data, force refresh.
</objective>

<process>

## 1. List Caches

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CACHE STATUS ==="
for cache in rl_engine/*_cache.json data/*_cache.json; do
  if [ -f "$cache" ]; then
    age_mins=$(( ($(date +%s) - $(stat -f %m "$cache")) / 60 ))
    size=$(ls -lh "$cache" | awk '{print $5}')
    echo "$cache: ${size}, ${age_mins}m old"
  fi
done 2>/dev/null
```

## 2. Clear Stale (>1hr)

```bash
cd ~/Developer/quant_master/quant_v4
echo "=== CLEARING STALE CACHES ==="
find . -name "*_cache.json" -mmin +60 -exec rm -v {} \; 2>/dev/null
echo "Done"
```

## 3. Force Refresh All

```bash
cd ~/Developer/quant_master/quant_v4
rm -f rl_engine/*_cache.json data/*_cache.json 2>/dev/null
echo "All caches cleared - will refresh on next access"
```

</process>

<success_criteria>
- [ ] Cache status shown
- [ ] Stale caches identified
- [ ] Clear executed if requested
</success_criteria>
