from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from datetime import datetime
import qrcode
import io
import base64
from PIL import Image

class CertificateGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin = 0.5 * inch
    
    def generate_completion_certificate(self, user_name, category_name, completion_date, certificate_id):
        """Generate a completion certificate PDF"""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Colors
        primary_color = HexColor('#667eea')
        secondary_color = HexColor('#764ba2')
        text_color = HexColor('#333333')
        
        # Background gradient effect (simplified)
        c.setFillColor(HexColor('#f8f9fa'))
        c.rect(0, 0, self.page_width, self.page_height, fill=1)
        
        # Header
        c.setFillColor(primary_color)
        c.rect(0, self.page_height - 2*inch, self.page_width, 2*inch, fill=1)
        
        # Title
        c.setFillColor(HexColor('#ffffff'))
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredText(self.page_width/2, self.page_height - 1.2*inch, "CERTIFICATE")
        c.setFont("Helvetica", 18)
        c.drawCentredText(self.page_width/2, self.page_height - 1.6*inch, "OF COMPLETION")
        
        # Main content
        c.setFillColor(text_color)
        c.setFont("Helvetica", 16)
        c.drawCentredText(self.page_width/2, self.page_height - 3*inch, "This is to certify that")
        
        # User name
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(primary_color)
        c.drawCentredText(self.page_width/2, self.page_height - 3.8*inch, user_name.upper())
        
        # Course details
        c.setFillColor(text_color)
        c.setFont("Helvetica", 16)
        c.drawCentredText(self.page_width/2, self.page_height - 4.6*inch, "has successfully completed the")
        
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(secondary_color)
        c.drawCentredText(self.page_width/2, self.page_height - 5.2*inch, f"{category_name} Course")
        
        # Date and signature area
        c.setFillColor(text_color)
        c.setFont("Helvetica", 14)
        c.drawCentredText(self.page_width/2, self.page_height - 6.5*inch, f"Completed on: {completion_date}")
        
        # Generate QR code for verification
        qr_data = f"https://microlearn.com/verify/{certificate_id}"
        qr = qrcode.QRCode(version=1, box_size=3, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        # Add QR code to certificate
        c.drawImage(qr_buffer, self.page_width - 2*inch, 0.5*inch, width=1.5*inch, height=1.5*inch)
        
        # Certificate ID
        c.setFont("Helvetica", 10)
        c.drawString(self.margin, 0.3*inch, f"Certificate ID: {certificate_id}")
        
        # Footer
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredText(self.page_width/2, 1.5*inch, "MicroLearn Coach")
        c.setFont("Helvetica", 10)
        c.drawCentredText(self.page_width/2, 1.2*inch, "Empowering learners worldwide")
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def generate_skill_badge(self, user_name, skill_name, level):
        """Generate a digital skill badge"""
        # This would create a smaller badge image
        # For now, returning a simple text-based badge
        badge_data = {
            'user': user_name,
            'skill': skill_name,
            'level': level,
            'issued': datetime.now().isoformat(),
            'issuer': 'MicroLearn Coach'
        }
        return badge_data
