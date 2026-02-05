#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kengni Finance - Complete Financial Management & Trading Application
Version 2.0 - Enhanced with AI Analysis and Advanced Features
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
from datetime import datetime, timedelta
import secrets
import json
import pandas as pd
from io import BytesIO
import yfinance as yf
import numpy as np
import base64
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Add Python built-in functions to Jinja2 environment
app.jinja_env.globals.update({
    'abs': abs,
    'min': min,
    'max': max,
    'round': round,
    'int': int,
    'float': float,
    'len': len,
    'sum': sum
})

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Configuration
DB_FILE = 'kengni_finance.db'

# Allowed extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Connection Helper
def get_db_connection():
    """Create and return database connection"""
    try:
        connection = sqlite3.connect(DB_FILE)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database with enhanced tables
def init_db():
    """Initialize database with all tables"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Users table with preferences
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            status TEXT DEFAULT 'active',
            preferred_currency TEXT DEFAULT 'EUR',
            timezone TEXT DEFAULT 'Europe/Paris',
            theme TEXT DEFAULT 'light',
            notifications_email INTEGER DEFAULT 1,
            notifications_app INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT
        )
        ''')
        
        # Financial transactions with enhanced categories
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('revenue', 'expense', 'receivable', 'credit', 'debt', 'investment')),
            category TEXT NOT NULL,
            subcategory TEXT,
            reason TEXT NOT NULL,
            usage TEXT,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'EUR',
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            payment_method TEXT,
            reference TEXT,
            status TEXT DEFAULT 'completed' CHECK(status IN ('completed', 'pending', 'cancelled')),
            notes TEXT,
            tags TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Trading positions
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            avg_price REAL NOT NULL,
            current_price REAL NOT NULL,
            status TEXT DEFAULT 'open',
            stop_loss REAL,
            take_profit REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            closed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Trading transactions
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            amount REAL NOT NULL,
            fees REAL DEFAULT 0,
            status TEXT DEFAULT 'completed',
            strategy TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Trading journal with images
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trading_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transaction_id INTEGER,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('buy', 'sell')),
            quantity REAL NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL,
            profit_loss REAL,
            strategy TEXT,
            setup_description TEXT,
            emotions TEXT,
            mistakes TEXT,
            lessons_learned TEXT,
            notes TEXT,
            image_path TEXT,
            chart_analysis TEXT,
            market_conditions TEXT,
            risk_reward_ratio REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (transaction_id) REFERENCES transactions(id)
        )
        ''')
        
        # AI Analysis results
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            analysis_type TEXT NOT NULL CHECK(analysis_type IN ('financial', 'trading', 'psychological', 'strategy')),
            subject TEXT,
            insights TEXT NOT NULL,
            recommendations TEXT,
            warnings TEXT,
            confidence_score REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Trader performance scores
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trader_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            overall_score REAL NOT NULL,
            discipline_score REAL,
            risk_management_score REAL,
            strategy_consistency_score REAL,
            emotional_control_score REAL,
            profitability_score REAL,
            monthly_trades INTEGER,
            win_rate REAL,
            profit_factor REAL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Psychological patterns detection
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS psychological_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pattern_type TEXT NOT NULL CHECK(pattern_type IN ('FOMO', 'revenge_trading', 'overtrading', 'overconfidence', 'fear', 'greed')),
            severity TEXT CHECK(severity IN ('low', 'medium', 'high', 'critical')),
            detected_date TEXT NOT NULL,
            description TEXT,
            evidence TEXT,
            recommendations TEXT,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'resolved', 'monitoring')),
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Reports table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            report_type TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            revenue REAL DEFAULT 0,
            expenses REAL DEFAULT 0,
            profit REAL DEFAULT 0,
            profit_margin REAL DEFAULT 0,
            data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Notifications
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('alert', 'warning', 'info', 'success')),
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            action_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Check if default user exists
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = ?", ('fabrice.kengni@icloud.com',))
        if cursor.fetchone()[0] == 0:
            hashed_password = generate_password_hash('kengni')
            cursor.execute('''
                INSERT INTO users (username, email, password, role, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', ('kengni', 'fabrice.kengni@icloud.com', hashed_password, 'admin', datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# AI Analysis Functions

def analyze_trading_psychology(user_id):
    """Analyze psychological trading patterns"""
    conn = get_db_connection()
    patterns = []
    
    if conn:
        cursor = conn.cursor()
        
        # Get recent transactions
        cursor.execute("""
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (user_id,))
        transactions = [dict(row) for row in cursor.fetchall()]
        
        # Get journal entries
        cursor.execute("""
            SELECT * FROM trading_journal
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 20
        """, (user_id,))
        journal_entries = [dict(row) for row in cursor.fetchall()]
        
        # Analyze patterns
        
        # 1. Overtrading detection
        recent_24h = sum(1 for t in transactions if datetime.fromisoformat(t['created_at']) > datetime.now() - timedelta(hours=24))
        if recent_24h > 10:
            patterns.append({
                'type': 'overtrading',
                'severity': 'high' if recent_24h > 20 else 'medium',
                'description': f'Vous avez effectué {recent_24h} transactions en 24h',
                'recommendation': 'Prenez du recul. Le overtrading augmente les frais et diminue la qualité des décisions.'
            })
        
        # 2. FOMO detection (buying after big moves)
        buy_after_loss = 0
        for i in range(1, min(len(transactions), 10)):
            if transactions[i]['type'] == 'buy' and i > 0:
                prev = transactions[i-1]
                if prev['type'] == 'sell' and prev['amount'] < 0:  # Previous was a loss
                    buy_after_loss += 1
        
        if buy_after_loss >= 3:
            patterns.append({
                'type': 'FOMO',
                'severity': 'high',
                'description': 'Tendance à acheter immédiatement après des pertes',
                'recommendation': 'Attendez 30 minutes avant toute nouvelle transaction après une perte.'
            })
        
        # 3. Revenge trading
        consecutive_losses = 0
        max_consecutive = 0
        for t in transactions:
            if t['type'] == 'sell' and t['amount'] < 0:
                consecutive_losses += 1
                max_consecutive = max(max_consecutive, consecutive_losses)
            else:
                consecutive_losses = 0
        
        if max_consecutive >= 3:
            patterns.append({
                'type': 'revenge_trading',
                'severity': 'critical',
                'description': f'{max_consecutive} pertes consécutives détectées',
                'recommendation': 'Arrêtez de trader après 2 pertes consécutives. Analysez vos erreurs.'
            })
        
        # 4. Emotional patterns from journal
        emotional_keywords = {
            'fear': ['peur', 'anxieux', 'stressé', 'inquiet', 'nerveux'],
            'greed': ['avidité', 'cupide', 'trop confiant', 'sûr de moi'],
            'overconfidence': ['facile', 'certain', 'évident', 'garanti']
        }
        
        for entry in journal_entries:
            if entry.get('emotions'):
                emotions_text = entry['emotions'].lower()
                for emotion, keywords in emotional_keywords.items():
                    if any(kw in emotions_text for kw in keywords):
                        patterns.append({
                            'type': emotion,
                            'severity': 'medium',
                            'description': f'Émotion détectée: {emotion}',
                            'recommendation': 'Identifiée dans votre journal. Restez objectif.'
                        })
        
        # Save patterns to database
        for pattern in patterns:
            cursor.execute("""
                INSERT INTO psychological_patterns 
                (user_id, pattern_type, severity, detected_date, description, recommendations)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                pattern['type'],
                pattern['severity'],
                datetime.now().isoformat(),
                pattern['description'],
                pattern['recommendation']
            ))
        
        conn.commit()
        conn.close()
    
    return patterns

def calculate_trader_score(user_id):
    """Calculate comprehensive trader score (0-100)"""
    conn = get_db_connection()
    score_data = {
        'overall_score': 50,
        'discipline_score': 50,
        'risk_management_score': 50,
        'strategy_consistency_score': 50,
        'emotional_control_score': 50,
        'profitability_score': 50,
        'details': {}
    }
    
    if conn:
        cursor = conn.cursor()
        
        # Get transactions
        cursor.execute("""
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 100
        """, (user_id,))
        transactions = [dict(row) for row in cursor.fetchall()]
        
        if not transactions:
            conn.close()
            return score_data
        
        # 1. Profitability Score (30% weight)
        total_profit = sum(t['amount'] for t in transactions if t['type'] == 'sell')
        total_invested = sum(abs(t['amount']) for t in transactions if t['type'] == 'buy')
        
        if total_invested > 0:
            roi = (total_profit / total_invested) * 100
            score_data['profitability_score'] = min(100, max(0, 50 + roi))
        
        wins = sum(1 for t in transactions if t['type'] == 'sell' and t['amount'] > 0)
        total_sells = sum(1 for t in transactions if t['type'] == 'sell')
        win_rate = (wins / total_sells * 100) if total_sells > 0 else 0
        score_data['details']['win_rate'] = round(win_rate, 2)
        
        # 2. Risk Management Score (25% weight)
        risk_score = 50
        
        # Check for stop losses
        cursor.execute("""
            SELECT COUNT(*) as with_sl FROM positions
            WHERE user_id = ? AND stop_loss IS NOT NULL
        """, (user_id,))
        positions_with_sl = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) as total FROM positions
            WHERE user_id = ?
        """, (user_id,))
        total_positions = cursor.fetchone()[0]
        
        if total_positions > 0:
            sl_percentage = (positions_with_sl / total_positions) * 100
            risk_score += (sl_percentage - 50) * 0.5
        
        # Check for position sizing consistency
        amounts = [abs(t['amount']) for t in transactions if t['type'] == 'buy']
        if len(amounts) > 5:
            avg_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            cv = (std_amount / avg_amount) if avg_amount > 0 else 0
            if cv < 0.3:  # Good consistency
                risk_score += 20
            elif cv > 0.8:  # Poor consistency
                risk_score -= 20
        
        score_data['risk_management_score'] = min(100, max(0, risk_score))
        
        # 3. Discipline Score (20% weight)
        discipline_score = 50
        
        # Check for overtrading
        recent_24h = sum(1 for t in transactions if datetime.fromisoformat(t['created_at']) > datetime.now() - timedelta(hours=24))
        if recent_24h > 15:
            discipline_score -= 30
        elif recent_24h < 5:
            discipline_score += 20
        
        # Check for revenge trading patterns
        cursor.execute("""
            SELECT COUNT(*) FROM psychological_patterns
            WHERE user_id = ? AND pattern_type = 'revenge_trading' AND status = 'active'
        """, (user_id,))
        revenge_patterns = cursor.fetchone()[0]
        if revenge_patterns > 0:
            discipline_score -= 20
        
        score_data['discipline_score'] = min(100, max(0, discipline_score))
        
        # 4. Strategy Consistency (15% weight)
        cursor.execute("""
            SELECT strategy, COUNT(*) as count
            FROM transactions
            WHERE user_id = ? AND strategy IS NOT NULL
            GROUP BY strategy
        """, (user_id,))
        strategies = cursor.fetchall()
        
        strategy_score = 50
        if strategies:
            # Reward using consistent strategies
            max_strategy_count = max(s[1] for s in strategies)
            total_with_strategy = sum(s[1] for s in strategies)
            consistency = (max_strategy_count / total_with_strategy) * 100 if total_with_strategy > 0 else 0
            strategy_score = min(100, consistency)
        
        score_data['strategy_consistency_score'] = strategy_score
        
        # 5. Emotional Control (10% weight)
        cursor.execute("""
            SELECT COUNT(*) FROM psychological_patterns
            WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        active_patterns = cursor.fetchone()[0]
        
        emotional_score = 100 - (active_patterns * 15)
        score_data['emotional_control_score'] = min(100, max(0, emotional_score))
        
        # Calculate overall score (weighted average)
        score_data['overall_score'] = round(
            score_data['profitability_score'] * 0.30 +
            score_data['risk_management_score'] * 0.25 +
            score_data['discipline_score'] * 0.20 +
            score_data['strategy_consistency_score'] * 0.15 +
            score_data['emotional_control_score'] * 0.10,
            2
        )
        
        # Save to database
        cursor.execute("""
            INSERT INTO trader_scores 
            (user_id, date, overall_score, discipline_score, risk_management_score, 
             strategy_consistency_score, emotional_control_score, profitability_score,
             monthly_trades, win_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            datetime.now().isoformat(),
            score_data['overall_score'],
            score_data['discipline_score'],
            score_data['risk_management_score'],
            score_data['strategy_consistency_score'],
            score_data['emotional_control_score'],
            score_data['profitability_score'],
            len(transactions),
            win_rate
        ))
        
        conn.commit()
        conn.close()
    
    return score_data

