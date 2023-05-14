![image](https://user-images.githubusercontent.com/74711093/219436570-8c0c7a2d-805e-418a-918e-7a3b9e8e6bd8.png)
# Gorilla - _Your Web-App's Bodyguard_
## About us
**_Gorilla_** is a powerfull Web-Application Firewall (WAF), that detect and block different web attacks. <br>
It communicates with a local database with MongoDB, that has the blocked attackers by their IP address. 
#### Supported attacks
- ⚔️ Cross-Site Scripting (XSS) & HTML Injection.
- 📑 SQL Injection (SQLi) [Note: Detection occurs with a ML model].
- 🏭 HTTP Parameter Pollution (HPP).
- ⏮️ SSI Injection (SSIi).
- 📬 Open Redirect Attack.
- 🌓 HTTP Response Splitting.
## Installation Guide
1. Install Docker & Docker Compose.
2. Create a file named "docker-compose.yml" with this content (pay attention to the things you need to change):

```
version: '3'
services:

  nginx-waf:
    image: alonnagar/gorilla:nginx-gorilla-waf
    ports:
      - "80:80"
    depends_on:
      - flask-waf
      - website

  flask-waf:
    image: alonnagar/gorilla:flask-gorilla-waf
    ports:
      - "3333:3333"
    depends_on:
      - mongo

  nginx-gui:
    image: alonnagar/gorilla:frontend-gorilla-gui
    ports:
      - "5555:80"
    depends_on:
      - flask-gui

  flask-gui:
    image: alonnagar/gorilla:backend-gorilla-gui
    ports:
      - "4444:4444"
    depends_on:
      - mongo

  mongo:
    image: mongo
    ports:
      - "27017:27017"

  website:
    image: <ENTER DOCKER IMAGE’S NAME FOR THE VULNERABLE WEBSITE>
    ports:
      - "7777:80"
```      
      
 3. Run "docker-compose up".
