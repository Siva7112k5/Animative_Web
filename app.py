from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexvion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER', 'your_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD', 'your_password')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER', 'your_email@gmail.com')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please login to access admin panel'

# ========== DATABASE MODELS ==========

class ContactMessage(db.Model):
    """Model for storing contact form messages"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ContactMessage {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read,
            'is_replied': self.is_replied
        }

class Admin(UserMixin, db.Model):
    """Model for admin users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# ========== CREATE DATABASE TABLES ==========
def init_db():
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@nexvion.com')
            admin.set_password('admin123')  # Change this password!
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: username='admin', password='admin123'")

# ========== TEAM DATA ==========
TEAM = [
    {
        'name': 'Siva',
        'role': 'Full Stack Architect',
        'bio': '10+ years of experience building scalable web applications. Expert in React, Python, and Cloud Architecture.',
        'icon': '🚀',
        'skills': ['Python', 'React', 'AWS', 'Docker']
    },
    {
        'name': 'Philip',
        'role': 'Backend Engineer',
        'bio': 'Database wizard and API specialist. Creates robust, secure, and lightning-fast backend systems.',
        'icon': '⚡',
        'skills': ['Node.js', 'PostgreSQL', 'Redis', 'MongoDB']
    },
    {
        'name': 'David',
        'role': 'UI/UX Designer',
        'bio': 'Creative mind behind beautiful interfaces. Turns complex ideas into intuitive user experiences.',
        'icon': '🎨',
        'skills': ['Figma', 'Tailwind', 'Framer', 'Adobe XD']
    }
]

# ========== SERVICES DATA ==========
SERVICES = [
    {
        'id': 1,
        'title': 'Web Applications',
        'icon': '💻',
        'description': 'Custom web apps built with modern frameworks. Scalable, secure, and high-performance.',
        'features': ['React/Next.js', 'Node.js/Python', 'Database Design', 'API Development']
    },
    {
        'id': 2,
        'title': 'E-Commerce Solutions',
        'icon': '🛒',
        'description': 'Full-featured online stores with payment integration and inventory management.',
        'features': ['Payment Gateway', 'Product Catalog', 'Order Management', 'Analytics']
    },
    {
        'id': 3,
        'title': 'Mobile Apps',
        'icon': '📱',
        'description': 'Cross-platform mobile applications for iOS and Android using React Native.',
        'features': ['iOS & Android', 'Push Notifications', 'Offline Mode', 'App Store Deploy']
    },
    {
        'id': 4,
        'title': 'Cloud Services',
        'icon': '☁️',
        'description': 'AWS, GCP, and Azure solutions. Scalable infrastructure and DevOps automation.',
        'features': ['Cloud Migration', 'CI/CD Pipeline', 'Monitoring', 'Auto-scaling']
    },
    {
        'id': 5,
        'title': 'UI/UX Design',
        'icon': '🎨',
        'description': 'Beautiful, user-centered designs that convert visitors into customers.',
        'features': ['User Research', 'Wireframing', 'Prototyping', 'Usability Testing']
    },
    {
        'id': 6,
        'title': 'Maintenance & Support',
        'icon': '🔧',
        'description': '24/7 technical support, security updates, and performance optimization.',
        'features': ['24/7 Monitoring', 'Security Patches', 'Backup', 'Performance Tuning']
    }
]

# ========== PORTFOLIO PROJECTS ==========
PROJECTS = [
    {
        'id': 1,
        'title': 'FinTech Dashboard',
        'category': 'Web App',
        'client': 'CapitalFlow',
        'description': 'Real-time financial analytics dashboard with live data visualization.',
        'tech': ['React', 'D3.js', 'Node.js', 'Socket.io'],
        'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600'
    },
    {
        'id': 2,
        'title': 'EcoShop Marketplace',
        'category': 'E-commerce',
        'client': 'GreenCart',
        'description': 'Sustainable products marketplace with AI recommendations.',
        'tech': ['Next.js', 'Stripe', 'MongoDB', 'Tailwind'],
        'image': 'https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=600'
    },
    {
        'id': 3,
        'title': 'HealthTrack App',
        'category': 'Mobile App',
        'client': 'Wellness Inc',
        'description': 'Fitness tracking app with personalized workout plans.',
        'tech': ['React Native', 'Firebase', 'Redux'],
        'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600'
    },
    {
        'id': 4,
        'title': 'AI Content Generator',
        'category': 'Web App',
        'client': 'ContentHub',
        'description': 'AI-powered content creation platform for marketers.',
        'tech': ['Python', 'OpenAI', 'React', 'PostgreSQL'],
        'image': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600'
    }
]

