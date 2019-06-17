# Acampabàsquet

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
CREATE DATABASE acampabasquet;
CREATE USER acampabasquet WITH PASSWORD 'acampabasquet';
GRANT ALL PRIVILEGES ON DATABASE "acampabasquet" TO acampabasquet;
ALTER USER acampabasquet CREATEDB;
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

## Funcionament
Se jugarà una competició 3x3 de basket per categories amb una durada màxima de 24h.

Es partits son de 15 minuts i se juguen dedins un slot de 20 minuts. La competició comença a les 19:00.

Hi ha 3 pistes disponibles però depen des volum d'equips se juga només en 2 pistes. Ses finals de cada categoria se juguen a sa pista central, però pot ser que se juguin dues finals alhora. Les semifinals es juguen a pista lateral.

Cada equip pertany a una categoria. Hi ha 3 categories: Infantil, Cadet i Absoluta. Per cada categoria es equips poden ser masculí o femení. Si hi ha equips mixtes es colocaran a masculí. Si a una categoria hi ha pocs equips s'ajuntaran masculina i femenina.

Cada categoria jugarà una competició en modo lliga (veure quadres FBIB) i només partit d'anada. Si hi ha categories molt grans, per exemple de 12, intentar dividir-les en 2 subcategories de 6 equips.

Si una categoria té 2 subcategories, se disputarà una final 1r contra 1r i una semi 2n contra 2n.
Si una categoria no te subcategories, se disuputaran 2 semis, 1r contra 4t i 2n contra 3r. Es guanyadors disputaran sa final. (Pendent de Aina)
Si una categoria es mixta (hi ha equips masculins i femenins), se disputara una final entre es dos millors classificats masculins i es dos millors classificats femenins.

Si un equip no se presenta, marcar partit com 23 a 0 a favor del equip presentat.

## Millores futures
- Cache a llistats
- Posar restriccions per equipo, grup o categoria, per exemple, Equip A no juga entra les 19:00 i les 22:00. Categoria B no ha d'acabar a les 07:00.
- Fer apartar de configuracio:
    > Temps de partit
    > Temps de descans
    > Cada quant volem pista buida
    > Temps entre partits
- Crear partits sense slot asignat, crear slots a base de dades, calular millor slots possible per partit i poder fer drag an drop per ordenar.
- Poder fer alta d'equips
- Marcar partits com: Lliga, fora competició (o amistos), play-off (per finals i semis)
- Marcar si un grup fa anada i tornada o no
- Poder afegir partits a mà. Alguns partits entre grups diferents, per exemple Abs Mac vs Abs Fem