def analyze_financial_report(data):
    """AI-powered financial report analysis"""
    try:
        insights = {
            'summary': "Analyse automatique du rapport financier",
            'recommendations': [],
            'risks': [],
            'opportunities': [],
            'anomalies': []
        }
        
        if 'revenue' in data and 'expenses' in data:
            profit_margin = ((data['revenue'] - data['expenses']) / data['revenue'] * 100) if data['revenue'] > 0 else 0
            
            if profit_margin > 20:
                insights['recommendations'].append("✅ Excellente marge bénéficiaire. Envisagez d'investir dans la croissance.")
                insights['opportunities'].append("Capacité d'investissement disponible")
            elif profit_margin < 10:
                insights['recommendations'].append("⚠️ Marge bénéficiaire faible. Optimisez vos dépenses.")
                insights['risks'].append("Risque de rentabilité")
            
            if data['expenses'] > data['revenue']:
                insights['risks'].append("🚨 Dépenses supérieures aux revenus - attention critique!")
                insights['recommendations'].append("Action immédiate requise: réduire les dépenses de " + 
                    f"{round((data['expenses'] - data['revenue']) / data['revenue'] * 100, 2)}%")
            
            # Anomaly detection
            if data['expenses'] > data['revenue'] * 1.5:
                insights['anomalies'].append("Dépenses anormalement élevées détectées")
        
        return insights
    except Exception as e:
        return {'error': str(e)}

