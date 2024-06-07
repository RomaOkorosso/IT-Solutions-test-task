## IT-Solutions Test Task
### ENG
Test task without frontend, just REST API with DB. Include seeder before startup. Contain user registration, auth, deleting.
Also contain full CRUD methods for goods/ad

### Installation


1. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/RomaOkorosso/IT-Solutions-test-task.git
    ```
2. Create `.env` file:
    ```bash
    cp .env.example .env
    ```

#### Run with docker

3. Run Docker containers:
   CHANGE `POSTGRES_HOST=127.0.0.1` to `POSTGRES_HOST=db` in .env
    ```bash
    docker-compose up -d
    ```
4. Visit `http://localhost:{APP_PORT}/docs` in your browser.


### Built With

* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Docker](https://www.docker.com/)
* [PostgreSQL](https://www.postgresql.org/)

### EXTRA
#### - If you need to activate pre-commit actions must:
1. run `pip install -r requirements.txt`
2. use `pre-commit install`
3. if you need to speed up checks for next uses or just get info about hooks use: `pre-commit run --all-files`
first run will take a few minutes
4. you can commit and push!


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact

Created by [@RomaOkorosso](https://github.com/RomaOkorosso)

### RU

Тестовое задание без фронтенда, просто REST API с базой данных. Включая заполнение базы данных при старте приложения. 
Содержит регистрация, авторизацию и удаление пользователей. Так же содержит полный CRUD для методов для объявлений

### Установка

Для установки проложения следуйте следующим шагам:

1. Скопируйте репозиторий с ГитХаба:
    ```bash
    git clone https://github.com/RomaOkorosso/IT-Solutions-test-task.git
    ```
2. Создайте `.env` файл:
    ```bash
    cp .env.example .env
    ```

#### Запуск через Докер

3. Запустите Докер контейнер:
   Поменяйте `POSTGRES_HOST=127.0.0.1` на `POSTGRES_HOST=db` в .env файле
    ```bash
    docker-compose up -d
    ```
4. Заходите  `http://localhost:{APP_PORT}/docs` в Вашем браузере.


### Создано при помощи:

* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Docker](https://www.docker.com/)
* [PostgreSQL](https://www.postgresql.org/)

### ДОПОЛНИТЕЛЬНО
#### - Если вы хотите активировать пре-коммиты, то:
1. запускаем `pip install -r requirements.txt`
2. затем `pre-commit install`
3. если вы хотите ускорить последующие проверки или или просто узнать о хуках, то используем: `pre-commit run --all-files`
первый запуск займет несколько минут
4. теперь вы можете коммитить и пушить!

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Контакты

Создано [@RomaOkorosso](https://github.com/RomaOkorosso)
