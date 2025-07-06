import schedule
import time
import threading
from datetime import datetime, timedelta
from app import db, bot
from models import User, Lesson, UserProgress
import random

class LessonScheduler:
    def __init__(self):
        self.is_running = False
        self.scheduler_thread = None
    
    def start_scheduler(self):
        """Start the lesson scheduling system"""
        if not self.is_running:
            self.is_running = True
            
            # Schedule daily lessons
            schedule.every().day.at("09:00").do(self.send_daily_lessons)
            
            # Schedule weekly progress reports
            schedule.every().monday.at("10:00").do(self.send_weekly_reports)
            
            # Schedule subscription reminders
            schedule.every().day.at("18:00").do(self.send_subscription_reminders)
            
            # Start scheduler thread
            self.scheduler_thread = threading.Thread(target=self._run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            
            print("Lesson scheduler started successfully!")
    
    def stop_scheduler(self):
        """Stop the lesson scheduling system"""
        self.is_running = False
        schedule.clear()
        print("Lesson scheduler stopped!")
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def send_daily_lessons(self):
        """Send daily lessons to all active subscribers"""
        print(f"Starting daily lesson delivery at {datetime.now()}")
        
        # Get all active subscribers
        active_users = User.query.filter(
            User.subscription_status.in_(['daily', 'weekly', 'premium']),
            User.subscription_end >= datetime.now().date()
        ).all()
        
        print(f"Found {len(active_users)} active subscribers")
        
        for user in active_users:
            try:
                self._send_personalized_lesson(user)
                time.sleep(2)  # Rate limiting to avoid overwhelming WhatsApp API
            except Exception as e:
                print(f"Error sending lesson to {user.phone_number}: {e}")
        
        print("Daily lesson delivery completed!")
    
    def _send_personalized_lesson(self, user):
        """Send a personalized lesson to a specific user"""
        # Get user's completed lessons
        completed_lesson_ids = [p.lesson_id for p in user.progress]
        
        # Find next lesson user hasn't completed
        next_lesson = Lesson.query.filter(
            ~Lesson.id.in_(completed_lesson_ids)
        ).order_by(Lesson.lesson_order).first()
        
        if not next_lesson:
            # User completed all lessons - send congratulations
            self._send_completion_message(user)
            return
        
        # Send the lesson
        lesson_message = self._format_lesson_message(next_lesson, user)
        bot.send_message(user.phone_number, lesson_message)
        
        # Send follow-up quiz if available
        if next_lesson.quiz_questions:
            quiz_message = self._format_quiz_message(next_lesson)
            bot.send_message(user.phone_number, quiz_message)
    
    def _format_lesson_message(self, lesson, user):
        """Format lesson content for WhatsApp delivery"""
        greeting = self._get_personalized_greeting(user)
        
        message = f"""{greeting}
        
📚 **Today's Lesson: {lesson.title}**

{lesson.content}

⏱️ **Duration:** ~{lesson.estimated_duration} minutes
📈 **Level:** {lesson.difficulty_level.title()}
🎯 **Category:** {lesson.category.name}

💡 **Quick Tip:** Take notes while learning for better retention!

Reply 'DONE' when you complete this lesson!
Reply 'HELP' if you need assistance."""
        
        return message
    
    def _format_quiz_message(self, lesson):
        """Format quiz questions for WhatsApp"""
        import json
        
        quiz_data = lesson.quiz_questions
        if isinstance(quiz_data, str):
            quiz_data = json.loads(quiz_data)
        
        if not quiz_data or len(quiz_data) == 0:
            return None
        
        question = quiz_data[0]  # Send first question
        
        quiz_message = f"""🧠 **Quick Knowledge Check:**

{question['question']}

"""
        
        for i, option in enumerate(question['options']):
            quiz_message += f"{i+1}. {option}\n"
        
        quiz_message += "\nReply with the number of your answer (1, 2, 3, or 4)!"
        
        return quiz_message
    
    def _get_personalized_greeting(self, user):
        """Get a personalized greeting based on user's progress"""
        greetings = [
            f"Good morning, {user.name or 'learner'}! 🌅",
            f"Hello {user.name or 'there'}! Ready to learn? 📚",
            f"Hi {user.name or 'champion'}! Time for today's lesson! 🎯",
            f"Hey {user.name or 'superstar'}! Let's grow together! 🌱"
        ]
        
        if user.current_streak > 7:
            greetings.append(f"Wow! {user.current_streak} days strong! Keep it up! 🔥")
        
        return random.choice(greetings)
    
    def _send_completion_message(self, user):
        """Send congratulations message for course completion"""
        message = f"""🎉 **CONGRATULATIONS, {user.name or 'CHAMPION'}!** 🎉

You've completed ALL available lessons! 

🏆 **Your Amazing Stats:**
• Total Lessons: {user.total_lessons_completed}
• Learning Streak: {user.current_streak} days
• You're in the top 5% of learners!

🎁 **What's Next:**
• New lessons added weekly
• Check your certificates: Reply 'CERTIFICATES'
• Refer friends and earn rewards
• Consider upgrading for advanced features

You're absolutely incredible! Keep learning! 💪✨"""
        
        bot.send_message(user.phone_number, message)
    
    def send_weekly_reports(self):
        """Send weekly progress reports to users"""
        print("Sending weekly progress reports...")
        
        active_users = User.query.filter(
            User.subscription_status.in_(['daily', 'weekly', 'premium'])
        ).all()
        
        for user in active_users:
            try:
                self._send_weekly_report(user)
                time.sleep(1)
            except Exception as e:
                print(f"Error sending weekly report to {user.phone_number}: {e}")
    
    def _send_weekly_report(self, user):
        """Send individual weekly progress report"""
        # Calculate weekly stats
        week_ago = datetime.now() - timedelta(days=7)
        weekly_progress = UserProgress.query.filter(
            UserProgress.user_id == user.id,
            UserProgress.completed_at >= week_ago
        ).count()
        
        report_message = f"""📊 **Your Weekly Learning Report**

Hello {user.name or 'Learner'}! Here's your progress:

📚 **This Week:**
• Lessons completed: {weekly_progress}
• Current streak: {user.current_streak} days
• Total lessons: {user.total_lessons_completed}

🎯 **Goals for Next Week:**
• Complete 5 more lessons
• Maintain your streak
• Try a new category

🔥 **Motivation:** You're doing great! Every lesson brings you closer to your goals!

Keep up the amazing work! 💪"""
        
        bot.send_message(user.phone_number, report_message)
    
    def send_subscription_reminders(self):
        """Send subscription renewal reminders"""
        print("Checking for subscription renewals...")
        
        # Find users whose subscriptions expire in 3 days
        expiry_date = datetime.now().date() + timedelta(days=3)
        expiring_users = User.query.filter(
            User.subscription_end == expiry_date,
            User.subscription_status != 'free'
        ).all()
        
        for user in expiring_users:
            try:
                self._send_renewal_reminder(user)
            except Exception as e:
                print(f"Error sending renewal reminder to {user.phone_number}: {e}")
    
    def _send_renewal_reminder(self, user):
        """Send subscription renewal reminder"""
        reminder_message = f"""⏰ **Subscription Reminder**

Hi {user.name or 'there'}! Your {user.subscription_status} plan expires in 3 days.

Don't lose access to:
• Daily personalized lessons
• Progress tracking
• Certificates and badges
• Priority support

💎 **Renew now to continue your learning journey!**

Reply 'RENEW' to extend your subscription
Reply 'HELP' for assistance

We'd hate to see you go! 💙"""
        
        bot.send_message(user.phone_number, reminder_message)

# Initialize scheduler
lesson_scheduler = LessonScheduler()