# ========== PRICING PLANS ==========
PRICING = [
    {
        'name': 'Starter',
        'price': '$2,999',
        'period': 'one-time',
        'description': 'Perfect for small businesses',
        'features': [
            '5-page website',
            'Mobile responsive',
            'Contact form',
            'Basic SEO',
            '1 month support'
        ],
        'popular': False
    },
    {
        'name': 'Professional',
        'price': '$7,999',
        'period': 'one-time',
        'description': 'For growing companies',
        'features': [
            '15-page website',
            'E-commerce ready',
            'Custom animations',
            'Advanced SEO',
            '6 months support',
            'Analytics dashboard'
        ],
        'popular': True
    },
    {
        'name': 'Enterprise',
        'price': 'Custom',
        'period': 'negotiable',
        'description': 'For large organizations',
        'features': [
            'Unlimited pages',
            'Custom backend',
            'Mobile apps',
            '24/7 priority support',
            'SLA agreement',
            'Dedicated team'
        ],
        'popular': False
    }
]

# ========== ROUTES ==========

@app.route('/')
def index():
    return render_template('index.html', team=TEAM, services=SERVICES, projects=PROJECTS, pricing=PRICING)

@app.route('/about')
def about():
    return render_template('about.html', team=TEAM)

@app.route('/services')
def services():
    return render_template('services.html', services=SERVICES)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', projects=PROJECTS)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', pricing=PRICING)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Save to database
            contact_msg = ContactMessage(
                name=name,
                email=email,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            
            # Send email notification (optional)
            try:
                mail = Mail(app)
                msg = Message(f'New Contact Form Submission from {name}',
                            recipients=[os.getenv('EMAIL_USER', 'admin@nexvion.com')])
                msg.body = f"""
                Name: {name}
                Email: {email}
                Message: {message}
                
                View in admin panel: http://localhost:5000/admin/messages
                """
                mail.send(msg)
            except:
                pass  # Email failed but message is saved
            
            return jsonify({'success': True, 'message': 'Message sent successfully!'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('contact.html')

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    # Save to database
    contact_msg = ContactMessage(
        name=name,
        email=email,
        message=message
    )
    db.session.add(contact_msg)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Thank you! We\'ll contact you soon.'})

# ========== ADMIN PANEL ROUTES ==========

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    # Get statistics
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_messages=total_messages,
                         unread_messages=unread_messages,
                         recent_messages=recent_messages)

@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/message/<int:message_id>')
@login_required
def admin_view_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    # Mark as read
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    return render_template('admin/message_detail.html', message=message)

@app.route('/admin/message/<int:message_id>/delete', methods=['POST'])
@login_required
def admin_delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/message/<int:message_id>/reply', methods=['POST'])
@login_required
def admin_reply_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    reply_text = request.form.get('reply')
    
    if reply_text:
        # Here you would send an email reply
        # For now, just mark as replied
        message.is_replied = True
        db.session.commit()
        flash('Reply sent successfully', 'success')
    
    return redirect(url_for('admin_view_message', message_id=message_id))

@app.route('/admin/messages/mark-all-read', methods=['POST'])
@login_required
def admin_mark_all_read():
    ContactMessage.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    flash('All messages marked as read', 'success')
    return redirect(url_for('admin_messages'))

# ========== RUN APP ==========
if __name__ == '__main__':
    init_db()  # Initialize database and create tables
    app.run(debug=True, port=5000)