def analyze_trade_image(image_path, trade_data):
    """Analyze trading chart image and provide insights"""
    insights = {
        'setup_quality': 'N/A',
        'entry_timing': 'N/A',
        'risk_reward': 'N/A',
        'recommendations': []
    }
    
    try:
        # Basic analysis based on trade data
        if trade_data.get('risk_reward_ratio'):
            rr = trade_data['risk_reward_ratio']
            if rr >= 2:
                insights['risk_reward'] = 'Excellent'
                insights['recommendations'].append('✅ Bon ratio risque/récompense')
            elif rr >= 1:
                insights['risk_reward'] = 'Acceptable'
                insights['recommendations'].append('⚠️ Ratio risque/récompense minimum atteint')
            else:
                insights['risk_reward'] = 'Mauvais'
                insights['recommendations'].append('❌ Ratio risque/récompense insuffisant')
        
        # Analyze based on profit/loss
        if trade_data.get('profit_loss'):
            pl = trade_data['profit_loss']
            if pl > 0:
                insights['recommendations'].append('✅ Trade gagnant - analysez ce qui a fonctionné')
            else:
                insights['recommendations'].append('📝 Trade perdant - identifiez les erreurs')
        
        # Entry timing analysis
        if trade_data.get('strategy'):
            insights['setup_quality'] = 'Défini'
            insights['recommendations'].append(f'Strategy utilisée: {trade_data["strategy"]}')
        
    except Exception as e:
        insights['error'] = str(e)
    
    return insights

