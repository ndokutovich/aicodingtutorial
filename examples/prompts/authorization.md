# Промт: Реализация SSO авторизации

Добавь SSO авторизацию в мобильное приложение, используя webview. Реализация должна соответствовать следующим требованиям:

1. Используй подход Model-Repository в качестве клиента для взаимодействия с API авторизации
2. Используй BLOC-архитектуру для управления состоянием на событиях DelayedResult<T>
3. После успешной авторизации webview должен скрываться автоматически
4. Необходимо реализовать сохранение токена авторизации в безопасном хранилище
5. Добавь механизм обновления токена при истечении срока действия
6. Реализуй выход из аккаунта с очисткой всех данных сессии
7. Добавь обработку основных ошибок авторизации (неверные учетные данные, отсутствие подключения и т.д.)

Технические детали:
- Используй пакет webview_flutter для реализации webview
- Для хранения токенов используй flutter_secure_storage
- API авторизации работает по протоколу OAuth 2.0 с поддержкой refresh токенов
- URL для авторизации: https://auth.example.com/sso/login
- Необходимо перехватывать редирект на URL: app://auth-callback с параметрами token и refreshToken

Структура компонентов:
- **Models**: AuthTokens, User, AuthenticationStatus, AuthException
- **Repository**: AuthRepository с методами login(), logout(), refreshToken(), getCurrentUser()
- **BLoC**: AuthBloc с событиями LoginEvent, LogoutEvent, RefreshTokenEvent, CheckAuthStatusEvent
- **UI**: AuthScreen с WebView, LoadingIndicator, ErrorWidget

Пример использования ожидаемого результата в коде:

```dart
// Инициирование авторизации
authBloc.add(LoginEvent());

// Слушатель состояния авторизации
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    if (state is AuthInitial) {
      return LoginButton();
    } else if (state is AuthLoading) {
      return LoadingIndicator();
    } else if (state is AuthAuthenticated) {
      return UserProfileScreen(user: state.user);
    } else if (state is AuthError) {
      return ErrorWidget(message: state.message);
    }
    return Container();
  },
);
```

Важно обеспечить безопасное хранение авторизационных данных и корректную обработку всех возможных состояний авторизации. 