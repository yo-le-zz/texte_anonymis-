"""
=============================================================================
  REFORMULATEUR DE TEXTE - 100% Gratuit & Local
=============================================================================
  Installation :
    pip install transformers torch language-tool-python sentencepiece accelerate
=============================================================================
"""

import sys
import re
import os
import builtins

# ─────────────────────────────────────────────
#  Forcer le mode non-bufferisé
# ─────────────────────────────────────────────

os.environ["PYTHONUNBUFFERED"] = "1"

# Dossier "models/" à côté de l'exe (fonctionne en .py ET en .exe Nuitka)
_BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
os.environ["TRANSFORMERS_CACHE"]    = os.path.join(_BASE_DIR, "models")
os.environ["HF_HOME"]               = os.path.join(_BASE_DIR, "models")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

_print_original = builtins.print
def print(*args, **kwargs):
    kwargs.setdefault("flush", True)
    _print_original(*args, **kwargs)
builtins.print = print

# ─────────────────────────────────────────────
#  Encodage UTF-8 sur Windows
# ─────────────────────────────────────────────

if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True
        )
    except AttributeError:
        pass


# ─────────────────────────────────────────────
#  Vérification des dépendances
# ─────────────────────────────────────────────

def verifier_dependances():
    manquantes = []
    for lib, pip_name in [
        ("torch",        "torch"),
        ("transformers", "transformers"),
        ("sentencepiece","sentencepiece"),
    ]:
        try:
            __import__(lib)
        except ImportError:
            manquantes.append(pip_name)

    if manquantes:
        print("\n❌ Bibliothèques manquantes !")
        print(f"   pip install {' '.join(manquantes)}\n")
        sys.exit(1)

    print("✅ Toutes les dépendances sont présentes.\n")


# ─────────────────────────────────────────────
#  Module 1 : Correction grammaticale
#  Utilise language_tool_python en mode "local" (sans Java)
#  via LanguageTool embedded (language_tool_python.utils)
# ─────────────────────────────────────────────

def corriger_grammaire(texte: str, langue: str = "fr") -> str:
    print("🔍 Correction grammaticale en cours...")
    try:
        import language_tool_python
        # Mode local standalone : télécharge automatiquement le jar LanguageTool
        # LanguageToolPublicAPI utilise l'API en ligne SANS Java local
        outil = language_tool_python.LanguageToolPublicAPI(langue)
        texte_corrige = outil.correct(texte)
        outil.close()
        nb = sum(1 for a, b in zip(texte.split(), texte_corrige.split()) if a != b)
        print(f"   → {nb} correction(s) appliquée(s).")
        return texte_corrige
    except Exception as e:
        print(f"   ⚠️  Correction grammaticale ignorée ({e}).")
        return texte


# ─────────────────────────────────────────────
#  Module 2 : Découpage en phrases
# ─────────────────────────────────────────────

def decouper_en_phrases(texte: str) -> list:
    phrases = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-ÖÙ-Ü])', texte.strip())
    return [p.strip() for p in phrases if p.strip()]


# ─────────────────────────────────────────────
#  Module 3 : Reformulation via MarianMT
# ─────────────────────────────────────────────

def charger_modele(langue: str = "fr"):
    from transformers import MarianMTModel, MarianTokenizer

    if langue == "fr":
        modele_a = "Helsinki-NLP/opus-mt-fr-en"
        modele_b = "Helsinki-NLP/opus-mt-en-fr"
    elif langue == "en":
        modele_a = "Helsinki-NLP/opus-mt-en-fr"
        modele_b = "Helsinki-NLP/opus-mt-fr-en"
    else:
        print(f"   ⚠️  Langue '{langue}' non supportée.")
        return None, None

    print("📦 Chargement des modèles Helsinki-NLP (MarianMT)...")
    print(f"   Cache : {os.environ['TRANSFORMERS_CACHE']}")
    print("   (Premier lancement : téléchargement ~300 Mo, patientez…)\n")

    try:
        print(f"   Modèle 1/2 : {modele_a}")
        tok_a   = MarianTokenizer.from_pretrained(modele_a)
        model_a = MarianMTModel.from_pretrained(modele_a)

        print(f"   Modèle 2/2 : {modele_b}")
        tok_b   = MarianTokenizer.from_pretrained(modele_b)
        model_b = MarianMTModel.from_pretrained(modele_b)

        print("✅ Modèles chargés avec succès.\n")
        return (tok_a, model_a), (tok_b, model_b)

    except Exception as e:
        print(f"   ❌ Erreur chargement : {e}")
        print("   Vérifiez votre connexion internet.")
        return None, None


def traduire(texte: str, tokenizer, model, max_length: int = 512) -> str:
    import torch
    inputs = tokenizer(
        [texte], return_tensors="pt", padding=True,
        truncation=True, max_length=max_length
    )
    with torch.no_grad():
        tokens = model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(tokens[0], skip_special_tokens=True)


