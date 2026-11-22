"""Récupère le dernier paquet de l'Atelier dans Google Drive et le décompresse dans le dépôt.

Variables d'environnement :
  GDRIVE_SA_JSON    clé JSON du compte de service Google (secret GitHub)
  GDRIVE_FOLDER_ID  identifiant du dossier Drive où l'Atelier dépose ses paquets

Le script n'écrit rien si le dernier paquet est déjà celui du dépôt.
Il écrit dans GITHUB_OUTPUT : changed=true|false et message=<résumé pour le commit>.
"""
import io
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

ROOT = Path(__file__).resolve().parent.parent
CONTENUS = ROOT / "contenus"
MARQUEUR = CONTENUS / ".dernier-paquet"


def sortie(cle, valeur):
    chemin = os.environ.get("GITHUB_OUTPUT")
    if chemin:
        with open(chemin, "a", encoding="utf-8") as f:
            if "\n" in valeur:
                f.write(f"{cle}<<FIN\n{valeur}\nFIN\n")
            else:
                f.write(f"{cle}={valeur}\n")
    print(f"{cle}: {valeur}")


def main():
    cle = os.environ.get("GDRIVE_SA_JSON")
    dossier = os.environ.get("GDRIVE_FOLDER_ID")
    if not cle or not dossier:
        sys.exit("GDRIVE_SA_JSON et GDRIVE_FOLDER_ID sont nécessaires (voir docs/acces-google-drive.md).")

    cred = service_account.Credentials.from_service_account_info(
        json.loads(cle), scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    drive = build("drive", "v3", credentials=cred, cache_discovery=False)
    res = drive.files().list(
        q=f"'{dossier}' in parents and trashed = false and name contains 'visites-etat-digital' and mimeType = 'application/zip'",
        orderBy="modifiedTime desc",
        pageSize=1,
        fields="files(id,name,modifiedTime,size)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    fichiers = res.get("files", [])
    if not fichiers:
        sortie("changed", "false")
        print("Aucun paquet dans le dossier Drive.")
        return
    paquet = fichiers[0]
    signature = f"{paquet['name']} ({paquet['modifiedTime']})"
    if MARQUEUR.exists() and MARQUEUR.read_text(encoding="utf-8").strip() == signature:
        sortie("changed", "false")
        print("Le dépôt a déjà ce paquet.")
        return

    tampon = io.BytesIO()
    requete = drive.files().get_media(fileId=paquet["id"], supportsAllDrives=True)
    telechargement = MediaIoBaseDownload(tampon, requete)
    fini = False
    while not fini:
        _, fini = telechargement.next_chunk()
    archive = zipfile.ZipFile(tampon)

    # Un paquet complet remplace les visites présentes : une visite retirée de l'Atelier disparaît aussi ici.
    visites = {n.split("/")[0] for n in archive.namelist() if n.startswith("visite-")}
    complet = "toutes-visites" in paquet["name"]
    CONTENUS.mkdir(exist_ok=True)
    for d in CONTENUS.glob("visite-*"):
        if d.is_dir() and (complet or d.name in visites):
            shutil.rmtree(d)
    for nom in archive.namelist():
        if nom.endswith("/"):
            continue
        cible = ROOT / "schema.json" if nom == "schema.json" else CONTENUS / nom
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_bytes(archive.read(nom))
    MARQUEUR.write_text(signature + "\n", encoding="utf-8")

    lignes = []
    for v in sorted(visites):
        journal = archive.read(f"{v}/CHANGELOG.md").decode("utf-8") if f"{v}/CHANGELOG.md" in archive.namelist() else ""
        chiffres = re.findall(r"- (\d+) (ajout|modification|retrait)", journal)
        resume = ", ".join(f"{n} {m}(s)" for n, m in chiffres) or "paquet reçu"
        lignes.append(f"{v} : {resume}")
    sortie("changed", "true")
    sortie("message", f"Paquet de l'Atelier : {paquet['name']}\n\n" + "\n".join(lignes))


if __name__ == "__main__":
    main()
