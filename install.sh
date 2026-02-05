#!/bin/bash
# Kengni Finance v2.0 - Installation Script for Parrot OS
# Enhanced Financial Management & Trading Application with AI

echo "======================================================="
echo "     Kengni Finance v2.0 - Installation"
echo "     Application de Gestion Financière avec IA"
echo "======================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${YELLOW}⚠️  Ce script est optimisé pour Parrot OS/Debian/Ubuntu${NC}"
    read -p "Voulez-vous continuer ? (o/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé.${NC}"
    echo "Installation de Python 3..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

echo -e "${GREEN}✅ Python détecté: $(python3 --version)${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "Installation de pip..."
    sudo apt-get install -y python3-pip
fi

echo -e "${GREEN}✅ Pip détecté: $(pip3 --version)${NC}"

# Create virtual environment
echo ""
echo -e "${YELLOW}📦 Création de l'environnement virtuel...${NC}"
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de la création de l'environnement virtuel${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}📦 Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}📦 Mise à jour de pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${YELLOW}📦 Installation des dépendances...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dépendances installées avec succès${NC}"

# Create necessary directories
echo ""
echo -e "${YELLOW}📁 Création des dossiers nécessaires...${NC}"
mkdir -p static/uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img
mkdir -p templates

echo -e "${GREEN}✅ Dossiers créés${NC}"

# Set permissions
echo -e "${YELLOW}🔒 Configuration des permissions...${NC}"
chmod +x app.py
chmod 755 static/uploads

# Create .env file
echo -e "${YELLOW}🔧 Configuration de l'application...${NC}"
cat > .env << EOF
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
EOF

echo -e "${GREEN}✅ Fichier .env créé${NC}"

# Initialize database
echo ""
echo -e "${YELLOW}🗄️  Initialisation de la base de données...${NC}"
python3 << EOF
from app import init_db
init_db()
print("Base de données initialisée!")
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erreur lors de l'initialisation de la base de données${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Base de données initialisée${NC}"

# Create start script
echo ""
echo -e "${YELLOW}🚀 Création du script de démarrage...${NC}"
CURRENT_DIR=$(pwd)

cat > start_kengni_finance.sh << EOF
#!/bin/bash
cd "$CURRENT_DIR"
source venv/bin/activate
python3 app.py
EOF

chmod +x start_kengni_finance.sh
echo -e "${GREEN}✅ Script de démarrage créé${NC}"

# Create desktop shortcut
echo ""
echo -e "${BLUE}🖥️  Création du raccourci bureau...${NC}"

# Determine desktop directory
if [ -d "$HOME/Desktop" ]; then
    DESKTOP_DIR="$HOME/Desktop"
elif [ -d "$HOME/Bureau" ]; then
    DESKTOP_DIR="$HOME/Bureau"
elif [ -d "$HOME/Escritorio" ]; then
    DESKTOP_DIR="$HOME/Escritorio"
else
    DESKTOP_DIR="$HOME"
    echo -e "${YELLOW}⚠️  Bureau non détecté, création dans le dossier personnel${NC}"
fi

DESKTOP_FILE="$DESKTOP_DIR/KengniFinance.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Kengni Finance
Comment=Application de Gestion Financière avec IA
Exec=bash -c "cd $CURRENT_DIR && source venv/bin/activate && python3 app.py"
Icon=$CURRENT_DIR/static/img/logo.jpeg
Terminal=true
Categories=Office;Finance;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"

# Also create in Applications menu
if [ -d "$HOME/.local/share/applications" ]; then
    cp "$DESKTOP_FILE" "$HOME/.local/share/applications/"
    echo -e "${GREEN}✅ Raccourci ajouté au menu Applications${NC}"
fi

echo -e "${GREEN}✅ Raccourci bureau créé: $DESKTOP_FILE${NC}"

# Create quick launch alias
echo ""
echo -e "${YELLOW}⚡ Configuration du lancement rapide...${NC}"
BASHRC="$HOME/.bashrc"

if ! grep -q "alias kengni-finance" "$BASHRC" 2>/dev/null; then
    echo "" >> "$BASHRC"
    echo "# Kengni Finance Quick Launch" >> "$BASHRC"
    echo "alias kengni-finance='cd $CURRENT_DIR && source venv/bin/activate && python3 app.py'" >> "$BASHRC"
    echo -e "${GREEN}✅ Alias 'kengni-finance' créé${NC}"
    echo -e "${BLUE}   Tapez 'kengni-finance' dans le terminal pour lancer l'app${NC}"
fi

echo ""
echo "======================================================="
echo -e "${GREEN}✅ Installation terminée avec succès !${NC}"
echo "======================================================="
echo ""
echo -e "${YELLOW}Pour démarrer l'application:${NC}"
echo ""
echo -e "${BLUE}Méthode 1 - Double-clic sur le raccourci bureau:${NC}"
echo -e "   📁 $DESKTOP_DIR/KengniFinance.desktop"
echo ""
echo -e "${BLUE}Méthode 2 - Ligne de commande:${NC}"
echo "   1️⃣  Activez l'environnement virtuel:"
echo -e "      ${GREEN}source venv/bin/activate${NC}"
echo ""
echo "   2️⃣  Lancez l'application:"
echo -e "      ${GREEN}python3 app.py${NC}"
echo ""
echo -e "${BLUE}Méthode 3 - Script de démarrage:${NC}"
echo -e "   ${GREEN}./start_kengni_finance.sh${NC}"
echo ""
echo -e "${BLUE}Méthode 4 - Alias rapide (après redémarrage terminal):${NC}"
echo -e "   ${GREEN}kengni-finance${NC}"
echo ""
echo "   3️⃣  Ouvrez votre navigateur:"
echo -e "      ${GREEN}http://localhost:5001${NC}"
echo ""
echo "======================================================="
echo -e "${YELLOW}Identifiants par défaut:${NC}"
echo -e "   Email: ${GREEN}fabrice.kengni@icloud.com${NC}"
echo -e "   Mot de passe: ${GREEN}kengni${NC}"
echo ""
echo -e "${RED}⚠️  IMPORTANT: Changez le mot de passe par défaut!${NC}"
echo -e "${BLUE}💡 Ou créez votre propre compte sur la page d'accueil${NC}"
echo "======================================================="
echo ""
echo -e "${YELLOW}Fonctionnalités:${NC}"
echo "   ✅ Gestion financière complète"
echo "   ✅ Trading avec analyse IA"
echo "   ✅ Journal de trading avec images"
echo "   ✅ Score trader (0-100)"
echo "   ✅ Détection FOMO, Revenge Trading, Overtrading"
echo "   ✅ Assistant IA conversationnel"
echo "   ✅ Thème sombre/clair"
echo "   ✅ Notifications et alertes"
echo "   ✅ Création de comptes personnalisés"
echo ""
echo "======================================================="
echo -e "${GREEN}Bon trading ! 📈💰${NC}"
echo "======================================================="
echo ""
echo -e "${BLUE}📧 Support: fabrice.kengni@icloud.com${NC}"
echo -e "${BLUE}🌐 GitHub: https://github.com/kengni${NC}"
echo ""
