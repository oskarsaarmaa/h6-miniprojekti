# Steam pelidatan visualisointityökalu

## Projektin tarkoitus
Projekti automatisoi Ansiblen ja Dockerin avulla Flask-pohjaisen verkkosovelluksen vetäen Steamin API:stä uusia videopelejä ja niiden arvosteluja, sekä tarjoaa visuaalisen käyttöliittymän niiden selaamiseen

## Screenshot tähän
```bash
<img width="1867" height="713" alt="image" src="https://github.com/user-attachments/assets/349b381a-3e01-48d4-a162-119aec7b7fd8" />
```

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
