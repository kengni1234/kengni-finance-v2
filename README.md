# 🚀 Kengni Finance v2.0 - Application de Gestion Financière & Trading avec IA

![Kengni Finance](static/img/logo.jpeg)

## 📋 Description

Kengni Finance est une application web complète de gestion financière et de trading enrichie par l'Intelligence Artificielle. Elle offre des fonctionnalités avancées d'analyse, de suivi et d'optimisation de vos finances personnelles et de votre activité de trading.

## ✨ Fonctionnalités Principales

### 💰 Gestion Financière
- **Transactions détaillées** : Revenus, Dépenses, Créances, Crédits, Dettes, Investissements
- **Catégorisation avancée** : Catégories, sous-catégories, raisons, usage
- **Tracking complet** : Montant, devise, date, heure, méthode de paiement, références
- **Analyse automatique** : Détection d'anomalies, recommendations IA

### 📈 Trading Professionnel
- **Exécution de trades** : Achat/Vente avec gestion des positions
- **Portfolio en temps réel** : Suivi de performance, P&L, répartition
- **Journal de trading avec images** : Capturez vos charts, ajoutez analyses et émotions
- **Stratégies multiples** : Suivi de cohérence et performance par stratégie

### 🤖 Intelligence Artificielle

#### Score Trader (0-100)
- **Rentabilité** : ROI, win rate, profit factor
- **Gestion du Risque** : Stop-loss, position sizing
- **Discipline** : Overtrading, consistency
- **Cohérence Stratégique** : Utilisation des stratégies
- **Contrôle Émotionnel** : Patterns psychologiques

#### Détection Automatique
- **FOMO** (Fear of Missing Out)
- **Revenge Trading** (Trading de revanche)
- **Overtrading** (Sur-trading)
- **Overconfidence** (Excès de confiance)
- **Analyse émotionnelle** : Peur, avidité

#### Assistant IA Conversationnel
Posez des questions comme :
- "Pourquoi j'ai perdu ce mois-ci ?"
- "Quelle est ma meilleure stratégie ?"
- "Quels sont mes problèmes psychologiques ?"
- "Donne-moi des conseils"

### 📊 Rapports & Analytics
- **Rapports automatiques** : Mensuels, trimestriels, annuels
- **Graphiques interactifs** : Performance, distribution, tendances
- **Export** : CSV, PDF
- **Comparaisons** : Historique, benchmarks

### 🎨 Interface Moderne
- **Thème Sombre/Clair** : Personnalisable
- **Design responsive** : Mobile, tablet, desktop
- **Animations fluides** : UX optimale
- **Logo personnalisé** : Votre identité

### 🔔 Notifications & Alertes
- **Alertes en temps réel** : Transactions importantes, anomalies
- **Notifications email** : Configurable
- **Centre de notifications** : Historique complet

### 👤 Gestion des Comptes
- **Inscription libre** : Créez votre compte personnalisé
- **Multi-utilisateurs** : Chacun ses données
- **Sécurité renforcée** : Mots de passe hashés, sessions sécurisées

## 🛠️ Technologies Utilisées

- **Backend** : Python 3.11+ / Flask 3.0
- **Database** : SQLite
- **Frontend** : HTML5, CSS3, JavaScript
- **Charts** : Chart.js
- **UI Framework** : Bootstrap 5
- **Icons** : Font Awesome 6
- **Data Analysis** : Pandas, NumPy
- **Market Data** : yfinance
- **Image Processing** : Pillow (PIL)

## 📦 Installation sur Parrot OS / Debian / Ubuntu

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel)

### Installation Automatique

```bash
# 1. Extraire l'archive
unzip kengni_finance_v2_complete.zip
cd kengni_finance_v2_complete

# 2. Rendre le script exécutable
chmod +x install.sh

# 3. Lancer l'installation
./install.sh
```