def trading_recommendation(symbol, timeframe='1mo'):
    """AI trading recommendations based on market data"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=timeframe)
        
        if hist.empty:
            return {'error': 'Données non disponibles'}
        
        current_price = hist['Close'].iloc[-1]
        sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else sma_20
        
        rsi = calculate_rsi(hist['Close'])
        
        # Volume analysis
        avg_volume = hist['Volume'].mean()
        recent_volume = hist['Volume'].iloc[-1]
        volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
        
        recommendation = {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'sma_20': round(sma_20, 2),
            'sma_50': round(sma_50, 2),
            'rsi': round(rsi, 2),
            'volume_ratio': round(volume_ratio, 2),
            'signal': 'NEUTRE',
            'confidence': 50,
            'analysis': [],
            'entry_points': [],
            'stop_loss': 0,
            'take_profit': 0
        }
        
        # Trend analysis
        if current_price > sma_20 and sma_20 > sma_50:
            recommendation['analysis'].append("📈 Tendance haussière confirmée")
            trend_score = 20
        elif current_price < sma_20 and sma_20 < sma_50:
            recommendation['analysis'].append("📉 Tendance baissière confirmée")
            trend_score = -20
        else:
            recommendation['analysis'].append("➡️ Tendance neutre/consolidation")
            trend_score = 0
        
        # RSI analysis
        if rsi > 70:
            recommendation['analysis'].append(f"🔴 RSI: {round(rsi, 2)} - Surachat détecté")
            rsi_score = -15
        elif rsi < 30:
            recommendation['analysis'].append(f"🟢 RSI: {round(rsi, 2)} - Survente détectée")
            rsi_score = 15
        else:
            recommendation['analysis'].append(f"🟡 RSI: {round(rsi, 2)} - Zone neutre")
            rsi_score = 0
        
        # Volume analysis
        if volume_ratio > 1.5:
            recommendation['analysis'].append(f"📊 Volume élevé ({round(volume_ratio, 2)}x) - Signal fort")
            volume_score = 10
        else:
            volume_score = 0
        
        # Generate signal
        total_score = trend_score + rsi_score + volume_score
        
        if total_score > 20:
            recommendation['signal'] = 'ACHAT FORT'
            recommendation['confidence'] = min(90, 50 + total_score)
            recommendation['entry_points'].append(round(current_price * 0.98, 2))
            recommendation['stop_loss'] = round(current_price * 0.95, 2)
            recommendation['take_profit'] = round(current_price * 1.10, 2)
        elif total_score > 5:
            recommendation['signal'] = 'ACHAT'
            recommendation['confidence'] = min(80, 50 + total_score)
            recommendation['entry_points'].append(round(current_price * 0.99, 2))
            recommendation['stop_loss'] = round(current_price * 0.96, 2)
            recommendation['take_profit'] = round(current_price * 1.08, 2)
        elif total_score < -20:
            recommendation['signal'] = 'VENTE FORTE'
            recommendation['confidence'] = min(90, 50 + abs(total_score))
            recommendation['entry_points'].append(round(current_price * 1.02, 2))
            recommendation['stop_loss'] = round(current_price * 1.05, 2)
            recommendation['take_profit'] = round(current_price * 0.90, 2)
        elif total_score < -5:
            recommendation['signal'] = 'VENTE'
            recommendation['confidence'] = min(80, 50 + abs(total_score))
            recommendation['entry_points'].append(round(current_price * 1.01, 2))
            recommendation['stop_loss'] = round(current_price * 1.04, 2)
            recommendation['take_profit'] = round(current_price * 0.92, 2)
        else:
            recommendation['signal'] = 'ATTENDRE'
            recommendation['confidence'] = 50
            recommendation['analysis'].append("⏸️ Pas de signal clair - attendre un meilleur setup")
        
        return recommendation
    except Exception as e:
        return {'error': str(e)}

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50

# Routes

@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['email'] = user['email']
                session['theme'] = user['theme']
                
                # Update last login
                cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                             (datetime.now().isoformat(), user['id']))
                conn.commit()
                
                conn.close()
                
                if request.is_json:
                    return jsonify({'success': True, 'redirect': url_for('dashboard')})
                return redirect(url_for('dashboard'))
            
            conn.close()
        
        if request.is_json:
            return jsonify({'success': False, 'message': 'Email ou mot de passe incorrect'}), 401
        return render_template('login.html', error='Email ou mot de passe incorrect')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        preferred_currency = data.get('preferred_currency', 'EUR')
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append("Le nom d'utilisateur doit contenir au moins 3 caractères")
        
        if not email or '@' not in email:
            errors.append("Email invalide")
        
        if not password or len(password) < 6:
            errors.append("Le mot de passe doit contenir au moins 6 caractères")
        
        if password != confirm_password:
            errors.append("Les mots de passe ne correspondent pas")
        
        if errors:
            if request.is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            return render_template('register.html', error=', '.join(errors))
        
        # Check if user already exists
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                conn.close()
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Cet email est déjà utilisé'}), 400
                return render_template('register.html', error='Cet email est déjà utilisé')
            
            # Create new user
            try:
                hashed_password = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO users 
                    (username, email, password, preferred_currency, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, email, hashed_password, preferred_currency, datetime.now().isoformat()))
                
                conn.commit()
                user_id = cursor.lastrowid
                conn.close()
                
                # Auto-login after registration
                session['user_id'] = user_id
                session['username'] = username
                session['email'] = email
                session['theme'] = 'dark'
                
                if request.is_json:
                    return jsonify({'success': True, 'redirect': url_for('dashboard')})
                return redirect(url_for('dashboard'))
                
            except Exception as e:
                conn.close()
                if request.is_json:
                    return jsonify({'success': False, 'message': str(e)}), 500
                return render_template('register.html', error=f"Erreur lors de la création du compte: {str(e)}")
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    stats = {
        'net_worth': 0,
        'monthly_cashflow': 0,
        'expense_ratio': 0,
        'savings_rate': 0,
        'total_revenue': 0,
        'total_expenses': 0,
        'trader_score': 0
    }
    
    if conn:
        cursor = conn.cursor()
        
        # Get financial stats
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN type = 'revenue' THEN amount ELSE 0 END) as total_revenue,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses
            FROM financial_transactions
            WHERE user_id = ? AND date >= date('now', '-30 days')
        """, (user_id,))
        
        result = cursor.fetchone()
        if result:
            stats['total_revenue'] = result['total_revenue'] or 0
            stats['total_expenses'] = result['total_expenses'] or 0
            stats['monthly_cashflow'] = stats['total_revenue'] - stats['total_expenses']
            
            if stats['total_revenue'] > 0:
                stats['expense_ratio'] = (stats['total_expenses'] / stats['total_revenue']) * 100
                stats['savings_rate'] = 100 - stats['expense_ratio']
        
        # Get trading value
        cursor.execute("""
            SELECT SUM(quantity * current_price) as portfolio_value
            FROM positions
            WHERE user_id = ? AND status = 'open'
        """, (user_id,))
        
        result = cursor.fetchone()
        portfolio_value = result['portfolio_value'] or 0
        
        stats['net_worth'] = stats['monthly_cashflow'] + portfolio_value
        
        # Get latest trader score
        cursor.execute("""
            SELECT overall_score FROM trader_scores
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))
        
        result = cursor.fetchone()
        if result:
            stats['trader_score'] = result['overall_score']
        
        # Get recent transactions
        cursor.execute("""
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        """, (user_id,))
        recent_transactions = [dict(row) for row in cursor.fetchall()]
        
        # Get unread notifications
        cursor.execute("""
            SELECT COUNT(*) as unread FROM notifications
            WHERE user_id = ? AND is_read = 0
        """, (user_id,))
        unread_notifications = cursor.fetchone()['unread']
        
        conn.close()
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             transactions=recent_transactions,
                             unread_notifications=unread_notifications)
    
    return render_template('dashboard.html', stats=stats, transactions=[], unread_notifications=0)

@app.route('/finances')
@login_required
def finances():
    """Financial management page"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    transactions = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM financial_transactions
            WHERE user_id = ?
            ORDER BY date DESC, time DESC
            LIMIT 100
        """, (user_id,))
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    # --- CALCUL DES STATISTIQUES (Correction) ---
    # On filtre les transactions par type 'income' pour les revenus
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    
    stats = {
        'total_revenue': total_income,
        'total_expenses': total_expenses,
        'balance': total_income - total_expenses
    }
    # --------------------------------------------

    return render_template('finances.html', transactions=transactions, stats=stats)

@app.route('/api/financial-transaction', methods=['POST'])
@login_required
def add_financial_transaction():
    """Add new financial transaction"""
    data = request.get_json()
    user_id = session['user_id']
    
    required_fields = ['type', 'category', 'reason', 'amount', 'date', 'time']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Champs requis manquants'}), 400
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO financial_transactions 
                (user_id, type, category, subcategory, reason, usage, amount, currency, 
                 date, time, payment_method, reference, status, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                data['type'],
                data['category'],
                data.get('subcategory'),
                data['reason'],
                data.get('usage'),
                float(data['amount']),
                data.get('currency', 'EUR'),
                data['date'],
                data['time'],
                data.get('payment_method'),
                data.get('reference'),
                data.get('status', 'completed'),
                data.get('notes'),
                data.get('tags')
            ))
            
            conn.commit()
            transaction_id = cursor.lastrowid
            
            # Create notification for large transactions
            if float(data['amount']) > 1000:
                cursor.execute("""
                    INSERT INTO notifications (user_id, type, title, message)
                    VALUES (?, 'info', 'Transaction importante', ?)
                """, (user_id, f"Transaction de {data['amount']}€ enregistrée"))
                conn.commit()
            
            conn.close()
            return jsonify({'success': True, 'id': transaction_id})
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify({'success': False, 'message': 'Erreur de connexion'}), 500

@app.route('/journal')
@login_required
def trading_journal():
    """Trading journal with images"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    entries = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM trading_journal
            WHERE user_id = ?
            ORDER BY date DESC, time DESC
        """, (user_id,))
        entries = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    return render_template('trading_journal.html', entries=entries)

@app.route('/api/journal-entry', methods=['POST'])
@login_required
def add_journal_entry():
    """Add trading journal entry with optional image"""
    user_id = session['user_id']
    
    # Handle file upload
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = filepath
    
    # Get form data
    data = request.form if not request.is_json else request.get_json()
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO trading_journal 
                (user_id, symbol, date, time, type, quantity, entry_price, exit_price, 
                 profit_loss, strategy, setup_description, emotions, mistakes, 
                 lessons_learned, notes, image_path, market_conditions, risk_reward_ratio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                data.get('symbol'),
                data.get('date'),
                data.get('time'),
                data.get('type'),
                float(data.get('quantity', 0)),
                float(data.get('entry_price', 0)),
                float(data.get('exit_price', 0)) if data.get('exit_price') else None,
                float(data.get('profit_loss', 0)) if data.get('profit_loss') else None,
                data.get('strategy'),
                data.get('setup_description'),
                data.get('emotions'),
                data.get('mistakes'),
                data.get('lessons_learned'),
                data.get('notes'),
                image_path,
                data.get('market_conditions'),
                float(data.get('risk_reward_ratio', 0)) if data.get('risk_reward_ratio') else None
            ))
            
            entry_id = cursor.lastrowid
            
            # Analyze the trade if image provided
            if image_path:
                trade_data = {
                    'profit_loss': float(data.get('profit_loss', 0)) if data.get('profit_loss') else None,
                    'risk_reward_ratio': float(data.get('risk_reward_ratio', 0)) if data.get('risk_reward_ratio') else None,
                    'strategy': data.get('strategy')
                }
                analysis = analyze_trade_image(image_path, trade_data)
                
                # Save analysis
                cursor.execute("""
                    INSERT INTO ai_analysis (user_id, analysis_type, subject, insights)
                    VALUES (?, 'trading', ?, ?)
                """, (user_id, f"Journal Entry #{entry_id}", json.dumps(analysis)))
            
            conn.commit()
            conn.close()
            
            if request.is_json:
                return jsonify({'success': True, 'id': entry_id})
            return redirect(url_for('trading_journal'))
        
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify({'success': False, 'message': 'Erreur de connexion'}), 500

@app.route('/trading')
@login_required
def trading():
    """Trading interface"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    positions = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM positions
            WHERE user_id = ? AND status = 'open'
            ORDER BY created_at DESC
        """, (user_id,))
        positions = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    return render_template('trading.html', positions=positions)

@app.route('/api/execute-trade', methods=['POST'])
@login_required
def execute_trade():
    """Execute trade"""
    data = request.get_json()
    user_id = session['user_id']
    
    required_fields = ['symbol', 'type', 'quantity', 'price']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'message': 'Champs requis manquants'}), 400
    
    symbol = data['symbol'].upper()
    trade_type = data['type']
    quantity = float(data['quantity'])
    price = float(data['price'])
    fees = float(data.get('fees', 0))
    strategy = data.get('strategy')
    
    amount = quantity * price
    
    if trade_type == 'sell':
        amount = amount - fees
    else:
        amount = -(amount + fees)
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Insert transaction
            cursor.execute("""
                INSERT INTO transactions (user_id, symbol, type, quantity, price, amount, fees, strategy, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, symbol, trade_type, quantity, price, amount, fees, strategy, datetime.now().isoformat()))
            
            # Update positions
            if trade_type == 'buy':
                cursor.execute("""
                    SELECT * FROM positions 
                    WHERE user_id = ? AND symbol = ? AND status = 'open'
                """, (user_id, symbol))
                existing_position = cursor.fetchone()
                
                if existing_position:
                    new_quantity = existing_position['quantity'] + quantity
                    new_avg_price = ((existing_position['quantity'] * existing_position['avg_price']) + 
                                   (quantity * price)) / new_quantity
                    
                    cursor.execute("""
                        UPDATE positions 
                        SET quantity = ?, avg_price = ?, updated_at = ?
                        WHERE user_id = ? AND symbol = ? AND status = 'open'
                    """, (new_quantity, new_avg_price, datetime.now().isoformat(), user_id, symbol))
                else:
                    cursor.execute("""
                        INSERT INTO positions (user_id, symbol, quantity, avg_price, current_price, status)
                        VALUES (?, ?, ?, ?, ?, 'open')
                    """, (user_id, symbol, quantity, price, price))
            else:  # sell
                cursor.execute("""
                    UPDATE positions 
                    SET quantity = quantity - ?, updated_at = ?
                    WHERE user_id = ? AND symbol = ? AND status = 'open'
                """, (quantity, datetime.now().isoformat(), user_id, symbol))
            
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Transaction exécutée avec succès'})
        
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify({'success': False, 'message': 'Erreur de connexion'}), 500