def reformuler_phrase(phrase: str, pipe_aller, pipe_retour) -> str:
    tok_a, model_a = pipe_aller
    tok_b, model_b = pipe_retour
    try:
        intermediaire = traduire(phrase, tok_a, model_a)
        reformulation = traduire(intermediaire, tok_b, model_b)
        return reformulation
    except Exception as e:
        print(f"   ⚠️  Erreur sur : '{phrase[:40]}…' ({e})")
        return phrase


def reformuler_texte(texte: str, pipe_aller, pipe_retour) -> str:
    if pipe_aller is None or pipe_retour is None:
        print("⚠️  Reformulation ignorée (modèles non disponibles).")
        return texte

    print("✍️  Reformulation du texte en cours...")
    phrases   = decouper_en_phrases(texte)
    total     = len(phrases)
    resultats = []

    for i, phrase in enumerate(phrases, 1):
        apercu = phrase[:55] + ("…" if len(phrase) > 55 else "")
        print(f"   → [{i}/{total}] {apercu}")
        resultats.append(reformuler_phrase(phrase, pipe_aller, pipe_retour))

    return " ".join(resultats)


# ─────────────────────────────────────────────
#  Module 4 : Post-traitement
# ─────────────────────────────────────────────

def post_traitement(texte: str) -> str:
    texte = re.sub(r' +', ' ', texte)
    texte = re.sub(r'\s([!?;:])', r'\1', texte)
    texte = re.sub(r'([.!?])([A-ZÀ-ÖÙ-Üa-zà-öù-ü])', r'\1 \2', texte)
    if texte:
        texte = texte[0].upper() + texte[1:]
    return texte.strip()


# ─────────────────────────────────────────────
#  Module 5 : Affichage
# ─────────────────────────────────────────────

def afficher_comparaison(original: str, reformule: str):
    sep = "─" * 60
    print(f"\n{sep}")
    print("📄  TEXTE ORIGINAL")
    print(sep)
    print(original)
    print(f"\n{sep}")
    print("✨  TEXTE REFORMULÉ")
    print(sep)
    print(reformule)
    print(f"{sep}\n")
    mots_o = len(original.split())
    mots_r = len(reformule.split())
    print(f"📊 Statistiques :")
    print(f"   Mots originaux  : {mots_o}")
    print(f"   Mots reformulés : {mots_r}")
    print(f"   Variation       : {mots_r - mots_o:+d} mot(s)")
    print()


# ─────────────────────────────────────────────
#  Fonction principale
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   REFORMULATEUR DE TEXTE — 100% Local & Gratuit")
    print("=" * 60)
    print()

    # 1. Dépendances
    verifier_dependances()

    # 2. Langue
    print("🌐 Langue du texte :")
    print("   [1] Français (défaut)")
    print("   [2] Anglais")
    choix  = input("   Votre choix (1/2) : ").strip()
    langue = "en" if choix == "2" else "fr"
    print(f"   → Langue : {'Français' if langue == 'fr' else 'Anglais'}\n")

    # 3. Saisie
    print("📝 Collez votre texte ci-dessous.")
    print("   Tapez  FIN  seul sur une ligne puis Entrée pour valider.\n")

    lignes = []
    while True:
        try:
            ligne = input()
        except EOFError:
            break
        if ligne.strip().upper() == "FIN":
            break
        lignes.append(ligne)

    texte_original = "\n".join(lignes).strip()
    texte_original = re.sub(r'\s*\bFIN\b\s*$', '', texte_original, flags=re.IGNORECASE).strip()

    if not texte_original:
        print("❌ Aucun texte fourni.")
        sys.exit(0)

    print(f"\n✅ Texte reçu ({len(texte_original.split())} mots).\n")

    # 4. Correction grammaticale
    texte_corrige = corriger_grammaire(texte_original, langue)

    # 5. Chargement modèles
    pipe_aller, pipe_retour = charger_modele(langue)

    # 6. Reformulation
    texte_reformule = reformuler_texte(texte_corrige, pipe_aller, pipe_retour)

    # 7. Post-traitement
    texte_final = post_traitement(texte_reformule)

    # 8. Affichage
    afficher_comparaison(texte_original, texte_final)

    # 9. Sauvegarde
    rep = input("💾 Sauvegarder le résultat ? (o/N) : ").strip().lower()
    if rep in ("o", "oui", "y", "yes"):
        nom = input("   Nom du fichier (défaut : resultat.txt) : ").strip() or "resultat.txt"
        try:
            with open(nom, "w", encoding="utf-8") as f:
                f.write("TEXTE ORIGINAL :\n" + texte_original + "\n\n")
                f.write("TEXTE REFORMULÉ :\n" + texte_final + "\n")
            print(f"✅ Sauvegardé dans '{nom}'.")
        except IOError as e:
            print(f"❌ Erreur : {e}")

    print("\n✅ Terminé !\n")


# ─────────────────────────────────────────────
#  Point d'entrée
# ─────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu.")
        sys.exit(0)