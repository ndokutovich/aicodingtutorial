# 15. Технологии и фреймворки


### 15.1. Фронтенд - Flutter

Flutter - мощный фреймворк для кросс-платформенной разработки от Google:

1. Установка и настройка Flutter:
   ```bash
   curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/macos/flutter_macos_3.16.9-stable.zip
   unzip flutter_macos_3.16.9-stable.zip
   export PATH="$PATH:`pwd`/flutter/bin"
   flutter doctor
   ```

2. Создание нового проекта Flutter:
   ```bash
   flutter create my_project_name
   cd my_project_name
   flutter run
   ```

3. Flutter и Cursor работают вместе особенно эффективно благодаря поддержке Dart и отличной интеграции с инструментами Flutter.

4. Документация по Flutter доступна на [официальном сайте](https://docs.flutter.dev/)

### 15.2. Backend

#### 15.2.1. Java и JHipster

JHipster - платформа для быстрой разработки современных веб-приложений с использованием Spring Boot и различных фронтенд-фреймворков:

1. Установка JHipster:
   ```bash
   npm install -g generator-jhipster
   ```

2. Создание нового проекта:
   ```bash
   mkdir my_jhipster_project && cd my_jhipster_project
   jhipster
   ```

3. Документация по JHipster доступна на [официальном сайте](https://www.jhipster.tech/documentation-archive/v7.9.3)

#### 15.2.2. NodeJS

Node.js - среда выполнения JavaScript на сервере:

1. Установка Node.js:
   - macOS: `brew install node`
   - Windows: Скачайте установщик с [официального сайта](https://nodejs.org/)

2. Создание Express-приложения:
   ```bash
   npx express-generator my-express-app
   cd my-express-app
   npm install
   npm start
   ```

3. Документация по Node.js доступна на [официальном сайте](https://nodejs.org/en/docs/)

### 15.3. Интеграция - N8N

N8N - расширяемая платформа рабочего процесса для соединения различных систем и автоматизации задач:

1. Установка N8N:
   ```bash
   npm install -g n8n
   ```

2. Запуск N8N:
   ```bash
   n8n
   ```

3. Документация по N8N доступна на [официальном сайте](https://docs.n8n.io/)

4. Cursor IDE может помочь в создании и отладке рабочих процессов N8N с помощью подсказок по API и автоматического заполнения.

