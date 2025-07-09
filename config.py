import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # Database Configuration
    # MYSQL_HOST = os.getenv('DB_HOST' )
    # MYSQL_USER = os.getenv('DB_USER')
    # MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
    # MYSQL_DATABASE = os.getenv('DB_NAME')
    DATABASE_URL = os.getenv('DATABASE_POS_URL', 'sqlite:///default.db')
    
    
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI= DATABASE_URL.replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Twilio Configuration (WhatsApp)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
    
    # Payment Configuration
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Lesson Configuration
    DAILY_LESSON_TIME = os.getenv('DAILY_LESSON_TIME', '09:00')
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    
    # Subscription Plans
    SUBSCRIPTION_PLANS = {
        'daily': {
            'name': 'Daily Plan',
            'price': 2.99,
            'duration_days': 7,
            'features': ['Daily lessons', 'Progress tracking', 'Basic certificates']
        },
        'weekly': {
            'name': 'Weekly Plan', 
            'price': 9.99,
            'duration_days': 30,
            'features': ['All daily features', 'Advanced quizzes', 'Priority support', 'Skill badges']
        },
        'premium': {
            'name': 'Premium Plan',
            'price': 29.99,
            'duration_days': 30,
            'features': ['Everything included', '1-on-1 coaching', 'Industry certificates', 'Job placement']
        }
    }

print("Config loaded successfully.")
print(f"Database URL: {Config.DATABASE_URL}")