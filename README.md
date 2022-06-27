# Python-rest API

## client.py
V súbore client.py sa nachádzajú funkcie na získanie dát z externej api. Funkcia **get_external_data** hľadá ID z externej api, ak sa toto ID nenachádza v systéme. Ak sa hľadané ID nachádza v externej api, a má rozdielny title, userID a body ako doteraz uložené príspevky v systéme, tak sa uloží do systému a funkcia vráti id príspevku. V prípade ak sa príspevok v externej api nenašiel alebo už bol uložený do systému, funkcia vráti 0.

Funkcia **get_user_id** sa používa na overenie userID prostredníctvom externej api. Načíta dáta z externého endpointu /users a postupne prechádza takto získané userID. Ak sa nájde hľadané id, funkcia vráti True, v opačnom prípade False.

## models.py
V tomto súbore je definovaný model Post s userID (integer), title (s maximálnou dĺžkou 100 znakov) a body (max dĺžka 1000 znakov).

## serializers.py
Tu je vytvorený PostSerializer s poliami id, userID, title, body

## Dockerfile
Aplikácia je napísaná v Pythone 3, preto sa vytvorí kontajner založený na Pythone 3. Vytvorí sa adresár pre zdrojový kód s názvom code. Nastaví sa working directory. Všetky súbory projektu sa skopírujú do image prostredníctvom príkazu COPY. Bodka v tomto príkaze znamená, že sa kopírujú súbory z lokálneho projektu. Nakoniec sa nainštalujú požiadavky zo súboru requirements.txt

## docker-compose.yml
V tomto súbore sa používa docker compose syntax 3. V časti 'web' hovoríme, ako build náš kontajner alebo kde sa nachádza docker file. Je tam zadaná ., čo znamená, že sa má vytvoriť zo súčasného adresára. Ďalej špecifikujeme príkaz, ktorý cheme zbehnúť keď ide náš kontajner. python manage.py runserver 0.0.0.0:8000. Ďalej pridám volumes, čo mi umožňuje mať prístup ku kódu v reálnom čase v mojom dockerfile. Čiže keď urobím zmenu v zdrojovom kóde, automaticky sa táto zmena prejaví aj v docker kontajneri, ktorý bude spustený. Nakoniec sa namapuje port z kontajnera. Po zadaní príkazu docker-compose run web python manage.py migrate sa vytvorí docker kontajner. Ďalším príkazom docker-compose build sa vytvorí kontajner. Image sa spustí príkazom docker-compose up. Po zadaní do url http://localhost:8000/posts/?id=1 sa prostredníctvom django servera zobrazí príspevok.

## urls.py
Sú tu definované fungujúce url adresy. Okrem admin url sú tu: posts/int:id - používa sa na DELETE a PUT posts/ - GET a POST

## views.py
Nachádzajú sa tu 2 funkcie - delete_or_put a get_post. Vo funkcii **delete_or_put** sa v bloku try pokúsim získať príspevok s id, ktorý bol zadaný v url (napr. http://localhost:8000/posts/1 pre príspevok s id = 1). Ak sa takýto príspevok nenájde, vypíše sa chybová hláška "This post does not exist" so statusom 404. Ak sa nájde a tento príspevok má byť vymazaný, tak sa jednoducho vymaže a vypíše sa status 204.

Ak chceme tento príspevok upraviť, zisťuje sa, aké parametre prišli v requeste. Ak sa v ňom nachádzalo 'title', tak sa prepíše pôvodný title na novú hodnotu. To isté platí aj pre body. Nakoniec sa prostredníctvom serializera načíta upravený príspevok, upraví sa do formátu json a vypíše sa spolu so statusom 200.

Funkcia **get_post** najprv zistí, či chceme vytvoriť nový príspevok alebo zobraziť príspevok. Ak ho chceme vytvoriť, zisťuje sa, či v body requestu sa nachádzajú všetky povinné polia. Ak sa v ňom nenachádza 'title', vypíše s chybová hláška "title": "is_blank". To isté platí aj pre body a userID príspevku. Ak sa userID v body requestu nachádza, kontroluje sa, či sa toto userID nachádza v externej API. Ak nie, vypíše sa "userID": "Unknown". Ak sa v body requeste nachádza nejaká z týchto chýb, vypíše sa spolu so statusom 400 (bad request). Ak boli zadané všetky povinné polia a userID existuje v externej API, uloží sa tento príspevok do systému a vypíše sa spolu so statusom 201 (created).

Ak chceme zobraziť nejaký príspevok, načíta sa z requestu id a userID (jeden z nich musí byť zadaný). Ak ID nie je prázdne, skontroluje sa, či bolo zadané ako parameter číslo. Ak nebolo, vypíše sa chybová hláška "ID": "Is not an integer". Ak bolo zadané číslo, vyhľadá sa v systéme príspevok s týmto ID. Ak sa v systéme nenájde, hľadá ho v externej API. Ak sa nájde, uloží sa a vypíše sa posledný príspevok (posledný uložený). Ak ho v externej API nenájde, vypíše sa "ID": "Invalid ID". Ak bolo v requeste zadané userID (napr. http://localhost:8000/posts/?userid=1), program vyhľadá všetky príspevky vytvorené týmto používateľom. Ak nenájde ani jeden, vypíše "userID": "Unknown userID" so statusom 400. Tiež kontroluje, či bol v requeste za userid zadaný integer. Ak sa nájde v systéme aspoň 1 príspevok od zadaného používateľa, vypíše sa tento príspevok. V prípade, že je od zadaného používateľa viac príspevkov, vypíšu sa všetky.
