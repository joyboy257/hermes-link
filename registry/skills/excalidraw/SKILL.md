---
name: excalidraw
description: Create hand-drawn style diagrams programmatically. Flowcharts, architecture diagrams, wireframes, and sketches in the Excalidraw JSON format.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: []
metadata:
  hermes:
    tags: [excalidraw, diagrams, architecture, flowchart, wireframe]
---

# excalidraw

Hand-drawn style diagrams from the terminal. No design skills needed.

## Install

```bash
pip install excalidraw-cli
# or
npm install -g @excalidraw/excalidraw-cli
```

## Quick Start

```bash
# Initialize a diagram
excalidraw init my-diagram
cd my-diagram
```

## Creating Diagrams

Excalidraw diagrams are JSON files with `.excalidraw` extension:

```json
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {
      "id": "rect-1",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 100,
      "fillColor": "#fff",
      "strokeColor": "#333"
    },
    {
      "id": "arrow-1",
      "type": "arrow",
      "startX": 300,
      "startY": 150,
      "endX": 450,
      "endY": 150
    }
  ]
}
```

## Python Helper

```python
import json

def create_rectangle(id, x, y, w, h, label="", fill="#fff", stroke="#333"):
    return {
        "id": id, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "label": {"text": label},
        "fillColor": fill, "strokeColor": stroke
    }

def create_arrow(id, x1, y1, x2, y2):
    return {
        "id": id, "type": "arrow",
        "startX": x1, "startY": y1, "endX": x2, "endY": y2,
        "strokeColor": "#333"
    }

elements = [
    create_rectangle("server", 100, 100, 120, 60, "Server"),
    create_rectangle("db", 100, 200, 120, 60, "Database"),
    create_arrow("arrow1", 160, 160, 160, 200),
]
```

## Opening Diagrams

Open `.excalidraw` files at [excalidraw.com](https://excalidraw.com) directly — paste the JSON or import the file.

## Architecture Diagram Example

```bash
cat > api-architecture.excalidraw << 'EOF'
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {"id": "lb", "type": "rectangle", "x": 100, "y": 50, "width": 100, "height": 50, "label": {"text": "Load Balancer"}, "fillColor": "#fbe4ff", "strokeColor": "#9333ea"},
    {"id": "api1", "type": "rectangle", "x": 50, "y": 150, "width": 80, "height": 50, "label": {"text": "API 1"}, "fillColor": "#dbeafe", "strokeColor": "#2563eb"},
    {"id": "api2", "type": "rectangle", "x": 170, "y": 150, "width": 80, "height": 50, "label": {"text": "API 2"}, "fillColor": "#dbeafe", "strokeColor": "#2563eb"},
    {"id": "db", "type": "rectangle", "x": 100, "y": 250, "width": 120, "height": 50, "label": {"text": "PostgreSQL"}, "fillColor": "#dcfce7", "strokeColor": "#16a34a"}
  ]
}
EOF
```
