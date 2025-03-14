# 12. Безопасность и конфиденциальность


При работе с Cursor IDE важно понимать аспекты безопасности и защиты личных данных, особенно при использовании AI-возможностей.

### 12.1. Обработка данных в Cursor

Cursor отправляет части вашего кода на серверы AI для обработки. Важно понимать:

- **Что отправляется**: открытые файлы, выделенный код, история чата с AI-ассистентом
- **Когда отправляется**: при явном запросе к AI-ассистенту или использовании автоматических функций
- **Как защищаются данные**: данные передаются по зашифрованному HTTPS-соединению

#### Режимы обработки данных

Cursor предлагает два основных режима обработки данных:

1. **Стандартный режим**:
   - Данные могут кэшироваться на серверах Cursor
   - Данные могут использоваться для улучшения моделей (согласно политике конфиденциальности)
   - Предлагает максимальную производительность и точность ответов

2. **Режим конфиденциальности (Privacy Mode)**:
   - Данные не сохраняются на серверах после обработки запроса
   - Данные не используются для обучения моделей
   - Доступен во всех тарифных планах (принудительное включение на уровне организации в Business-плане)

#### Использование собственных API-ключей для повышения конфиденциальности

Как описано в разделе [4.4. Подключение собственных моделей](#44-подключение-собственных-моделей), использование собственного API-ключа может предоставить дополнительный уровень контроля над данными:

- Данные обрабатываются через вашу учетную запись у провайдера модели
- Вы можете выбрать провайдера с подходящей политикой конфиденциальности
- При использовании Azure OpenAI можно настроить региональное размещение для соответствия нормативным требованиям

Однако важно помнить, что даже при использовании собственного API-ключа, данные все равно проходят через серверы Cursor для формирования финального промпта.

### 12.2. Меры безопасности

Рекомендуемые меры для обеспечения безопасности при работе с Cursor:

- Не храните конфиденциальные данные (пароли, API-ключи) в обычных текстовых файлах
- Используйте `.cursorignore` для исключения чувствительных файлов
- Рассмотрите возможность использования собственного API-ключа для повышения безопасности
- Активируйте обнаружение/искажение конфиденциальной информации в настройках
- Для особо чувствительных проектов рассмотрите работу в офлайн-режиме
- Используйте VPN при работе с чувствительными проектами

### 12.3. Лучшие практики безопасности

Рекомендации по безопасной работе с Cursor:

- Регулярно обновляйте Cursor до последней версии
- Следуйте принципу наименьших привилегий для моделей AI
- Проводите аудит генерируемого кода перед внедрением
- Настройте правила в `.cursorrules` для ограничения доступа AI к определенным частям кодовой базы
- Используйте принципы безопасного кодирования при работе с генерируемым кодом
- Контролируйте, какие проекты открываются с использованием AI-ассистента

Пример настройки `.cursorrules` для повышения безопасности:
```
# Ограничение контекста для AI
Пожалуйста, анализируй только файлы с исходным кодом и документацию.
Никогда не анализируй файлы конфигурации, содержащие учетные данные или токены.
Всегда предлагай безопасные практики кодирования и отмечай потенциальные проблемы безопасности.
```

