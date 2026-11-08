# Validateur de payload de support

Exemple autonome en Python/Pydantic, réalisé avec assistance IA. Il illustre
une validation de données à expliquer et reproduire en entretien ; ce n'est
pas une fonctionnalité présentée comme déployée chez un client.

## Contrat

`validate_support_payload(payload)` retourne un modèle immuable ou lève
`pydantic.ValidationError`. L'entrée n'est pas modifiée. Le titre et la
description sont des chaînes non vides après suppression des espaces aux
extrémités, limitées respectivement à 120 et 2 000 caractères. La priorité
vaut `low`, `normal` ou `high` (par défaut `normal`). Les champs inconnus et
les types incorrects sont refusés sans conversion implicite.

Ce validateur ne fait ni appel réseau, ni écriture, ni authentification.
Il ne remplace pas l'autorisation, la limitation de débit ou l'échappement
des données lors de leur affichage.

## Exécuter les deux tests

Depuis ce dossier, avec Python 3.10 ou supérieur :

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q -p no:cacheprovider
```

Les deux fonctions de test couvrent une entrée valide, les valeurs limites,
la normalisation répétée, l'immuabilité et treize payloads invalides.
La répétabilité du résultat ne prouve pas l'idempotence d'une transaction
ou d'un appel à un service externe.

## Licence

MIT pour les fichiers de ce dossier uniquement ; voir `LICENSE`.