@app.route('/portfolio')
@login_required
def portfolio():
    """Portfolio management with enhanced structure"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    positions = []
    portfolio_stats = {
        'total_value': 0,
        'total_cost': 0,
        'total_pnl': 0,
        'total_pnl_percent': 0,
        'best_performer': None,
        'worst_performer': None
    }
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM positions
            WHERE user_id = ? AND status = 'open'
            ORDER BY (quantity * current_price) DESC
        """, (user_id,))
        positions = [dict(row) for row in cursor.fetchall()]
        
        # Calculate portfolio statistics
        for pos in positions:
            pos['market_value'] = pos['quantity'] * pos['current_price']
            pos['cost_basis'] = pos['quantity'] * pos['avg_price']
            pos['pnl'] = pos['market_value'] - pos['cost_basis']
            pos['pnl_percent'] = (pos['pnl'] / pos['cost_basis'] * 100) if pos['cost_basis'] > 0 else 0
            
            portfolio_stats['total_value'] += pos['market_value']
            portfolio_stats['total_cost'] += pos['cost_basis']
            portfolio_stats['total_pnl'] += pos['pnl']
        
        if portfolio_stats['total_cost'] > 0:
            portfolio_stats['total_pnl_percent'] = (portfolio_stats['total_pnl'] / 
                                                   portfolio_stats['total_cost'] * 100)
        
        # Find best and worst performers
        if positions:
            positions_sorted = sorted(positions, key=lambda x: x['pnl_percent'], reverse=True)
            portfolio_stats['best_performer'] = positions_sorted[0]
            portfolio_stats['worst_performer'] = positions_sorted[-1]
        
        conn.close()
    
    return render_template('portfolio.html', 
                         positions=positions, 
                         stats=portfolio_stats)

