# 24 hours basket

This app will manage a 24 hours basketball championship

## Installation

Make sure you have installed in your OS
```
make
python3.6
virtualenv
postgresql
```

Create a PostgreSQL database
```
sudo su - postgres
psql
CREATE DATABASE 24hours;
CREATE USER 24hours WITH PASSWORD '24hours';
GRANT ALL PRIVILEGES ON DATABASE 24hours TO 24hours;
ALTER USER 24hours CREATEDB;
```

Then run:
```
make requirements
make virtualenv
source venv/bin/activate
cd src/
./manage.py migrate
```

## Run tests

Run `make tests`. It will do isort-check, lint and django tests.

## Utils

Update packages: `make requirements`. Creates a requirements.txt file with the last versions of the packages inside requirements/base.txt. You can run it whenever you want to update your project. It will create a temporary virtualenv.

`make virtualenv` Creates a new virtualenv using requirements.txt.

`make virtualenv_test` Creates a development virtualenv using requirements.txt and packages from requirements/test.txt.

`make clean` Removes the .pyc files and deletes the virtualenv folder.

`make isort` Checks your code and fixes the imports using isort.

`make run` Will execute a runserver with development settings.

`make makemigrations` Will execute a makemigrations with development settings.

`make migrate` Will execute a migrate with development settings.

### Notes
Objectiu:
- Un equipo ha de poder sabre quan torna a jugar
- Tenir es creuaments entre equipos automatizats

Coses a tenir en compte
- Cada equip pertany a una categoria
- Un equpip no ha d'estar molt de temps sense jugar ni jugar molt seguit

Preguntes
- Acces domini esporlesbc.com o un de nou?
- Quines categories hi haura?
- Quin tipo de competició jugaran? Lliga, cuadro de cruces, ...?
- Si un equipo se retira / no presenta, que feim?
- Hem de dir a quina pista se juga es partit? Quantes pistes hi haurà? Estaran sempre disponibles?
- Hem de calcular quan dura un partit i a quina hora juga cada partit?
- Poden jugar qualsevol categoria a qualsevol hora? Per exemple, minis a les 4 de sa matinada?

- Que ha de veure organització i quines accions podrà fer?
    > Seguents partits (quan i on)
    > Classificacions
    > Resultats
    > Introduir resultat d'un partit
    > Poder crear un equip
    > Poder crear categories
- Que han de veure es jugadors?
    > Seguents partits (quan i on)
    > Classificació
    > Resultats

Models
- Equipo
    > Nom
    > Categoria
- Categoria
    > Nom
- Partit
    > Local (equip)
    > Visitant (equip)
    > Resultat (punts local - punts visitant)
- Pista
    > Nom
- Classificació
    > Categoria
    > Equips (M2M) ordenats
- Time slot
    > Hora inici
    > Hora fi