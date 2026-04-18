from flask import Flask, render_template, request, jsonify, session
from flask_mail import Mail, Message
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)

# Team Data with Social Media
TEAM = [
    {
        'name': 'Siva',
        'role': 'Full Stack Architect',
        'bio': '10+ years of experience building scalable web applications. Expert in React, Python, and Cloud Architecture.',
        'icon': '🚀',
        'skills': ['Python', 'React', 'AWS', 'Docker'],
        'social': {
            'github': 'https://github.com/siva',
            'linkedin': 'https://linkedin.com/in/siva',
            'twitter': 'https://twitter.com/siva',
            'instagram': 'https://instagram.com/siva'
        }
    },
    {
        'name': 'Philip',
        'role': 'Backend Engineer',
        'bio': 'Database wizard and API specialist. Creates robust, secure, and lightning-fast backend systems.',
        'icon': '⚡',
        'skills': ['Node.js', 'PostgreSQL', 'Redis', 'MongoDB'],
        'social': {
            'github': 'https://github.com/philip',
            'linkedin': 'https://linkedin.com/in/philip',
            'twitter': 'https://twitter.com/philip',
            'instagram': 'https://instagram.com/philip'
        }
    },
    {
        'name': 'David',
        'role': 'UI/UX Designer',
        'bio': 'Creative mind behind beautiful interfaces. Turns complex ideas into intuitive user experiences.',
        'icon': '🎨',
        'skills': ['Figma', 'Tailwind', 'Framer', 'Adobe XD'],
        'social': {
            'github': 'https://github.com/david',
            'linkedin': 'https://linkedin.com/in/david',
            'dribbble': 'https://dribbble.com/david',
            'behance': 'https://behance.net/david'
        }
    }
]

# Services Data
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

# Portfolio Projects
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

# Pricing Plans
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
            
            # Send email notification
            msg = Message(f'New Contact Form Submission from {name}',
                        recipients=[os.getenv('EMAIL_USER')])
            msg.body = f"""
            Name: {name}
            Email: {email}
            Message: {message}
            """
            mail.send(msg)
            
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
    
    # Process contact form
    # Add your logic here
    
    return jsonify({'status': 'success', 'message': 'Thank you! We\'ll contact you soon.'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)