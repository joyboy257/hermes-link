---
name: arxiv
description: Search and download academic papers from arXiv. Find research by keyword, author, or subject area. Free, no account needed.
version: 1.0.0
author: joyboy257
license: MIT
prerequisites:
  env_vars: []
metadata:
  hermes:
    tags: [arxiv, academic, papers, research, ml, cs]
---

# arxiv

Access the arXiv preprint server directly from the terminal. No login, no paywall.

## Usage

```bash
# Search papers
curl "https://export.arxiv.org/api/query?search_query=all:transformer+language+model&start=0&max_results=5&sortBy=relevance"

# Or use arxiv-cli (Node.js)
npx arxiv-cli search "diffusion models image generation"

# Download PDF
curl -L "https://arxiv.org/pdf/2301.00001.pdf" -o paper.pdf
```

## Finding Paper IDs

Search at [arxiv.org](https://arxiv.org) first if you don't know the paper ID.
Paper IDs look like: `2301.00001` or `cs/0704/0704001`

## Direct API Examples

```bash
# By keyword
curl "https://export.arxiv.org/api/query?search_query=ti:language+model&max_results=10"

# By author
curl "https://export.arxiv.org/api/query?search_query=au:hovland"

# By category (cs.AI, cs.LG, cs.CL, etc.)
curl "https://export.arxiv.org/api/query?search_query=cat:cs.LG&max_results=20&sortBy=submittedDate"

# Full-text search
curl "https://export.arxiv.org/api/query?search_query=all:+reasoning+chain+thought"
```

## Get Abstract Only

```bash
curl "https://export.arxiv.org/abs/2301.00001" | head -30
```

## Download Paper

```bash
curl -L "https://arxiv.org/e-print/2301.00001" -o paper.tar.gz
# or PDF
curl -L "https://arxiv.org/pdf/2301.00001.pdf" -o paper.pdf
```

## Python Script for Bulk Downloads

```python
import urllib.request
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=10):
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    data = urllib.request.urlopen(url).read()
    root = ET.fromstring(data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    for entry in root.findall('atom:entry', ns):
        print(entry.find('atom:title', ns).text.strip())
        print(entry.find('atom:id', ns).text)
        print()
```
