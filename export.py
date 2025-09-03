"""
Export Module
Handles exporting search results to PDF and CSV formats
"""

import csv
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

class ResultExporter:
    def __init__(self):
        """Initialize the exporter"""
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=1,  # Center alignment
            spaceAfter=30
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceBefore=20,
            spaceAfter=10
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=6,
            spaceAfter=6
        )
    
    def export_to_csv(self, results, domain, filename=None):
        """
        Export search results to CSV format
        
        Args:
            results (dict): Dictionary with categories and search results
            domain (str): Target domain name
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the created CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dorking_results_{domain}_{timestamp}.csv"
        
        # Ensure filename ends with .csv
        if not filename.endswith('.csv'):
            filename += '.csv'
            
        filepath = os.path.abspath(filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Category', 'Query', 'Title', 'URL', 'Snippet', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for category, queries in results.items():
                for query, search_results in queries.items():
                    if search_results:
                        for result in search_results:
                            # Safely convert all values to strings
                            title_val = result.get('title', 'N/A')
                            url_val = result.get('url', 'N/A')
                            snippet_val = result.get('snippet', 'N/A')
                            
                            writer.writerow({
                                'Category': str(category) if category is not None else 'N/A',
                                'Query': str(query) if query is not None else 'N/A',
                                'Title': str(title_val) if title_val is not None else 'N/A',
                                'URL': str(url_val) if url_val is not None else 'N/A',
                                'Snippet': str(snippet_val) if snippet_val is not None else 'N/A',
                                'Timestamp': timestamp
                            })
                    else:
                        # Include queries with no results
                        writer.writerow({
                            'Category': category,
                            'Query': query,
                            'Title': 'No results found',
                            'URL': 'N/A',
                            'Snippet': 'N/A',
                            'Timestamp': timestamp
                        })
        
        return filepath
    
    def export_to_pdf(self, results, domain, filename=None):
        """
        Export search results to PDF format
        
        Args:
            results (dict): Dictionary with categories and search results
            domain (str): Target domain name
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the created PDF file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dorking_report_{domain}_{timestamp}.pdf"
        
        # Ensure filename ends with .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'
            
        filepath = os.path.abspath(filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1*inch)
        story = []
        
        # Add title
        title_text = f"Google Dorking Report - {domain}"
        story.append(Paragraph(title_text, self.title_style))
        
        # Add timestamp
        timestamp_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Paragraph(timestamp_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # Add summary
        try:
            total_queries = sum(len(queries) for queries in results.values() if isinstance(queries, dict))
            total_results = sum(
                sum(len(search_results) if hasattr(search_results, '__len__') else 0 
                    for search_results in queries.values()) 
                for queries in results.values() if isinstance(queries, dict)
            )
        except Exception as e:
            # Fallback if summary calculation fails
            total_queries = 0
            total_results = 0
        
        summary_text = f"""
        <b>Summary:</b><br/>
        • Total categories: {len(results)}<br/>
        • Total queries executed: {total_queries}<br/>
        • Total results found: {total_results}<br/>
        """
        story.append(Paragraph(summary_text, self.normal_style))
        story.append(Spacer(1, 20))
        
        # Add results by category
        for category, queries in results.items():
            # Category heading
            story.append(Paragraph(f"{category}", self.heading_style))
            
            category_results = 0
            for query, search_results in queries.items():
                if search_results:
                    category_results += len(search_results)
                    
                    # Query subheading
                    query_text = f"<b>Query:</b> {query} ({len(search_results)} results)"
                    story.append(Paragraph(query_text, self.normal_style))
                    
                    # Results table
                    table_data = [['Title', 'URL']]
                    for result in search_results[:10]:  # Limit to first 10 results per query
                        # Ensure title and url are strings and handle truncation safely
                        title_raw = result.get('title', 'N/A')
                        title_str = str(title_raw) if title_raw is not None else 'N/A'
                        title = title_str[:80] + ('...' if len(title_str) > 80 else '')
                        
                        url_raw = result.get('url', 'N/A')
                        url_str = str(url_raw) if url_raw is not None else 'N/A'
                        url = url_str[:60] + ('...' if len(url_str) > 60 else '')
                        
                        table_data.append([title, url])
                    
                    if table_data[1:]:  # If there are results
                        table = Table(table_data, colWidths=[3*inch, 2.5*inch])
                        table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),
                            ('FONTSIZE', (0, 1), (-1, -1), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ]))
                        story.append(table)
                        
                        if len(search_results) > 10:
                            more_text = f"... and {len(search_results) - 10} more results"
                            story.append(Paragraph(more_text, self.normal_style))
                    
                    story.append(Spacer(1, 10))
                
                else:
                    # No results for this query
                    query_text = f"<b>Query:</b> {query} (0 results)"
                    story.append(Paragraph(query_text, self.normal_style))
                    story.append(Paragraph("No results found", self.normal_style))
                    story.append(Spacer(1, 10))
            
            # Category summary
            category_summary = f"<i>Total results in {category}: {category_results}</i>"
            story.append(Paragraph(category_summary, self.normal_style))
            story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def export_raw_json(self, results, domain, filename=None):
        """
        Export raw results to JSON format for debugging
        
        Args:
            results (dict): Dictionary with categories and search results
            domain (str): Target domain name
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to the created JSON file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"raw_results_{domain}_{timestamp}.json"
        
        # Ensure filename ends with .json
        if not filename.endswith('.json'):
            filename += '.json'
            
        filepath = os.path.abspath(filename)
        
        export_data = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
        
        return filepath
