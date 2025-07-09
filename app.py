from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import schedule
import time
import threading
from twilio.rest import Client
from config import Config
from flask_moment import Moment

app = Flask(__name__)
moment = Moment(app)
# app.config['SECRET_KEY'] = 'your-secret-key-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/dbname'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)

db = SQLAlchemy(app)

# Twilio Configuration (for WhatsApp)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

@app.before_request
def before_request():
    try:
        db.engine.connect()
    except Exception as e:
        return "Database connection failed", 500

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    preferred_language = db.Column(db.String(10), default='en')
    subscription_status = db.Column(db.Enum('free', 'daily', 'weekly', 'premium'), default='free')
    subscription_start = db.Column(db.Date)
    subscription_end = db.Column(db.Date)
    current_streak = db.Column(db.Integer, default=0)
    total_lessons_completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.Enum('beginner', 'intermediate', 'advanced'), default='beginner')
    estimated_duration = db.Column(db.Integer, default=5)
    lesson_order = db.Column(db.Integer)
    media_url = db.Column(db.String(500))
    quiz_questions = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    category = db.relationship('Category', backref='lessons')

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    quiz_score = db.Column(db.Integer)
    time_spent = db.Column(db.Integer)
    
    user = db.relationship('User', backref='progress')
    lesson = db.relationship('Lesson', backref='user_progress')

class MessageLog(db.Model):
    __tablename__ = 'message_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message_type = db.Column(db.Enum('incoming', 'outgoing'))
    message_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# WhatsApp Bot Logic
