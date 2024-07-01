# POJAT API-REST

## Vue d'ensemble du projet

**Date limite : 30/07/2024**

### Objectif

Développer une API REST avec Flask pour gérer les utilisateurs et les propositions de textes (Prompts). L'API doit inclure des fonctionnalités de gestion des connexions et des autorisations.

## Description fonctionnelle

### Rôles et fonctionnalités

**Administrateur :**
- Peut créer des utilisateurs individuels ou des groupes d'utilisateurs.
- Valide, demande la modification ou supprime des Prompts.
- Peut voir tous les Prompts mais ne peut ni voter ni noter.

**Utilisateurs :**
- Proposent des Prompts à vendre.
- Peuvent voter pour l'activation des Prompts en attente de validation.
- Peuvent noter les Prompts activés, mais ne peuvent ni voter ni noter leurs propres Prompts.
- Les membres d'un même groupe ont un impact plus fort sur la note et les votes.

**Visiteur (n'a pas besoin de se connecter) :**
- Peut consulter un Prompt.
- Peut rechercher un Prompt par son contenu ou par mots-clés.
- Peut acheter un Prompt.

### Gestion des Prompts

- Les Prompts ont un prix par défaut de 1000 F CFA.
- La note des Prompts est comprise entre -10 et +10.
- La note d'un membre du même groupe compte pour 60 %.
- La note d'un membre extérieur au groupe compte pour 40 %.
- Le prix des Prompts est recalculé après chaque notation avec la formule :
  `Nouveau prix = 1000 * (1 + moyenne des notes)`.

### États des Prompts

- **En attente :** Lors de l'ajout d'un Prompt par un utilisateur.
- **Activé :** Après validation par un administrateur ou par vote.
- **À revoir :** Si l'administrateur demande une modification.
- **Rappel :** Si aucune action n'est prise par l'administrateur dans les deux jours suivant l'ajout ou une demande de suppression/modification.
- **À supprimer :** Lorsque l'utilisateur demande la suppression de son propre Prompt.

### Processus de gestion des Prompts

- Les membres peuvent voter pour l'activation des Prompts en état de Rappel.
- Un vote d'un membre du groupe compte pour 2 points.
- Un vote d'un membre extérieur au groupe compte pour 1 point.
- Le Prompt est activé s'il atteint au moins 6 points.
- Un administrateur peut valider ou supprimer un Prompt à tout moment.
- Les utilisateurs peuvent demander la suppression de leurs propres Prompts, qui passent alors à l'état À supprimer.
- Si un Prompt reste en état À supprimer pendant plus d'un jour sans action de l'administrateur, il passe à l'état Rappel.

### Autres fonctionnalités

- Les utilisateurs peuvent voir les détails de chaque Prompt.
- Une fois validé ou supprimé, un Prompt ne peut plus être noté.

## Diagrammes et planification

### Maquettage

- Dessin des interfaces pour la gestion des utilisateurs et des Prompts.
- Interface de notation et de vote des Prompts.
- Interface d'administration pour la gestion des états des Prompts.

### Diagramme de cas d'utilisation

- Visualisation des interactions entre les utilisateurs, les administrateurs et le système.
- Inclut les actions principales telles que la création de comptes, la gestion des Prompts, la notation et le vote.

### Diagramme de classe

- Modélisation des entités principales (Utilisateur, Groupe, Prompt) et leurs relations.
- Intégration des états des Prompts et des actions possibles.

### Planification avec Trello

- Création de tableaux de bord avec des sprints et des User Stories (US).
- Organisation des tâches par priorité : gestion des utilisateurs, gestion des Prompts, intégration des règles de notation, etc.

### Création de l'API

- Implémentation des Endpoints REST pour gérer les utilisateurs, les groupes, les Prompts et leurs états.
- Gestion de l'authentification et de l'autorisation.

## Exigences techniques

- Utiliser PostgreSQL pour la base de données.
- Utiliser SQL pour les requêtes.
- Utiliser JWT pour la gestion des connexions et des autorisations.
- Tester l'API avec Postman.