@app.route('/ai-assistant')
@login_required
def ai_assistant():
    """AI Assistant conversational page"""
    return render_template('ai_assistant.html')

@app.route('/api/ai-chat', methods=['POST'])
@login_required
def ai_chat():
    """AI conversational assistant endpoint"""
    data = request.get_json()
    user_id = session['user_id']
    question = data.get('question', '').lower()
    
    conn = get_db_connection()
    response = {
        'answer': '',
        'data': None,
        'charts': []
    }
    
    if conn:
        cursor = conn.cursor()
        
        # Analyze question and provide intelligent response
        if 'pourquoi' in question and ('perdu' in question or 'perte' in question):
            # Why did I lose money this month?
            cursor.execute("""
                SELECT 
                    symbol,
                    SUM(CASE WHEN type = 'sell' THEN amount ELSE 0 END) as total_sell,
                    SUM(CASE WHEN type = 'buy' THEN amount ELSE 0 END) as total_buy,
                    COUNT(*) as trade_count
                FROM transactions
                WHERE user_id = ? AND created_at >= date('now', '-30 days')
                GROUP BY symbol
                HAVING (total_sell + total_buy) < 0
                ORDER BY (total_sell + total_buy) ASC
            """, (user_id,))
            
            losing_trades = [dict(row) for row in cursor.fetchall()]
            
            if losing_trades:
                total_loss = sum(t['total_sell'] + t['total_buy'] for t in losing_trades)
                response['answer'] = f"Vous avez perdu {abs(total_loss):.2f}€ ce mois-ci. "
                response['answer'] += f"Les principales pertes proviennent de: "
                response['answer'] += ", ".join([f"{t['symbol']} ({t['total_sell'] + t['total_buy']:.2f}€)" 
                                                for t in losing_trades[:3]])
                response['data'] = losing_trades
            else:
                response['answer'] = "Vous n'avez pas enregistré de pertes ce mois-ci. Bravo!"
        
        elif 'stratégie' in question and ('rentable' in question or 'meilleur' in question):
            # Which strategy is most profitable?
            cursor.execute("""
                SELECT 
                    strategy,
                    COUNT(*) as trade_count,
                    SUM(amount) as total_profit,
                    AVG(amount) as avg_profit,
                    SUM(CASE WHEN amount > 0 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) as losses
                FROM transactions
                WHERE user_id = ? AND strategy IS NOT NULL AND type = 'sell'
                GROUP BY strategy
                ORDER BY total_profit DESC
            """, (user_id,))
            
            strategies = [dict(row) for row in cursor.fetchall()]
            
            if strategies:
                best = strategies[0]
                win_rate = (best['wins'] / best['trade_count'] * 100) if best['trade_count'] > 0 else 0
                
                response['answer'] = f"Votre meilleure stratégie est '{best['strategy']}' avec:\n"
                response['answer'] += f"• Profit total: {best['total_profit']:.2f}€\n"
                response['answer'] += f"• {best['trade_count']} trades\n"
                response['answer'] += f"• Taux de réussite: {win_rate:.1f}%\n"
                response['answer'] += f"• Profit moyen: {best['avg_profit']:.2f}€"
                response['data'] = strategies
            else:
                response['answer'] = "Vous n'avez pas encore de données de stratégie enregistrées."
        
        elif 'score' in question or 'performance' in question:
            # What's my trader score?
            score_data = calculate_trader_score(user_id)
            
            response['answer'] = f"Votre score de trader est: {score_data['overall_score']:.1f}/100\n\n"
            response['answer'] += "Détails:\n"
            response['answer'] += f"• Rentabilité: {score_data['profitability_score']:.1f}/100\n"
            response['answer'] += f"• Gestion du risque: {score_data['risk_management_score']:.1f}/100\n"
            response['answer'] += f"• Discipline: {score_data['discipline_score']:.1f}/100\n"
            response['answer'] += f"• Cohérence stratégique: {score_data['strategy_consistency_score']:.1f}/100\n"
            response['answer'] += f"• Contrôle émotionnel: {score_data['emotional_control_score']:.1f}/100"
            
            if score_data['overall_score'] < 50:
                response['answer'] += "\n\n⚠️ Votre score est faible. Concentrez-vous sur la discipline et la gestion du risque."
            elif score_data['overall_score'] < 70:
                response['answer'] += "\n\n📈 Bon début ! Travaillez sur la cohérence de vos stratégies."
            else:
                response['answer'] += "\n\n✅ Excellent score ! Continuez ainsi!"
            
            response['data'] = score_data
        
        elif 'combien' in question and ('gagn' in question or 'perdu' in question):
            # How much did I make/lose?
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_gains,
                    SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_losses,
                    SUM(amount) as net_profit
                FROM transactions
                WHERE user_id = ? AND type = 'sell'
            """, (user_id,))
            
            result = cursor.fetchone()
            
            if result and result['total_gains']:
                response['answer'] = f"Résultats de trading:\n"
                response['answer'] += f"• Gains totaux: {result['total_gains']:.2f}€\n"
                response['answer'] += f"• Pertes totales: {result['total_losses']:.2f}€\n"
                response['answer'] += f"• Profit net: {result['net_profit']:.2f}€"
                
                if result['net_profit'] > 0:
                    response['answer'] += "\n\n✅ Vous êtes profitable!"
                else:
                    response['answer'] += "\n\n⚠️ Vous êtes en perte. Analysez vos trades."
            else:
                response['answer'] = "Vous n'avez pas encore de trades fermés."
        
        elif 'problème' in question or 'erreur' in question:
            # What are my problems?
            patterns = analyze_trading_psychology(user_id)
            
            if patterns:
                response['answer'] = f"J'ai détecté {len(patterns)} problèmes:\n\n"
                for i, pattern in enumerate(patterns[:5], 1):
                    response['answer'] += f"{i}. {pattern['type'].upper()} ({pattern['severity']})\n"
                    response['answer'] += f"   {pattern['description']}\n"
                    response['answer'] += f"   💡 {pattern['recommendation']}\n\n"
                response['data'] = patterns
            else:
                response['answer'] = "Aucun problème majeur détecté. Continuez votre bon travail!"
        
        elif 'conseil' in question or 'recommandation' in question:
            # Give me advice
            patterns = analyze_trading_psychology(user_id)
            score_data = calculate_trader_score(user_id)
            
            response['answer'] = "Recommandations personnalisées:\n\n"
            
            if score_data['discipline_score'] < 60:
                response['answer'] += "1. 📋 Discipline: Créez un plan de trading et suivez-le strictement\n"
            
            if score_data['risk_management_score'] < 60:
                response['answer'] += "2. 🛡️ Risque: Utilisez toujours des stop-loss (max 2% par trade)\n"
            
            if score_data['emotional_control_score'] < 60:
                response['answer'] += "3. 🧘 Émotions: Prenez une pause après 2 pertes consécutives\n"
            
            if patterns:
                response['answer'] += f"4. ⚠️ Attention: Vous montrez des signes de {patterns[0]['type']}\n"
            
            response['answer'] += "\n💡 Conseil du jour: Tenez un journal de trading détaillé pour identifier vos patterns."
        
        else:
            response['answer'] = "Je peux vous aider avec:\n"
            response['answer'] += "• 'Pourquoi j'ai perdu ce mois-ci?'\n"
            response['answer'] += "• 'Quelle est ma meilleure stratégie?'\n"
            response['answer'] += "• 'Quel est mon score?'\n"
            response['answer'] += "• 'Quels sont mes problèmes?'\n"
            response['answer'] += "• 'Donne-moi des conseils'\n"
            response['answer'] += "• 'Combien j'ai gagné/perdu?'"
        
        conn.close()
    
    return jsonify(response)

@app.route('/analysis')
@login_required
def analysis():
    """Analysis and insights page"""
    user_id = session['user_id']
    
    # Calculate scores and patterns
    trader_score = calculate_trader_score(user_id)
    patterns = analyze_trading_psychology(user_id)
    
    conn = get_db_connection()
    recent_analyses = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ai_analysis
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        """, (user_id,))
        recent_analyses = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    return render_template('analysis.html', 
                         trader_score=trader_score,
                         patterns=patterns,
                         analyses=recent_analyses)

