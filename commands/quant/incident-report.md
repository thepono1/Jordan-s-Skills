---
name: quant:incident-report
description: Document trading incidents and issues
argument-hint: [create|list]
allowed-tools:
  - Bash
  - Write
---

<process>
```bash
cd ~/Developer/quant_master/quant_v4
mkdir -p data/incidents
echo "=== RECENT INCIDENTS ==="
ls -lt data/incidents/*.md 2>/dev/null | head -5 || echo "No incidents logged"
```

To create: Write to data/incidents/YYYYMMDD_title.md with details
</process>