Le script va :
- ✅ Vérifier Python et pip
- ✅ Créer un environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Créer les dossiers nécessaires
- ✅ Initialiser la base de données
- ✅ Créer un raccourci bureau
- ✅ Ajouter un alias de lancement rapide

## 🚀 Lancement de l'Application

### Méthode 1 : Raccourci Bureau (Recommandé)
Double-cliquez sur l'icône **KengniFinance** sur votre bureau

### Méthode 2 : Ligne de commande

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer l'application
python3 app.py
```

### Méthode 3 : Script de démarrage

```bash
./start_kengni_finance.sh
```

### Méthode 4 : Alias rapide

```bash
kengni-finance
```

## 🌐 Accès à l'Application

Une fois lancée, l'application est accessible à :
- **URL** : http://localhost:5001

### Première Connexion

**Option 1 - Créer votre compte** (Recommandé)
1. Cliquez sur "Créer un compte"
2. Remplissez le formulaire d'inscription
3. Configurez vos préférences
4. Commencez à utiliser l'application

**Option 2 - Compte par défaut**
- **Email** : fabrice.kengni@icloud.com
- **Mot de passe** : kengni
- ⚠️ **Important** : Changez le mot de passe dans les paramètres !

## 📁 Structure du Projet

```
kengni_finance_v2_complete/
├── app.py                  # Application Flask principale
├── requirements.txt        # Dépendances Python
├── install.sh             # Script d'installation
├── start_kengni_finance.sh # Script de démarrage
├── README.md              # Ce fichier
├── .env                   # Variables d'environnement (créé à l'installation)
├── kengni_finance.db      # Base de données SQLite (créée au démarrage)
│
├── static/
│   ├── css/              # Feuilles de style personnalisées
│   ├── js/               # Scripts JavaScript
│   ├── img/              # Images et logo
│   │   └── logo.jpeg     # Logo de l'application
│   └── uploads/          # Uploads utilisateurs (charts, etc.)
│
└── templates/
    ├── base.html          # Template de base
    ├── login.html         # Page de connexion
    ├── register.html      # Page d'inscription (NOUVEAU)
    ├── dashboard.html     # Tableau de bord
    ├── finances.html      # Gestion financière
    ├── trading.html       # Interface de trading
    ├── portfolio.html     # Portfolio
    ├── trading_journal.html  # Journal de trading
    ├── ai_assistant.html  # Assistant IA
    ├── analysis.html      # Analyses IA
    ├── reports.html       # Rapports
    ├── history.html       # Historique
    ├── notifications.html # Notifications
    └── settings.html      # Paramètres
```

## 🎯 Utilisation

### 1. Dashboard
- Vue d'ensemble de vos finances et trading
- KPIs principaux : Valeur nette, flux de trésorerie, score trader
- Graphiques de performance
- Transactions récentes

### 2. Gestion Financière
- Ajouter des transactions (revenus, dépenses, etc.)
- Catégoriser et taguer
- Suivre les créances et crédits
- Analyser les tendances

### 3. Trading
- Exécuter des trades (buy/sell)
- Gérer votre portfolio
- Définir stop-loss et take-profit
- Suivre les P&L en temps réel

### 4. Journal de Trading
- Documenter chaque trade
- Uploader des screenshots de charts
- Noter vos émotions et erreurs
- Tirer des leçons
- Analyse IA automatique des images

### 5. Analyse IA
- Consulter votre score trader
- Identifier les patterns psychologiques
- Recevoir des recommandations
- Suivre votre progression

### 6. Assistant IA
- Poser des questions en langage naturel
- Obtenir des insights personnalisés
- Analyser vos performances
- Recevoir des conseils

## 🔧 Configuration

### Paramètres Utilisateur
Dans **Paramètres** (`/settings`), vous pouvez configurer :
- Devise préférée (EUR, USD, etc.)
- Fuseau horaire
- Thème (sombre/clair)
- Notifications (email, app)
- Mot de passe

### Variables d'Environnement
Le fichier `.env` contient :
```env
FLASK_ENV=development
SECRET_KEY=votre_clé_secrète
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 📱 Responsive Design

