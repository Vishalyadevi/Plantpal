import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///plantpal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # App settings
    PLANTS_PER_PAGE = 12
    MOOD_LOGS_PER_PAGE = 20
    
    # Gamification settings
    DAILY_LOGIN_BONUS = 10
    MOOD_LOG_BONUS = 5
    LEVEL_UP_THRESHOLD = 100   