@app.route('/api/analyze-finances', methods=['POST'])
@login_required
def analyze_finances():
    """Analyze financial data"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Get financial data
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN type = 'revenue' THEN amount ELSE 0 END) as revenue,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
            FROM financial_transactions
            WHERE user_id = ? AND date >= date('now', '-30 days')
        """, (user_id,))
        
        result = cursor.fetchone()
        data = {
            'revenue': result['revenue'] or 0,
            'expenses': result['expenses'] or 0
        }
        
        insights = analyze_financial_report(data)
        
        # Save analysis
        cursor.execute("""
            INSERT INTO ai_analysis (user_id, analysis_type, subject, insights)
            VALUES (?, 'financial', 'Monthly Report', ?)
        """, (user_id, json.dumps(insights)))
        
        conn.commit()
        conn.close()
        
        return jsonify(insights)
    
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/trading-recommendation/<symbol>')
@login_required
def get_trading_recommendation(symbol):
    """Get AI trading recommendation for a symbol"""
    recommendation = trading_recommendation(symbol.upper())
    return jsonify(recommendation)

@app.route('/settings')
@login_required
def settings():
    """User settings page"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    user_settings = {}
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            user_settings = dict(user)
        conn.close()
    
    return render_template('settings.html', settings=user_settings)

@app.route('/api/update-settings', methods=['POST'])
@login_required
def update_settings():
    """Update user settings"""
    data = request.get_json()
    user_id = session['user_id']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            updates = []
            params = []
            
            allowed_fields = ['username', 'email', 'preferred_currency', 'timezone', 
                            'theme', 'notifications_email', 'notifications_app']
            
            for field in allowed_fields:
                if field in data:
                    updates.append(f"{field} = ?")
                    params.append(data[field])
            
            if 'password' in data and data['password']:
                updates.append("password = ?")
                params.append(generate_password_hash(data['password']))
            
            if updates:
                params.append(user_id)
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
                
                # Update session theme
                if 'theme' in data:
                    session['theme'] = data['theme']
            
            conn.close()
            return jsonify({'success': True, 'message': 'Paramètres mis à jour'})
        
        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify({'success': False, 'message': 'Erreur de connexion'}), 500

@app.route('/notifications')
@login_required
def notifications():
    """Notifications page"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    notifications_list = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (user_id,))
        notifications_list = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    return render_template('notifications.html', notifications=notifications_list)

