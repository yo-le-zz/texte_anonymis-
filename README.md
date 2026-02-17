# ✏️ Reformulateur de Texte

> Permet d’anonymiser un texte en changeant le style d’écriture et en corrigeant les fautes d’orthographe.  
> Fonctionne en français et en anglais. Une connexion internet est nécessaire pour la correction grammaticale.

<p align="center">
  <img src="assets/banner.png" alt="Reformulateur de Texte Banner" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square" alt="Python"/>
  <img src="https://img.shields.io/badge/plateforme-Windows%2FLinux-0078d7?style=flat-square" alt="Plateforme"/>
  <img src="https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square" alt="License"/>
</p>

---

## ✨ Fonctionnalités

| Fonctionnalité | Détail |
|---|---|
| 📝 **Correction grammaticale** | Corrige fautes d’orthographe et de grammaire (fr/en) |
| 🎨 **Anonymisation du style** | Change le style pour neutraliser l’écriture originale |
| 🔄 **Reformulation** | Traduction aller-retour via MarianMT pour reformuler chaque phrase |
| 🗂️ **Support multilingue** | Français et anglais |
| 📊 **Comparaison texte** | Affiche texte original vs texte reformulé et stats de mots |
| 💾 **Sauvegarde** | Enregistrement local du résultat dans un fichier texte |

---

## 🖥️ Interface

==============================================
REFORMULATEUR DE TEXTE — 100% Local & Gratuit

🌐 Langue :
[1] Français (défaut)
[2] Anglais

📝 Collez votre texte
Tapez FIN seul sur une ligne pour valider

✨ Le texte sera corrigé et reformulé
📊 Affichage du texte original et du texte final
💾 Option pour sauvegarder le résultat


---

## 🚀 Installation rapide

### Installation manuelle

```bash
# Cloner le dépôt
git clone https://github.com/yo-le-zz/Reformulateur_texte.git
cd Reformulateur_texte

# Installer les dépendances
pip install -r requirements.txt

# Lancer le script
python src/main.py
```

# Compilation en exécutable avec Nuitka (Windows)
python -m nuitka --standalone --remove-output --output-dir=dist --output-filename=texte_anonymise \
--windows-icon-from-ico=assets/icon.ico \
--include-package=transformers \
--include-package=torch \
--include-package=language_tool_python \
--include-package=sentencepiece \
--include-package=huggingface_hub \
--include-package=filelock \
--include-package=numpy \
--include-package=regex \
--include-package=requests \
--include-package=tqdm \
--include-package=packaging \
--nofollow-import-to=transformers.cli \
--nofollow-import-to=transformers.commands \
--nofollow-import-to=transformers.utils.fx \
--assume-yes-for-downloads \
--windows-console-mode=attach \
--include-data-files=assets/icon.ico=assets/icon.ico src/main.py
## ⚠️ La première compilation télécharge les modèles MarianMT (~300 Mo).

# 📦 Dépendances
accelerate==1.12.0
annotated-doc==0.0.4
anyio==4.12.1
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
colorama==0.4.6
filelock==3.24.2
fsspec==2026.2.0
h11==0.16.0
hf-xet==1.2.0
httpcore==1.0.9
httpx==0.28.1
huggingface_hub==1.4.1
idna==3.11
Jinja2==3.1.6
language_tool_python==3.2.2
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
mpmath==1.3.0
networkx==3.6.1
Nuitka==4.0.1
numpy==2.4.2
packaging==26.0
psutil==7.2.2
Pygments==2.19.2
PyYAML==6.0.3
regex==2026.1.15
requests==2.32.5
rich==14.3.2
safetensors==0.7.0
sentencepiece==0.2.1
shellingham==1.5.4
sympy==1.14.0
tokenizers==0.22.2
toml==0.10.2
torch==2.10.0
tqdm==4.67.3
transformers==5.2.0
typer==0.24.0
typer-slim==0.24.0
typing_extensions==4.15.0
urllib3==2.6.3

# 🛠️ Fonctionnement

  1. Correction grammaticale : le texte est corrigé automatiquement.

  2. Découpage en phrases : chaque phrase est isolée.

  3. Reformulation : traduction aller-retour pour anonymiser le style.

  4. Post-traitement : nettoyage des espaces et ponctuation.

# 📖 Exemple d’utilisation
  ➤ Langue : Français
  ➤ Texte :
     ok merci mais c'etait just pour modifier votre message d'annonce pour plus d'info
     FIN
  
  ✅ Texte reformulé :
     Merci, c'était simplement pour apporter une modification à votre message d'annonce afin de fournir plus d'informations.

# 📄 Licence

Ce projet est distribué sous licence MIT.

# 👤 Auteur
yo-le-zz
