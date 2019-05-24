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
CREATE DATABASE "24hours";
CREATE USER twentyfourhours WITH PASSWORD "24hours";
GRANT ALL PRIVILEGES ON DATABASE "24hours" TO twentyfourhours;
ALTER USER twentyfourhours CREATEDB;
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
- Un equpip no ha d'estar molt de temps sense jugar ni jugar molt seguit. Jugar cada 1h:30 2h

Domini
- Acces domini esporlesbc.com o un de nou? Domini nou: acampabasquetebc.com

- Que ha de veure organització i quines accions podrà fer?
    > Seguents partits (quan i on)
    > Classificacions
    > Resultats
    > Introduir resultat d'un partit
    > Poder crear un equip
    > Poder crear categories (ja ho faig jo)
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


### Funcionament
Se jugarà una competició 3x3 de basket per categories amb una durada màxima de 24h (nomrmalment unes 16h).

Es partits son de 12 minuts i se juguen dedins un slot de 15 minuts. La competició comença a les 19:00.

Hi ha 3 pistes disponibles però depen des volum d'equips se juga només en 2 pistes. Ses finals de cada categoria se juguen a sa pista central, però pot ser que se juguin dues finals alhora. Les semifinals es juguen a pista lateral.

Cada equip pertany a una categoria. Hi ha 3 categories: Infantil, Cadet i Absoluta. Per cada categoria es equips poden ser masculí o femení. Si hi ha equips mixtes es colocaran a altres categories. Si a una categoria hi ha pocs equips s'ajuntaran masculina i femenina.

Cada categoria jugarà una competició en modo lliga (veure quadres FBIB). Si hi ha categories molt grans, per exemple de 12, intentar dividir-les en 2 subcategories de 6 equips.

Si una categoria té 2 subcategories, se disputarà una final 1r contra 1r i una semi 2n contra 2n.
Si una categoria no te subcategories, se disuputaran 2 semis, 1r contra 4t i 2n contra 3r. Es guanyadors disputaran sa final. (Pendent de Aina)
Si una categoria es mixta (hi ha equips masculins i femenins), se disputara una final entre es dos millors classificats masculins i es dos millors classificats femenins.

La categoria Infantil no pot jugar partits entre les 02:00 i les 07:00. Si no es pot emplenar tot el quadre amb els equips que hi ha, deixar forats buids per possibles canvis.

Si un equip no se presenta, marcar partit com 23 a 0 a favor del equip presentat.