@app.route('/api/mark-notification-read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark notification as read"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE notifications SET is_read = 1
            WHERE id = ? AND user_id = ?
        """, (notification_id, user_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 500

@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    reports_list = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM reports
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        reports_list = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    return render_template('reports.html', reports=reports_list)

@app.route('/api/generate-report', methods=['POST'])
@login_required
def generate_report():
    """Generate financial report"""
    data = request.get_json()
    user_id = session['user_id']
    
    report_type = data.get('type', 'monthly')
    period_start = data.get('start')
    period_end = data.get('end')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # Get financial data for period
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN type = 'revenue' THEN amount ELSE 0 END) as revenue,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
            FROM financial_transactions
            WHERE user_id = ? AND date BETWEEN ? AND ?
        """, (user_id, period_start, period_end))
        
        result = cursor.fetchone()
        revenue = result['revenue'] or 0
        expenses = result['expenses'] or 0
        profit = revenue - expenses
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        # Create report
        cursor.execute("""
            INSERT INTO reports 
            (user_id, title, report_type, period_start, period_end, revenue, expenses, profit, profit_margin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            f"Rapport {report_type} - {period_start} à {period_end}",
            report_type,
            period_start,
            period_end,
            revenue,
            expenses,
            profit,
            profit_margin
        ))
        
        conn.commit()
        report_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'success': True, 'report_id': report_id})
    
    return jsonify({'success': False}), 500

@app.route('/history')
@login_required
def history():
    """Transaction history"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    transactions = []
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 200
        """, (user_id,))
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
    
    return render_template('history.html', transactions=transactions)

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run the application
    print("=" * 60)
    print("🚀 Kengni Finance v3.0 - Démarrage")
    print("=" * 60)
    print("📊 Application de gestion financière et trading avec IA")
    print("🌐 URL: http://kengni.fabrice.com")
    print("👤 Email: fabrice.kengni@icloud.com")
    print("🔐 Password: MdPFort")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
