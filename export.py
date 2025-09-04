"""
Export Module - Enhanced with Professional Branding
Handles exporting search results to PDF and CSV formats
Now with company logos, customer info, and dad jokes! 😂
"""
Export Module
Handles exporting search results to PDF and CSV formats
"""

import csv
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from PIL import Image as PILImage

# Import our new modules
try:
    from branding_manager import get_branding_manager
    from dad_jokes import get_export_message
except ImportError:
    # Fallback if modules aren't available
    def get_branding_manager():
        return None
    def get_export_message():
        return "Export complete! 📄"

class ResultExporter:
    def __init__(self):
        """Initialize the enhanced exporter with branding support"""
        self.styles = getSampleStyleSheet()
        self.branding_manager = get_branding_manager()
        
        # Get branding colors if available
        primary_color = colors.darkblue
        secondary_color = colors.darkgreen
        
        if self.branding_manager:
            branding_settings = self.branding_manager.get_branding_settings()
            try:
                primary_color = colors.Color(*self.hex_to_rgb(branding_settings.get('primary_color', '#0000AA')))
                secondary_color = colors.Color(*self.hex_to_rgb(branding_settings.get('secondary_color', '#00AA00')))
            except:
                pass  # Use defaults if color parsing fails
        
        # Create custom styles with branding
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=primary_color,
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=primary_color,
            spaceBefore=20,
            spaceAfter=10
        )
        
        self.company_style = ParagraphStyle(
            'CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=secondary_color,
            spaceBefore=6,
            spaceAfter=6,
            alignment=TA_RIGHT
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
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple for ReportLab"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))
    
    def export_to_pdf(self, results, domain, filename=None, customer_id=None):
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
        
        # Create PDF document with enhanced margins for header
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1.5*inch, bottomMargin=1*inch)
        story = []
        
        # Add company header with logo if available
        story.extend(self._create_company_header(customer_id))
        
        # Add title with dad joke
        title_text = f"🎯 Google Dorking Intelligence Report<br/>{domain}"
        story.append(Paragraph(title_text, self.title_style))
        
        # Add a dad joke for fun
        try:
            dad_joke = get_export_message()
            joke_style = ParagraphStyle(
                'JokeStyle',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )
            story.append(Paragraph(f"💡 {dad_joke}", joke_style))
            story.append(Spacer(1, 10))
        except:
            pass  # Skip jokes if module not available
        
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
        
        # Add professional footer
        story.extend(self._create_professional_footer())
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _create_company_header(self, customer_id=None):
        """Create professional header with company and customer logos"""
        header_elements = []
        
        if not self.branding_manager:
            return header_elements
        
        try:
            # Get company info
            company_info = self.branding_manager.get_company_info()
            
            # Create header table data
            header_data = []
            
            # Company logo and info
            company_cell_content = []
            
            # Add company logo if available
            company_logo_path = company_info.get('logo_path')
            if company_logo_path and os.path.exists(company_logo_path):
                try:
                    # Resize company logo
                    img = PILImage.open(company_logo_path)
                    img.thumbnail((100, 60), PILImage.Resampling.LANCZOS)
                    temp_logo_path = f"temp_company_logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    img.save(temp_logo_path)
                    
                    company_logo = Image(temp_logo_path, width=80, height=48)
                    company_cell_content.append(company_logo)
                    
                    # Clean up temp file after use
                    try:
                        os.remove(temp_logo_path)
                    except:
                        pass
                except Exception as e:
                    print(f"Error processing company logo: {e}")
            
            # Company info text
            company_text = f"""
            <b>{company_info.get('name', 'Your Company')}</b><br/>
            {company_info.get('address', '').replace(chr(10), '<br/>')}<br/>
            📞 {company_info.get('phone', '')}<br/>
            ✉️ {company_info.get('email', '')}<br/>
            🌐 {company_info.get('website', '')}
            """
            company_info_para = Paragraph(company_text, self.company_style)
            
            # Customer info if provided
            customer_cell_content = []
            if customer_id:
                customer = self.branding_manager.get_customer(customer_id)
                if customer:
                    # Customer logo if available
                    customer_logo_path = customer.get('logo_path')
                    if customer_logo_path and os.path.exists(customer_logo_path):
                        try:
                            img = PILImage.open(customer_logo_path)
                            img.thumbnail((80, 48), PILImage.Resampling.LANCZOS)
                            temp_customer_logo_path = f"temp_customer_logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            img.save(temp_customer_logo_path)
                            
                            customer_logo = Image(temp_customer_logo_path, width=60, height=36)
                            customer_cell_content.append(customer_logo)
                            
                            # Clean up temp file
                            try:
                                os.remove(temp_customer_logo_path)
                            except:
                                pass
                        except Exception as e:
                            print(f"Error processing customer logo: {e}")
                    
                    # Customer info text
                    customer_text = f"""
                    <b>Prepared for:</b><br/>
                    <b>{customer.get('name', 'Customer')}</b><br/>
                    {customer.get('company', '')}<br/>
                    {customer.get('address', '').replace(chr(10), '<br/>')}
                    """
                    customer_info_para = Paragraph(customer_text, self.company_style)
                    customer_cell_content.append(customer_info_para)
            
            # Create header table
            if customer_cell_content:
                header_table = Table([[company_info_para, customer_cell_content]], 
                                   colWidths=[3*inch, 2.5*inch])
            else:
                header_table = Table([[company_info_para, ""]], 
                                   colWidths=[4*inch, 1.5*inch])
            
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey)
            ]))
            
            header_elements.append(header_table)
            header_elements.append(Spacer(1, 20))
            
        except Exception as e:
            print(f"Error creating company header: {e}")
        
        return header_elements
    
    def _create_professional_footer(self):
        """Create professional footer with timestamp and branding"""
        footer_elements = []
        
        try:
            footer_elements.append(PageBreak())
            
            # Professional closing
            closing_text = """
            <br/><br/>
            <b>📋 REPORT SUMMARY</b><br/>
            This intelligence report was generated by MissDorking™ Professional Suite.<br/>
            Report contains sensitive security information - handle with care.<br/><br/>
            
            <b>🔒 CONFIDENTIALITY NOTICE</b><br/>
            This report contains confidential and proprietary information. 
            Distribution should be limited to authorized personnel only.<br/><br/>
            
            <b>⚡ POWERED BY MISSDORKING™</b><br/>
            Advanced Google Dorking & Intelligence Platform<br/>
            Making cybersecurity fabulous since 2024! 💋<br/><br/>
            
            Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
            Report ID: MissDorking-{datetime.now().strftime('%Y%m%d-%H%M%S')}
            """
            
            footer_style = ParagraphStyle(
                'FooterStyle',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                spaceBefore=20,
                alignment=TA_CENTER
            )
            
            footer_elements.append(Paragraph(closing_text, footer_style))
            
        except Exception as e:
            print(f"Error creating footer: {e}")
        
        return footer_elements
    
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