class WhatsAppBot:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.user_states = {}  # Track conversation states
    
    def send_message(self, to_number, message):
        """Send WhatsApp message to user"""
        try:
            message = self.client.messages.create(
                body=message,
                from_=TWILIO_WHATSAPP_NUMBER,
                to=f'whatsapp:{to_number}'
            )
            
            # Log outgoing message
            user = User.query.filter_by(phone_number=to_number).first()
            if user:
                log = MessageLog(
                    user_id=user.id,
                    message_type='outgoing',
                    message_content=message
                )
                db.session.add(log)
                db.session.commit()
            
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def process_incoming_message(self, from_number, message_body):
        """Process incoming WhatsApp messages"""
        # Clean phone number
        phone_number = from_number.replace('whatsapp:', '')
        
        # Get or create user
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            user = User(phone_number=phone_number)
            db.session.add(user)
            db.session.commit()
            
            # Send welcome message
            welcome_msg = """🎓 Welcome to MicroLearn Coach!
            
I'm your personal learning assistant. I'll send you 5-minute daily lessons to help you grow your skills.

Available categories:
🇬🇧 English Language
💻 Digital Skills  
🔧 Vocational Training
💼 Business Skills
💰 Financial Literacy

Reply with:
• START - Begin your learning journey
• MENU - See all options
• HELP - Get assistance"""
            
            self.send_message(phone_number, welcome_msg)
            return
        
        # Log incoming message
        log = MessageLog(
            user_id=user.id,
            message_type='incoming',
            message_content=message_body
        )
        db.session.add(log)
        db.session.commit()
        
        # Process commands
        message_body = message_body.upper().strip()
        
        if message_body == 'START':
            self.handle_start_command(user)
        elif message_body == 'MENU':
            self.handle_menu_command(user)
        elif message_body == 'HELP':
            self.handle_help_command(user)
        elif message_body == 'LESSON':
            self.send_daily_lesson(user)
        elif message_body == 'PROGRESS':
            self.show_progress(user)
        elif message_body == 'SUBSCRIBE':
            self.show_subscription_options(user)
        elif message_body.startswith('CATEGORY'):
            category_id = message_body.split()[-1] if len(message_body.split()) > 1 else None
            self.show_category_lessons(user, category_id)
        else:
            self.handle_unknown_command(user)
    
    def handle_start_command(self, user):
        """Handle START command"""
        categories = Category.query.all()
        message = "🚀 Let's start learning! Choose a category:\n\n"
        
        for cat in categories:
            message += f"{cat.icon} {cat.name} - Reply 'CATEGORY {cat.id}'\n"
        
        message += "\n💡 Or reply 'LESSON' for today's recommended lesson!"
        self.send_message(user.phone_number, message)
    
    def handle_menu_command(self, user):
        """Handle MENU command"""
        menu_msg = """📚 MicroLearn Coach Menu:

🎯 LESSON - Get today's lesson
📊 PROGRESS - View your progress  
🏆 SUBSCRIBE - Upgrade your plan
📋 CATEGORIES - Browse all topics
❓ HELP - Get assistance

What would you like to do?"""
        
        self.send_message(user.phone_number, menu_msg)
    
    def handle_help_command(self, user):
        """Handle HELP command"""
        help_msg = """🆘 Need Help?

Commands you can use:
• START - Begin learning
• LESSON - Get daily lesson
• PROGRESS - Check your stats
• SUBSCRIBE - View plans
• MENU - See all options

📞 For technical support, contact: support@microlearn.com
⏰ Lessons are sent daily at 9 AM

Keep learning! 🌟"""
        
        self.send_message(user.phone_number, help_msg)
    
    def send_daily_lesson(self, user):
        """Send a daily lesson to user"""
        # Get user's next lesson based on progress
        completed_lessons = [p.lesson_id for p in user.progress]
        
        # Find next lesson user hasn't completed
        lesson = Lesson.query.filter(~Lesson.id.in_(completed_lessons)).first()
        
        if not lesson:
            # User completed all lessons
            message = """🎉 Congratulations! 

You've completed all available lessons! 

🏆 You're a learning champion!
📜 Check your certificates with PROGRESS
🔄 New lessons are added weekly

Keep up the amazing work! 💪"""
            
            self.send_message(user.phone_number, message)
            return
        
        # Format lesson message
        lesson_msg = f"""📚 Today's Lesson: {lesson.title}

{lesson.content}

⏱️ Duration: ~{lesson.estimated_duration} minutes
📈 Level: {lesson.difficulty_level.title()}

Reply 'DONE' when you complete this lesson!
Reply 'QUIZ' to test your knowledge!"""
        
        self.send_message(user.phone_number, lesson_msg)
        
        # Send quiz if available
        if lesson.quiz_questions:
            quiz_data = json.loads(lesson.quiz_questions) if isinstance(lesson.quiz_questions, str) else lesson.quiz_questions
            if quiz_data:
                quiz_msg = f"\n🧠 Quick Quiz:\n{quiz_data[0]['question']}\n\n"
                for i, option in enumerate(quiz_data[0]['options']):
                    quiz_msg += f"{i+1}. {option}\n"
                quiz_msg += "\nReply with the number of your answer!"
                
                self.send_message(user.phone_number, quiz_msg)
    
    def show_progress(self, user):
        """Show user's learning progress"""
        total_lessons = Lesson.query.count()
        completed_lessons = len(user.progress)
        completion_rate = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        progress_msg = f"""📊 Your Learning Progress:

✅ Lessons Completed: {completed_lessons}/{total_lessons}
📈 Completion Rate: {completion_rate:.1f}%
🔥 Current Streak: {user.current_streak} days
🏆 Total Learning Time: {sum([p.time_spent or 0 for p in user.progress])} minutes

🎯 Keep going! You're doing great!

Reply 'LESSON' for your next lesson!"""
        
        self.send_message(user.phone_number, progress_msg)
    
    def show_subscription_options(self, user):
        """Show subscription plans"""
        sub_msg = f"""💎 Upgrade Your Learning Experience!

Current Plan: {user.subscription_status.title()}

📅 DAILY PLAN - $2.99/week
• Daily personalized lessons
• Progress tracking
• Basic certificates

📊 WEEKLY PLAN - $9.99/month  
• All daily features
• Advanced quizzes
• Priority support
• Skill badges

🏆 PREMIUM PLAN - $29.99/month
• Everything included
• 1-on-1 coaching sessions
• Industry certificates
• Job placement assistance

Reply 'UPGRADE DAILY', 'UPGRADE WEEKLY', or 'UPGRADE PREMIUM' to subscribe!"""
        
        self.send_message(user.phone_number, sub_msg)
    
    def handle_unknown_command(self, user):
        """Handle unknown commands"""
        unknown_msg = """🤔 I didn't understand that command.

Try these options:
• LESSON - Get today's lesson
• MENU - See all commands
• HELP - Get assistance
• START - Begin learning

What would you like to do?"""
        
        self.send_message(user.phone_number, unknown_msg)

# Initialize bot
bot = WhatsAppBot()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        from_number = request.form.get('From')
        message_body = request.form.get('Body')
        
        if from_number and message_body:
            bot.process_incoming_message(from_number, message_body)
        
        return '', 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return '', 500

@app.route('/admin')
def admin_dashboard():
    try:
        # Admin dashboard
        users_count = User.query.count()
        lessons_count = Lesson.query.count()
        categories_count = Category.query.count()
        
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        
        return render_template('admin.html', 
                            users_count=users_count,
                            lessons_count=lessons_count, 
                            categories_count=categories_count,
                            recent_users=recent_users)
    except Exception as e:
        return "Database error", 500

@app.route('/admin/lessons')
def admin_lessons():
    """Manage lessons"""
    lessons = Lesson.query.join(Category).all()
    categories = Category.query.all()
    return render_template('lessons.html', lessons=lessons, categories=categories)

@app.route('/admin/users')
def admin_users():
    """Manage users"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('users.html', users=users)

# Scheduled Tasks
def send_daily_lessons():
    """Send daily lessons to all active users"""
    active_users = User.query.filter(
        User.subscription_status.in_(['daily', 'weekly', 'premium'])
    ).all()
    
    for user in active_users:
        try:
            bot.send_daily_lesson(user)
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Error sending lesson to {user.phone_number}: {e}")

def run_scheduler():
    """Run scheduled tasks"""
    schedule.every().day.at("09:00").do(send_daily_lessons)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in background thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
