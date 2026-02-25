---
name: terminal
description: Control Jordan's Mac - run terminal commands, control mouse/keyboard, take screenshots, system control. Use when asked to run something on the Mac or control the computer.
---

# Terminal Control for Kaleo

Execute commands on Jordan's Mac via `computer_control.py`.

## Usage

```
/terminal <command or description>
```

## Script Location

```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py <command> [args]
```

## Quick Reference

### Run Shell Commands
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py shell "ls -la"
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py shell "git status"
```

### Mouse Control
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py move 500 300
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py click 500 300
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py click 500 300 right
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py double_click 500 300
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py drag 100 100 500 500
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py position
```

### Keyboard Control
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py type "Hello World"
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py key enter
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py key c command   # Cmd+C
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py hotkey command shift s
```

### Screenshots
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py screenshot /tmp/screen.png
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py screenshot_base64
```

### Window Control
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py focus "Google Chrome"
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py active_window
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py list_windows
```

### System Power
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py restart
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py shutdown
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py sleep
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py wake
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py lock
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py wol  # Wake-on-LAN
```

### System Settings
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py volume 50
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py mute
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py unmute
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py dark_mode on
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py brightness 0.8
```

### Apps
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py open_app Safari
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py quit Safari
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py open https://google.com
```

### Clipboard
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py clipboard          # get
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py clipboard "text"   # set
```

### Notifications
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py notify "Title" "Message"
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py say "Hello Jordan"
```

### System Info
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py battery
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py cpu
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py disk
```

## Process

When user says `/terminal <request>`:

1. Parse what they want to do
2. Map to the appropriate computer_control.py command
3. Execute via Bash tool
4. Return the result

## Examples

**User**: `/terminal take a screenshot`
**Action**: `python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py screenshot /tmp/screen.png`

**User**: `/terminal click on the search bar at 500, 200`
**Action**: `python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py click 500 200`

**User**: `/terminal type hello world`
**Action**: `python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py type "hello world"`

**User**: `/terminal restart the mac`
**Action**: `python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py restart`

**User**: `/terminal run git status`
**Action**: `python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py shell "git status"`

**User**: `/terminal open chrome and go to google`
**Action**:
```bash
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py open_app "Google Chrome"
python3 ~/Developer/quant_master/quant_v4/kaleo/computer_control.py shell "open https://google.com"
```

## No Restrictions

This skill executes exactly what is requested. No confirmations, no safety prompts.
