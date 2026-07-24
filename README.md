# Musicon - Platforma za Povezivanje Muzičara

**Musicon** je veb aplikacija razvijena u Django framework-u, dizajnirana da bude centralno mesto za rock i metal muzičare i bendove. Platforma omogućava kreiranje detaljnih profila, objavljivanje svirki, i međusobnu komunikaciju, sa ciljem da olakša pronalaženje novih članova benda i saradnika.

## Ključne Funkcionalnosti

*   **Autentikacija Korisnika:** Kompletna funkcionalnost za registraciju, prijavljivanje i odjavljivanje korisnika.
*   **Profil Benda:** Svaki korisnik može kreirati i uređivati detaljan profil za svoj bend, uključujući:
    *   Osnovne informacije (ime, grad, država).
    *   Profilnu sliku (logo benda).
    *   Biografiju, muzičke žanrove i uticaje.
    *   Upload do dve demo pesme u `.mp3` formatu.
    *   Status o potrazi za novim članovima i dostupnosti za svirke.
    *   Linkove ka društvenim mrežama i streaming servisima (Spotify, YouTube, itd.).
*   **Sistem za Svirke:** Korisnici mogu objavljivati detalje o nadolazećim svirkama, koje se zatim prikazuju na javnoj listi.
*   **Interni Sistem za Poruke:**
    *   Posetioci mogu slati poruke direktno bendovima preko njihovih profilnih stranica.
    *   Korisnici imaju privatni inbox za pregled primljenih poruka.
*   **Real-time Notifikacije:** Asinhroni sistem (AJAX Polling) koji periodično proverava nove poruke i obaveštava korisnika putem bedža u navigaciji, bez potrebe za osvežavanjem stranice.
*   **Javne Liste sa Paginacijom:** Posebne stranice za pregled svih bendova i svih nadolazećih svirki, sa paginacijom za lakšu navigaciju.
*   **Moderan Korisnički Interfejs:** Responzivan dizajn sa modernim tamnim temama, animacijama i modalnim prozorima za bolji korisnički doživljaj.

## Tehnologije

*   **Backend:**
    *   Python 3
    *   Django 4+
*   **Frontend:**
    *   HTML5
    *   SCSS / CSS3
    *   JavaScript (ES6)
    *   Bootstrap 5
*   **Baza Podataka:**
    *   SQLite 3 (za razvoj)

## Struktura Projekta

Projekat je organizovan u dve glavne Django aplikacije:

*   `core`: Glavna aplikacija koja sadrži većinu poslovne logike, uključujući modele za profile, svirke i poruke, kao i sve glavne poglede (views) i templejte.
*   `users`: Aplikacija zadužena isključivo za proces registracije i upravljanje korisnicima.

## Pokretanje Projekta Lokalno

Da biste pokrenuli projekat na svom računaru, pratite sledeće korake:

1.  **Klonirajte repozitorijum:**
    ```bash
    git clone <URL_VAŠEG_REPOZITORIJUMA>
    cd musiconapp
    ```

2.  **Kreirajte i aktivirajte virtuelno okruženje:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalirajte zavisnosti:**
    Pre nego što pokrenete ovu komandu, potrebno je da kreirate `requirements.txt` fajl. To možete uraditi komandom:
    ```bash
    pip freeze > requirements.txt
    ```
    Nakon toga, instalirajte sve sa:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Pokrenite migracije:**
    Ova komanda će kreirati šemu baze podataka na osnovu modela.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Kreirajte superkorisnika:**
    Ovo će vam omogućiti pristup Django admin panelu.
    ```bash
    python manage.py createsuperuser
    ```

6.  **Pokrenite razvojni server:**
    ```bash
    python manage.py runserver
    ```

7.  Aplikacija će biti dostupna na adresi `http://127.0.0.1:8000/`.

## Ključni Modeli

*   `BandProfile`: Sadrži sve informacije vezane za profil jednog benda. Povezan je `OneToOne` vezom sa Django `User` modelom.
*   `AddGigDate`: Predstavlja jedan događaj (svirku). Povezan je `ForeignKey` vezom sa `User` modelom, kako bi se znalo ko je objavio svirku.
*   `SendMessageToBand`: Predstavlja jednu poruku poslatu bendu. Povezan je `ForeignKey` vezom sa `BandProfile` modelom.

## API Endpoints (za AJAX)

Aplikacija koristi nekoliko internih API endpoint-a za dinamičke funkcionalnosti:

*   `/api/check-new-messages/`: `GET` - Vraća broj nepročitanih poruka za ulogovanog korisnika.
*   `/api/mark-messages-as-read/`: `POST` - Označava sve poruke korisnika kao pročitane.
*   `/api/messages/<id>/delete/`: `POST` - Briše poruku sa datim ID-jem.
*   `/api/messages/<id>/toggle-read/`: `POST` - Menja status poruke (pročitano/nepročitano).
*   `/api/gigs/<id>/delete/`: `POST` - Briše svirku sa datim ID-jem.

