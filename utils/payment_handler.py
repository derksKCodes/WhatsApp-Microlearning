import stripe
import os
from datetime import datetime, timedelta
from app import db
from models import User, Subscription

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class PaymentHandler:
    def __init__(self):
        self.plans = {
            'daily': {'price': 299, 'interval': 'week'},  # $2.99 per week
            'weekly': {'price': 999, 'interval': 'month'},  # $9.99 per month
            'premium': {'price': 2999, 'interval': 'month'}  # $29.99 per month
        }
    
    def create_payment_intent(self, user_id, plan_type, amount):
        """Create a Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'user_id': user_id,
                    'plan_type': plan_type
                }
            )
            return intent
        except Exception as e:
            print(f"Error creating payment intent: {e}")
            return None
    
    def process_subscription(self, user_id, plan_type, payment_intent_id):
        """Process successful subscription payment"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False
            
            # Calculate subscription dates
            start_date = datetime.now().date()
            if plan_type == 'daily':
                end_date = start_date + timedelta(days=7)
            else:
                end_date = start_date + timedelta(days=30)
            
            # Create subscription record
            subscription = Subscription(
                user_id=user_id,
                plan_type=plan_type,
                amount=self.plans[plan_type]['price'] / 100,
                payment_status='completed',
                payment_id=payment_intent_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Update user subscription status
            user.subscription_status = plan_type
            user.subscription_start = start_date
            user.subscription_end = end_date
            
            db.session.add(subscription)
            db.session.commit()
            
            return True
        except Exception as e:
            print(f"Error processing subscription: {e}")
            db.session.rollback()
            return False
    
    def check_subscription_status(self, user_id):
        """Check if user's subscription is active"""
        user = User.query.get(user_id)
        if not user or not user.subscription_end:
            return False
        
        return user.subscription_end >= datetime.now().date()
    
    def cancel_subscription(self, user_id):
        """Cancel user's subscription"""
        try:
            user = User.query.get(user_id)
            if user:
                user.subscription_status = 'free'
                user.subscription_end = datetime.now().date()
                db.session.commit()
                return True
        except Exception as e:
            print(f"Error canceling subscription: {e}")
            db.session.rollback()
        return False
