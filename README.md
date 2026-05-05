# Steam pelidatan visualisointityökalu

## Projektin tarkoitus
Projekti automatisoi Ansiblen ja Dockerin avulla Flask-pohjaisen verkkosovelluksen vetäen Steamin API:stä uusia videopelejä ja niiden arvosteluja, sekä tarjoaa visuaalisen käyttöliittymän niiden selaamiseen

## Screenshot tähän

<img width="2312" height="883" alt="projektikuva" src="https://github.com/user-attachments/assets/fb8c9af3-41e1-44f0-aa4b-e496403da10d" />


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
