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
```bash
git clone https://github.com/oskarsaarmaa/h6-miniprojekti
cd h6-miniprojekti
```

### 2. Asenna Ansible
```bash
sudo apt update
sudo apt install ansible -y
```
### 3. Aja playbook
```bash
ansible-playbook playbook.yml
```
### 4. Avaa selaimessa
```bash
http://localhost:5000
```
