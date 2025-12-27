#!/usr/bin/env python3
import os
import json
from pathlib import Path

def generate_html(paper, base_name):
    title = paper['title']
    authors = paper['authors']
    date = paper['date'].replace('-', '/')  # YYYY/MM/DD
    abstract = paper['abstract']
    pdf_url = f"https://researcharchive.github.io/pdfs/{paper['pdf']}"
    venue = paper['venue']
    
    # Optional fields
    volume = paper.get('volume', '')
    issue = paper.get('issue', '')
    firstpage = paper.get('firstpage', '')
    lastpage = paper.get('lastpage', '')
    
    # Read bib if exists
    bib_content = ""
    bib_file = Path('bibs') / f"{base_name}.bib"
    if bib_file.exists():
        with open(bib_file, 'r', encoding='utf-8') as f:
            bib_content = f.read().strip()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  
  <meta name="citation_title" content="{title}">
"""
    for author in authors:
        html += f'  <meta name="citation_author" content="{author}">\n'
    
    html += f"""  <meta name="citation_publication_date" content="{date}">
  <meta name="citation_journal_title" content="{venue}">
"""
    if volume:
        html += f'  <meta name="citation_volume" content="{volume}">\n'
    if issue:
        html += f'  <meta name="citation_issue" content="{issue}">\n'
    if firstpage:
        html += f'  <meta name="citation_firstpage" content="{firstpage}">\n'
    if lastpage:
        html += f'  <meta name="citation_lastpage" content="{lastpage}">\n'
    
    html += f"""
  <meta name="citation_pdf_url" content="{pdf_url}">

  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f9f9f9;
    }}
    h1 {{
      color: #2c3e50;
      border-bottom: 2px solid #3498db;
      padding-bottom: 10px;
    }}
    h2 {{
      color: #34495e;
    }}
    h3 {{
      color: #3498db;
      margin-top: 30px;
    }}
    .download-btn {{
      display: inline-block;
      background-color: #3498db;
      color: white;
      padding: 10px 20px;
      text-decoration: none;
      border-radius: 5px;
      margin-top: 20px;
      transition: background-color 0.3s;
    }}
    .download-btn:hover {{
      background-color: #2980b9;
    }}
    .bib-block {{
      background-color: #ecf0f1;
      border: 1px solid #bdc3c7;
      border-radius: 5px;
      padding: 15px;
      margin-top: 20px;
      position: relative;
    }}
    .bib-content {{
      font-family: 'Courier New', monospace;
      white-space: pre-wrap;
      margin: 0;
    }}
    .copy-btn {{
      position: absolute;
      top: 10px;
      right: 10px;
      background-color: #e74c3c;
      color: white;
      border: none;
      padding: 5px 10px;
      border-radius: 3px;
      cursor: pointer;
      font-size: 12px;
    }}
    .copy-btn:hover {{
      background-color: #c0392b;
    }}
    .copy-hint {{
      display: none;
      position: absolute;
      top: 40px;
      right: 10px;
      background-color: #27ae60;
      color: white;
      padding: 5px 10px;
      border-radius: 3px;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <h2>Authors: {', '.join(authors)}</h2>
  <h3>Abstract</h3>
  <p>
    {abstract}
  </p>
  
  <a href="../pdfs/{paper['pdf']}" class="download-btn">Download Full PDF</a>
"""
    if bib_content:
        html += f"""
  <h3>Bibliographic Reference</h3>
  <div class="bib-block">
    <button class="copy-btn" onclick="copyBib()">Copy</button>
    <div class="copy-hint" id="copyHint">Copied successfully!</div>
    <pre class="bib-content">{bib_content}</pre>
  </div>
"""
    
    html += """
  <script>
    function copyBib() {
      const bibText = document.querySelector('.bib-content').textContent;
      navigator.clipboard.writeText(bibText).then(() => {
        const hint = document.getElementById('copyHint');
        hint.style.display = 'block';
        setTimeout(() => {
          hint.style.display = 'none';
        }, 2000);
      });
    }
  </script>
</body>
</html>
"""
    return html

def main():
    data_file = Path('_data/papers.json')
    papers_dir = Path('papers')

    # Load existing papers
    if data_file.exists():
        with open(data_file, 'r') as f:
            papers = json.load(f)
    else:
        papers = []

    # Generate HTML pages
    for paper in papers:
        base_name = Path(paper['pdf']).stem
        html_content = generate_html(paper, base_name)
        html_file = papers_dir / f"{base_name}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

if __name__ == '__main__':
    main()