L'application est entièrement responsive et fonctionne sur :
- 🖥️ Desktop (optimisé pour 1920x1080+)
- 💻 Laptop (optimisé pour 1366x768+)
- 📱 Tablet (optimisé pour iPad)
- 📱 Mobile (optimisé pour iPhone/Android)

## 🔐 Sécurité

- ✅ Mots de passe hashés (Werkzeug)
- ✅ Sessions sécurisées
- ✅ Protection CSRF
- ✅ Validation des uploads
- ✅ Limite de taille de fichiers
- ✅ Sanitization des inputs
- ✅ Isolation des données utilisateurs

## 🛠 Dépannage

### L'application ne démarre pas
```bash
# Vérifier Python
python3 --version

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifier les permissions
chmod +x app.py
```

### Erreur de base de données
```bash
# Supprimer et réinitialiser la DB
rm kengni_finance.db
python3 -c "from app import init_db; init_db()"
```

### Port 5001 déjà utilisé
Modifiez le port dans `app.py` ligne 1702 :
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Changez 5001 en 5002
```

### Le raccourci bureau ne fonctionne pas
```bash
# Rendre le fichier exécutable
chmod +x ~/Desktop/KengniFinance.desktop

# Ou relancer l'installation
./install.sh
```

## 🆘 Support

Pour toute question ou problème :
1. Consultez ce README
2. Vérifiez les logs dans le terminal
3. Contactez : fabrice.kengni@icloud.com

## 📈 Nouveautés v2.0

✨ **Nouvelles Fonctionnalités** :
- 👤 Système d'inscription et de création de comptes
- 🖥️ Raccourci bureau automatique pour Parrot OS
- ⚡ Alias de lancement rapide `kengni-finance`
- 🎨 Page finances complète
- 🔐 Sécurité multi-utilisateurs renforcée
- 📊 Interface améliorée et plus intuitive

## 📊 Roadmap / Améliorations Futures

- [ ] API REST complète
- [ ] Application mobile native
- [ ] Intégration avec exchanges (Binance, Kraken, etc.)
- [ ] Trading automatisé (bots)
- [ ] Backtesting de stratégies
- [ ] Social trading (partage de trades)
- [ ] Dashboard admin
- [ ] Intégration ML avancée
- [ ] Analyse technique automatique
- [ ] Alertes SMS
- [ ] Export vers Excel
- [ ] Import de transactions bancaires

## 📝 Changelog

### Version 2.0.1 (Février 2025)
- ✨ Ajout système d'inscription
- 🖥️ Création automatique de raccourci bureau
- ⚡ Alias de lancement rapide
- 🎨 Page finances complète
- 🔧 Amélioration du script d'installation
- 📚 Documentation enrichie

### Version 2.0 (Février 2025)
- ✨ Refonte complète de l'interface
- 🤖 Ajout de l'Intelligence Artificielle
- 📊 Score Trader (0-100)
- 🧠 Détection patterns psychologiques
- 💬 Assistant IA conversationnel
- 📸 Journal de trading avec images
- 🎨 Thème sombre/clair
- 🔔 Système de notifications
- 📈 Analytics avancés
- 🌐 Support multi-devises

## 👨‍💻 Auteur

**Kengni Finance Team**
- Email: fabrice.kengni@icloud.com
- GitHub: [kengni](https://github.com/kengni)

## 📄 Licence

Ce projet est sous licence privée. Tous droits réservés.

## 🙏 Remerciements

Merci d'utiliser Kengni Finance ! Nous espérons que cette application vous aidera à :
- 💰 Mieux gérer vos finances
- 📈 Améliorer votre trading
- 🧠 Comprendre votre psychologie
- 🚀 Atteindre vos objectifs financiers

**Bon trading ! 📈💰**

---
**Kengni Finance v2.0.1** - © 2025 - Tous droits réservés
# kengni.fabrice
