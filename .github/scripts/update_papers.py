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
    
    html = f"""<!DOCTYPE html>
<html>
<head>
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

</head>
<body>
  <h1>{title}</h1>
  <h2>Authors: {', '.join(authors)}</h2>
  <h3>Abstract</h3>
  <p>
    {abstract}
  </p>
  
  <p>
    <a href="../pdfs/{paper['pdf']}">Download Full PDF</a>
  </p>
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