# Steam pelidatan visualisointityökalu

## Projektin tarkoitus
Projekti automatisoi Ansiblen ja Dockerin avulla Flask-pohjaisen verkkosovelluksen joka kerää RAWG API:tä hyödyntäen Steamin pelidataa ja arvosteluja, sekä tarjoaa visuaalisen käyttöliittymän sen selaamiseen.

Kaikki hallitaan ansiblella, joka takaa nopean ja helpon käyttöönoton sekä idempotenttiuden.

<img width="2312" height="883" alt="projektikuva" src="https://github.com/user-attachments/assets/fb8c9af3-41e1-44f0-aa4b-e496403da10d" />

---

## Tekijät
Oskar Saarmaa & Miro Rautanen

---

## Lisenssi

Projekti on toteutettu GNU General Public License v3.0 -lisenssillä.

---
## Asennus & Käyttöönotto

### 1. Kloonaa repositorio
Kloonaa repositorio ja siirry projektikansioon.
```bash
git clone https://github.com/oskarsaarmaa/h6-miniprojekti
cd h6-miniprojekti
```

### 2. Asenna Ansible
Valmistele hallintatyökalu. Ansible suorittaa projektin automaation puolestasi.
```bash
sudo apt update
sudo apt install ansible -y
```
### 3. Aja Automaattinen asennus
Aja Ansible-playbook. Voit käyttää -K lippua, tai vaihtoehtoisesti --ask-become-pass -lippua, jonka avulla Ansible pyytää pääkäyttäjän oikeuksia, joita tarvitaan jotta järjestelmään voidaan tehdä muutoksia.
```bash
ansible-playbook playbook.yml -K
```
### 4. Testaa sovellus
Playbookin valmistuttua sovellus on nyt toiminnassa. Avaa selain ja mene osoitteeseen:
```bash
http://localhost:5000
```
