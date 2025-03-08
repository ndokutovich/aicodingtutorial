# 5. Настройка проекта для разработки


### 5.1. Инициализация проекта

Перед началом работы рекомендуется инициализировать Git-репозиторий:

```bash
git init
```

Подробнее о Git можно узнать в [официальной документации Git](https://git-scm.com/book/ru/v2).

### 5.2. Специальные файлы Cursor

Для эффективной работы с Cursor рекомендуется создать следующие файлы:

- **.cursorrules** - файл с правилами для AI-ассистента
- **.cursorignore** - файл для исключения определенных директорий из анализа AI
- **.notes/project-overview.md** - файл с обзором проекта для контекста AI

Эти файлы помогут настроить взаимодействие с AI-ассистентом под специфику вашего проекта. Подробнее о настройке Cursor можно узнать в [документации Cursor](https://cursor.sh/docs).

### 5.3. Создание проекта

При создании нового проекта рекомендуется использовать стандартные инструменты фреймворков или готовые шаблоны (boilerplate):

```bash
# Для React-проекта
npx create-react-app project-name
```
Подробнее о Create React App в [официальной документации React](https://create-react-app.dev/docs/getting-started/).

```bash
# Для Flutter-проекта
flutter create project-name --platforms=ios,linux,windows,macos,android
```
Подробнее о создании проектов Flutter в [документации Flutter](https://docs.flutter.dev/get-started/test-drive).

```bash
# Для JHipster-проекта
jhipster
```
Подробнее о JHipster в [официальной документации JHipster](https://www.jhipster.tech/documentation-archive/).

```bash
# Для Node.js-проекта
npm init
```
Подробнее о создании Node.js проектов в [документации NPM](https://docs.npmjs.com/cli/v8/commands/npm-init).

Важно: **Всегда предпочитайте создание каркаса проекта специализированными утилитами** или используйте готовые boilerplate-решения, вместо того чтобы генерировать структуру с нуля через ИИ.

### 5.4. Стандартные инструменты разработки

В зависимости от типа проекта используйте следующие стандартные инструменты:

- **[Git](https://git-scm.com/)** - система контроля версий для отслеживания изменений и совместной работы
- **[Flutter](https://flutter.dev/)** - фреймворк для создания кроссплатформенных мобильных приложений
- **[JHipster](https://www.jhipster.tech/)** - платформа для быстрой генерации веб-приложений
- **[Node.js](https://nodejs.org/)** - среда выполнения JavaScript для серверной разработки
- **[Java](https://www.java.com/)/[Python](https://www.python.org/)** - языки программирования для серверной разработки

#### 5.4.1. Установка и проверка необходимых инструментов

Ниже представлена таблица с инструментами разработки, необходимыми для работы с различными типами проектов в Cursor IDE, а также команды для их установки и проверки работоспособности:

| Инструмент | Установка | Проверка работоспособности |
|------------|-----------|----------------------------|
| **Общие инструменты** |  |  |
| Git | [Скачать с git-scm.com](https://git-scm.com/downloads)<br>macOS: `brew install git` | `git --version` |
| Homebrew (macOS) | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` | `brew --version` |
| Node.js | [Скачать с nodejs.org](https://nodejs.org/)<br>macOS: `brew install node`<br>Windows: winget: `winget install OpenJS.NodeJS` | `node --version`<br>`npm --version` |
| Docker | [Docker Desktop](https://www.docker.com/products/docker-desktop)<br>macOS: `brew install --cask docker` | `docker --version`<br>`docker-compose --version` |
| **Backend** |  |  |
| Java JDK | [Oracle JDK](https://www.oracle.com/java/technologies/downloads/)<br>[OpenJDK](https://openjdk.org/)<br>macOS: `brew install openjdk@17` | `java --version`<br>`javac --version` |
| Gradle | [gradle.org/install](https://gradle.org/install/)<br>macOS: `brew install gradle` | `gradle --version` |
| Maven | [maven.apache.org](https://maven.apache.org/download.cgi)<br>macOS: `brew install maven` | `mvn --version` |
| Python | [python.org/downloads](https://www.python.org/downloads/)<br>macOS: `brew install python` | `python --version`<br>`pip --version` |
| **Frontend** |  |  |
| Flutter | [flutter.dev/docs/get-started/install](https://flutter.dev/docs/get-started/install)<br>macOS: `brew install --cask flutter` | `flutter --version`<br>`flutter doctor` |
| Dart SDK | Устанавливается с Flutter<br>macOS: `brew install dart` | `dart --version` |
| npm/yarn | npm: (устанавливается с Node.js)<br>yarn: `npm install -g yarn` | `npm --version`<br>`yarn --version` |
| **Дополнительные инструменты** |  |  |
| Visual Studio Code | [code.visualstudio.com](https://code.visualstudio.com/)<br>macOS: `brew install --cask visual-studio-code` | Запустить и проверить версию в меню Help > About |
| Android Studio | [developer.android.com/studio](https://developer.android.com/studio)<br>macOS: `brew install --cask android-studio` | Запустить и проверить версию в меню About |
| Xcode (macOS) | App Store или [developer.apple.com](https://developer.apple.com/xcode/) | `xcodebuild -version` |
| CocoaPods (macOS) | `sudo gem install cocoapods`<br>macOS: `brew install cocoapods` | `pod --version` |
| ESLint | `npm install -g eslint` | `eslint --version` |
| n8n | `npm install -g n8n` | `n8n --version` |

> **Примечание**: На macOS рекомендуется использовать Homebrew для установки большинства инструментов. На Windows можно использовать [Chocolatey](https://chocolatey.org/) или [winget](https://docs.microsoft.com/en-us/windows/package-manager/winget/) как альтернативу.

### 5.5. Форматы данных

Рекомендуемые форматы данных для различных целей:

- **[JSON](https://www.json.org/json-en.html)** - для структурированных данных, конфигураций API и обмена данными
- **[Markdown (MD)](https://daringfireball.net/projects/markdown/)** - для форматированного текста, документации и инструкций
- **[YAML (YML)](https://yaml.org/)** - для конфигурационных файлов, более читабельная альтернатива JSON
- **[Mermaid в MD](https://mermaid-js.github.io/mermaid/#/)** - для создания диаграмм прямо в markdown-документах

