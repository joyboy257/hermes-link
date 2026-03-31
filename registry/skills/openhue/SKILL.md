---
name: openhue
description: Control Philips Hue lights, rooms, and scenes from the terminal. Brightness, color, color temperature, and scene activation.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: [HUE_BRIDGE_IP, HUE_API_KEY]
metadata:
  hermes:
    tags: [smart-home, hue, lights, iot, automation]
---

# openhue

CLI for Philips Hue bridges. No app required.

## Setup

1. Find your Hue Bridge IP: check the Hue app or run `nmap -p 80 192.168.1.0/24`
2. Press the Bridge button, then create an API key:

```bash
curl -X POST -d '{"devicetype":"hermes#openhue"}' http://HUE_BRIDGE_IP/api
```

3. Export:
```bash
export HUE_BRIDGE_IP="192.168.1.x"
export HUE_API_KEY="your-api-key"
```

## Install

```bash
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue
```

## Usage

```bash
openhue lights                    # List all lights
openhue light 1 on              # Turn on
openhue light 1 off             # Turn off
openhue light 1 brightness 50   # Set brightness
openhue light 1 color ff0000    # Set color (hex)
openhue light 1 temp 4000       # Color temperature (Kelvin)
openhue scene movie              # Activate scene
openhue room living room        # Control entire room
```

## Examples

Morning routine:
```bash
openhue light 1-6 on && openhue light 1-6 brightness 80 && openhue light 1-6 temp 5000
```

Movie mode:
```bash
openhue scene movie
```
