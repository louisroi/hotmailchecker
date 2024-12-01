# 🎮 Guide d'Utilisation de Hotmail Checker<br><br>
## 🚀 Prérequis

Assurez-vous d'avoir les éléments suivants :

Python 3.x
Vérifiez l'installation de Python en utilisant la commande suivante :

    python --version

Bibliothèques Requises
Installez les bibliothèques nécessaires avec pip :

    pip install requests selenium colorama

WebDriver pour Firefox
Téléchargez GeckoDriver et assurez-vous qu'il est accessible dans votre PATH.

Vous pouvez télécharger GeckoDriver ici :
https://github.com/mozilla/geckodriver/releases
## Fichier JSON des Identifiants

Assurez-vous que le fichier combo.json est bien formaté comme suit :

    [
        {"email": "user1@example.com", "password": "password1"},
        {"email": "user2@example.com", "password": "password2"}
    ]

Le fichier combo.json contient la liste des identifiants à tester.

## 🏁 Étapes pour Exécuter le Script

Télécharger le Script

Clonez le dépôt GitHub ou téléchargez directement le fichier Python du script.
2. Ouvrir votre Terminal

Naviguez jusqu'au dossier où se trouve le script.
3. Lancer le Script

Exécutez la commande suivante pour démarrer le script :

    python hotmailchecker.py

Le script vérifiera automatiquement si une nouvelle version est disponible. Si une mise à jour est trouvée, elle sera téléchargée et le script sera redémarré.
4. Sélectionner le Fichier combo.json

Une fenêtre de dialogue apparaîtra. Sélectionnez le fichier combo.json contenant les identifiants à tester.
5. Vérification des Identifiants

Le script tentera de se connecter à Hotmail avec les identifiants fournis en utilisant les proxies configurés. Les résultats de chaque tentative seront affichés dans le terminal. Chaque email et mot de passe réussi sera enregistré dans un fichier hit.txt.
6. Gestion des Proxies

Le script utilise une liste de proxies prédéfinie. Si nécessaire, vous pouvez la personnaliser directement dans le code.
7. Fin de la Vérification

À la fin du processus, le script créera un fichier hit.txt dans le même répertoire, contenant tous les emails et mots de passe qui ont réussi la connexion.
## ⚙️ Résolution des Problèmes
Erreur de Téléchargement

Vérifiez votre connexion Internet.
Assurez-vous que l'URL du téléchargement est accessible.

Fichier JSON Vide

Assurez-vous que le fichier combo.json contient des données valides.
Si le fichier est vide ou mal formaté, le script échouera.

Échec de Connexion

Vérifiez l'exactitude des identifiants dans le fichier combo.json.
Si les proxies sont utilisés, assurez-vous qu'ils fonctionnent correctement.

## 🔒 Remarques
Sécurité

Soyez vigilant lorsque vous utilisez des identifiants pour tester des connexions à des services en ligne. Respectez toujours les conditions d'utilisation des services (comme Hotmail).
Utilisation des Proxies

Vous pouvez modifier la liste des proxies dans le code si vous avez vos propres proxies ou si vous souhaitez en utiliser d'autres.

# Si vous avez besoin d'aide ou avez des questions, n'hésitez pas à me contacter sur Discord ! 😊
