from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from config import Config
from models import db, User, Plant, MoodLog, Reminder
from forms import RegistrationForm, LoginForm, PlantForm, MoodLogForm, ReminderForm
from sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Welcome to PlantPal! 🌱', 'success')
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            # Update streak
            now = datetime.utcnow()
            if user.last_login:
                days_diff = (now - user.last_login).days
                if days_diff == 1:
                    user.streak_days += 1
                    flash(f'🔥 {user.streak_days} day streak!', 'info')
                elif days_diff > 1:
                    user.streak_days = 1
            else:
                user.streak_days = 1
            
            user.last_login = now
            db.session.commit()
            
            login_user(user)
            flash(f'Welcome back, {user.username}! 🌿', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out. See you soon! 👋', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    plants = Plant.query.filter_by(user_id=current_user.id).all()
    
    # Get upcoming reminders
    upcoming_reminders = Reminder.query.join(Plant).filter(
        Plant.user_id == current_user.id,
        Reminder.completed == False,
        Reminder.reminder_date >= datetime.utcnow()
    ).order_by(Reminder.reminder_date).limit(5).all()
    
    # Get recent mood logs
    recent_moods = MoodLog.query.join(Plant).filter(
        Plant.user_id == current_user.id
    ).order_by(MoodLog.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                          plants=plants, 
                          reminders=upcoming_reminders,
                          recent_moods=recent_moods)

@app.route('/plant/add', methods=['GET', 'POST'])
@login_required
def add_plant():
    form = PlantForm()
    if form.validate_on_submit():
        plant = Plant(
            name=form.name.data,
            type=form.type.data,
            user_id=current_user.id
        )
        db.session.add(plant)
        db.session.commit()
        flash(f'🌱 {plant.name} has been planted!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_plant.html', form=form)

@app.route('/plant/<int:plant_id>')
@login_required
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != current_user.id:
        flash('You do not have permission to view this plant.', 'danger')
        return redirect(url_for('dashboard'))
    
    mood_logs = MoodLog.query.filter_by(plant_id=plant_id).order_by(MoodLog.created_at.desc()).all()
    reminders = Reminder.query.filter_by(plant_id=plant_id).order_by(Reminder.reminder_date).all()
    
    return render_template('plant_detail.html', 
                          plant=plant, 
                          mood_logs=mood_logs,
                          reminders=reminders)

@app.route('/plant/<int:plant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != current_user.id:
        flash('You do not have permission to edit this plant.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = PlantForm(obj=plant)
    if form.validate_on_submit():
        plant.name = form.name.data
        plant.type = form.type.data
        db.session.commit()
        flash(f'✅ {plant.name} has been updated!', 'success')
        return redirect(url_for('plant_detail', plant_id=plant.id))
    
    return render_template('add_plant.html', form=form, edit=True)

@app.route('/plant/<int:plant_id>/delete', methods=['POST'])
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != current_user.id:
        flash('You do not have permission to delete this plant.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(plant)
    db.session.commit()
    flash(f'🗑️ {plant.name} has been removed.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/plant/<int:plant_id>/mood', methods=['GET', 'POST'])
@login_required
def add_mood_log(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != current_user.id:
        flash('You do not have permission to add mood logs to this plant.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = MoodLogForm()
    if form.validate_on_submit():
        # Analyze sentiment
        sentiment = SentimentAnalyzer.analyze(form.note_text.data)
        
        # Create mood log
        mood_log = MoodLog(
            plant_id=plant_id,
            note_text=form.note_text.data,
            sentiment_score=sentiment['score'],
            sentiment_label=sentiment['label']
        )
        db.session.add(mood_log)
        
        # Update plant growth
        plant.add_growth_points(sentiment['growth_points'])
        db.session.commit()
        
        emoji = SentimentAnalyzer.get_emoji(sentiment['label'])
        flash(f'{emoji} Mood logged! Your plant {sentiment["label"]} vibes!', 'success')
        return redirect(url_for('plant_detail', plant_id=plant_id))
    
    return render_template('mood_log.html', form=form, plant=plant)

@app.route('/mood/<int:mood_id>/delete', methods=['POST'])
@login_required
def delete_mood(mood_id):
    mood = MoodLog.query.get_or_404(mood_id)
    plant = mood.plant
    
    if plant.user_id != current_user.id:
        flash('You do not have permission to delete this mood log.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(mood)
    db.session.commit()
    flash('Mood log deleted.', 'info')
    return redirect(url_for('plant_detail', plant_id=plant.id))

@app.route('/plant/<int:plant_id>/reminder', methods=['POST'])
@login_required
def add_reminder(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    if plant.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    form = ReminderForm()
    if form.validate_on_submit():
        reminder = Reminder(
            plant_id=plant_id,
            description=form.description.data,
            reminder_date=form.reminder_date.data
        )
        db.session.add(reminder)
        db.session.commit()
        flash('⏰ Reminder added!', 'success')
        return redirect(url_for('plant_detail', plant_id=plant_id))
    
    flash('Invalid reminder data.', 'danger')
    return redirect(url_for('plant_detail', plant_id=plant_id))

@app.route('/reminder/<int:reminder_id>/complete', methods=['POST'])
@login_required
def complete_reminder(reminder_id):
    reminder = Reminder.query.get_or_404(reminder_id)
    plant = reminder.plant
    
    if plant.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    reminder.completed = True
    db.session.commit()
    return jsonify({'success': True})

@app.route('/reminder/<int:reminder_id>/delete', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    reminder = Reminder.query.get_or_404(reminder_id)
    plant = reminder.plant
    
    if plant.user_id != current_user.id:
        flash('You do not have permission to delete this reminder.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(reminder)
    db.session.commit()
    flash('Reminder deleted.', 'info')
    return redirect(url_for('plant_detail', plant_id=plant.id))

@app.route('/insights')
@login_required
def insights():
    # Get all mood logs for the user
    mood_logs = MoodLog.query.join(Plant).filter(
        Plant.user_id == current_user.id
    ).order_by(MoodLog.created_at).all()
    
    # Prepare data for charts
    mood_data = {
        'labels': [log.created_at.strftime('%m/%d') for log in mood_logs[-30:]],
        'scores': [log.sentiment_score for log in mood_logs[-30:]],
        'sentiments': [log.sentiment_label for log in mood_logs[-30:]]
    }
    
    # Calculate statistics
    total_logs = len(mood_logs)
    positive_count = len([log for log in mood_logs if log.sentiment_label == 'positive'])
    neutral_count = len([log for log in mood_logs if log.sentiment_label == 'neutral'])
    negative_count = len([log for log in mood_logs if log.sentiment_label == 'negative'])
    
    stats = {
        'total': total_logs,
        'positive': positive_count,
        'neutral': neutral_count,
        'negative': negative_count
    }
    
    return render_template('insights.html', mood_data=mood_data, stats=stats)

if __name__ == '__main__':
    app.run()