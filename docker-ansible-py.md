## Projektin arkkitehtuuri ja tiedonkulku

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/87bc2c8b-2090-4e42-90f0-6697740d1782" />

1. Hallintakerros (Ansible): Ansible toimii koko prosessin kapellimestarina. Se valmistelee kohdekoneen, varmistaa Dockerin tilan ja suorittaa automaattisesti sovelluksen rakentamisen ja käynnistyksen. Tämä poistaa manuaalisen työn tarpeen.
2. Eristyskerros (Docker): Sovellus pakataan Docker-konttiin, joka sisältää kaiken tarvittavan: Python-ympäristön, Flask-kehyksen ja tarvittavat kirjastot. Kontitus takaa, että sovellus toimii identtisesti riippumatta siitä, missä se ajetaan.
3. Sovelluskerros (Flask): Itse Pythonilla toteutettu Flask-sovellus on järjestelmän moottori. Se kommunikoi ulkoisen RAWG API:n kanssa hakeakseen reaaliaikaista pelidataa (JSON-muodossa) ja muuntaa sen visuaaliseksi  käyttäjälle.
   





### Ansible-playbook 

Aloitin tekemällä Ansible-playbookin, koska halusin automatisoida Docker-kontin hallinnan. Playbook varmistaa, että vanhat versiot siivotaan pois tieltä ennen uuden rakentamista.

```yaml

- name: Setup GamePulse Production Environment
  hosts: localhost
  connection: local
  become: yes

  tasks:
    - name: Remove old container if it exists
      docker_container:
        name: game-insights-service
        state: absent

    - name: Remove old image to ensure fresh build
      docker_image:
        name: game-insights-app
        state: absent

    - name: Build GameInsights Docker image
      docker_image:
        build:
          path: .
        name: game-insights-app
        source: build

    - name: Start GamePulse container
      docker_container:
        name: game-insights-service
        image: game-insights-app
        state: started
        published_ports:
          - "5000:5000"
        restart_policy: always
```
* Kirjoitettiin playbook idempotentiksi, mikä tarkoittaa, että se voidaan ajaa uudelleen ja uudelleen ilman, että se aiheuttaa virheitä tai muuttaa järjestelmää, jos se on jo halutussa tilassa.
* Playbook ei vain käynnistä sovellusta, vaan hoitaa koko prosessin: poistaa vanhat jämät, rakentaa uuden version ja varmistaa verkkoyhteydet.
* Playbook siltaa kontin sisäisen liikenteen ulkomaailmaan (portti 5000), jolloin sovellus on oikeasti käytettävissä.


###  Dockerfile 

`Dockerfile` on tiedosto, joka sisältää kaikki tarvittavat askeleet "levykuvan" (image) luomiseen. Käytin tässä **multi-stage build** -ajattelun sijaan selkeää ja suoraviivaista rakennetta.
```dockerfile
# 1. Valitaan virallinen Python-pohja (kevyt versio säästää tilaa)
FROM python:3.9-slim

# 2. Määritetään kansion polku kontin sisällä
WORKDIR /app

# 3. Kopioidaan sovelluskoodi paikallisesta kansiosta konttiin
COPY app/ /app/

# 4. Asennetaan Python-riippuvuudet ilman turhaa välimuistia
RUN pip install --no-cache-dir flask requests

# 5. Kerrotaan Dockerille, että sovellus kuuntelee porttia 5000
EXPOSE 5000

# 6. Komento, joka käynnistää palvelimen kontin käynnistyessä
CMD ["python", "main.py"]

```
* Käyttämällä python:3.9-slim -pohjaa, kontin koko pidetään pienenä ja kevyeenä.
* Sovellus ja sen riippuvuudet (flask, requests) on eristetty omaan kuplaansa, jolloin ne eivät sotkeudu tietokoneen muiden ohjelmien kanssa.
* Tiedosto määrittelee tarkan aloituskomennon, jolloin kontti tietää heti käynnistyessään, mitä sen pitää tehdä.

### Python

```main.py
import requests
from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

# RAWG API-avain
RAWG_API_KEY = "8dd3b98aadc54844964a64bdc08ab6eb"

@app.route('/')
def index():
    # Lasketaan aikaväli automaattisesti (viimeiset 12 kuukautta)
    today = datetime.now().strftime('%Y-%m-%d')
    last_year = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Haetaan suosituimmat julkaisut rajapinnasta
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&dates={last_year},{today}&ordering=-added&page_size=20"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return render_template('index.html', games=data.get('results', []))
    except Exception as e:
        return f"Virhe sovelluksessa: {str(e)}"

if __name__ == "__main__":
    # Host '0.0.0.0' mahdollistaa liikenteen vastaanottamisen kontin ulkopuolelta
    app.run(host='0.0.0.0', port=5000)
```
* Koodi laskee päivämäärät lennosta, joten sovellus näyttää aina viimeisimmät pelit ilman koodimuutoksia.
* Sovellus hyödyntää modernia REST-rajapintaa (RAWG) tiedonlähteenä.
   * tuotantoympäristössä API-avain tulisi syöttää ympäristömuuttujana tai Ansiblen Vaultilla, jotta se ei päädy versionhallintaan selkokielisenä.
* try-except rakenne varmistaa, ettei koko sivu kaadu, jos esimerkiksi API-palvelu pätkisi hetkellisesti.
* Docker konttien yhteensopivuus: host='0.0.0.0' on kriittinen asetus, joka sallii Flaskin kuunnella liikennettä Docker-verkon yli.

### Lähteet
**Hallinta ja automaatio:**
* Ansible Documentation (Infrastruktuurin automaatio ja idempotentit playbookit):
     * Ansible 2024: https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks.html
     * Ansible 2024: https://docs.ansible.com/projects/ansible/latest/collections/community/docker/index.html
     * Tero Karvinen 2026: https://terokarvinen.com/palvelinten-hallinta/
       
**Docker kontitus:**
* Docker Documentation:
   * Docker Engine 2024: https://docs.docker.com/reference/dockerfile
* Docker Hub - Python:
   *  Docker Hub 2024: https://hub.docker.com/_/python
     
**API ja Flask**
* Flask Documentation:
     * Flask 2024: https://flask.palletsprojects.com/en/stable/api/#module-flask.json
* RAWG API Documentation:
     * RAWG 2026: https://api.rawg.io/docs/

**Käyttöliittymä ja visualisointi**
* Bootstrap 5:
     * Bootstrap: https://getbootstrap.com/docs/5.3/getting-started/introduction/
       
* MDN Web Docs: CSS Animations:
     * MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Animations
     
