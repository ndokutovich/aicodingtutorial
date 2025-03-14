# 6. Работа с промтами


### 6.1. Формулирование эффективных промтов

Для эффективной работы с AI-ассистентом Cursor важно правильно формулировать запросы:

- Будьте конкретны в своих запросах
- Указывайте контекст (технологии, фреймворки)
- Разбивайте сложные задачи на более мелкие
- Указывайте ожидаемый формат результата

### 6.2. Примеры промтов

В этом разделе представлены краткие примеры промтов. Более подробные и расширенные примеры вынесены в отдельные файлы в директории `examples/prompts/`:

#### HTTP Клиент
```
В качестве транспорта используем авторизованный webview c post запросом и следующим телом...
```
> 💡 Полный пример промта: [examples/prompts/http_client.md](examples/prompts/http_client.md)

#### Авторизация
```
Добавь SSO авторизацию, используя webview. Используй подход Model-Repository в качестве клиента, BLOC на событиях DelayedResult<T>...
```
> 💡 Полный пример промта: [examples/prompts/authorization.md](examples/prompts/authorization.md)

#### Загрузка данных
```
На основе данного HTML создай модель данных и парсер, который извлечет данные о сотрудниках и их отпусках...
```
> 💡 Полный пример промта: [examples/prompts/data_loading.md](examples/prompts/data_loading.md)

#### Отображение данных
```
Добавь иконку в трее и меню со следующими пунктами...
```
> 💡 Полный пример промта: [examples/prompts/tray_menu.md](examples/prompts/tray_menu.md)

### 6.3. Принципы генерации кода

При работе с генерацией кода в Cursor следуйте следующим принципам:

- **Предпочитайте гарантированную генерацию генеративной**. Лучше использовать проверенные методы и инструменты, чем полагаться только на ИИ.
- **Поручайте ИИ скриптовать существующую генерацию**, а не генерировать всё самостоятельно. Многие профессиональные инструменты имеют скриптовые языки (макросы в Photoshop, Blender, MS Office) - попросите ИИ создать скрипт, который создаст то, что вам нужно.
- **Используйте AI для обработки и улучшения результатов**, а не для создания всего с нуля.

