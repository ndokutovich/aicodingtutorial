# Руководство по TDD тестированию во Flutter

## Оглавление

1. [Введение в TDD для Flutter](#введение-в-tdd-для-flutter)
2. [Алгоритм написания тестов](#алгоритм-написания-тестов)
3. [Типы тестов во Flutter](#типы-тестов-во-flutter)
4. [Тестирование по типам компонентов](#тестирование-по-типам-компонентов)
5. [Пограничные случаи](#пограничные-случаи)
6. [Практические примеры](#практические-примеры)

## Введение в TDD для Flutter

Test-Driven Development (TDD) во Flutter следует тем же принципам, что и классический TDD, но с учетом специфики фреймворка:

1. Написать тест (Red)
2. Реализовать минимальный код для прохождения теста (Green)
3. Провести рефакторинг (Refactor)

Особенности TDD во Flutter:
- Использование пакета `flutter_test` для виджет-тестов
- Применение `mockito` или `mocktail` для мокирования
- Тестирование как бизнес-логики, так и UI-компонентов

## Алгоритм написания тестов

### 1. Подготовка тестового окружения

```dart
void main() {
  late MockNavigator mockNavigator;
  late MockAuthBloc mockAuthBloc;
  late LoginScreen loginScreen;

  setUp(() {
    mockNavigator = MockNavigator();
    mockAuthBloc = MockAuthBloc();
    loginScreen = LoginScreen(
      navigator: mockNavigator,
      authBloc: mockAuthBloc,
    );
  });

  tearDown(() {
    // Очистка после тестов
  });
}
```

### 2. Структура тестового файла

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

class MockNavigator extends Mock implements Navigator {}
class MockAuthBloc extends Mock implements AuthBloc {}

void main() {
  group('LoginScreen', () {
    group('login button', () {
      testWidgets('should show loading indicator when pressed',
          (WidgetTester tester) async {
        // Arrange
        // Act
        // Assert
      });
    });
  });
}
```

## Типы тестов во Flutter

### 1. Unit Tests (Модульные тесты)

```dart
void main() {
  group('AuthService', () {
    late AuthService authService;
    late MockHttpClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockHttpClient();
      authService = AuthService(httpClient: mockHttpClient);
    });

    test('login should return user on success', () async {
      // Arrange
      when(mockHttpClient.post(
        any,
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
        '{"id": 1, "name": "Test User"}',
        200,
      ));

      // Act
      final result = await authService.login(
        email: 'test@example.com',
        password: 'password123',
      );

      // Assert
      expect(result, isA<User>());
      expect(result.name, equals('Test User'));
    });

    test('login should throw AuthException on failure', () async {
      // Arrange
      when(mockHttpClient.post(
        any,
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
        '{"error": "Invalid credentials"}',
        401,
      ));

      // Act & Assert
      expect(
        () => authService.login(
          email: 'test@example.com',
          password: 'wrong_password',
        ),
        throwsA(isA<AuthException>()),
      );
    });
  });
}
```

### 2. Widget Tests (Тесты виджетов)

```dart
void main() {
  group('LoginForm', () {
    testWidgets('should show validation errors for empty fields',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: LoginForm(
            onSubmit: (email, password) async {},
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(
        find.text('Email is required'),
        findsOneWidget,
      );
      expect(
        find.text('Password is required'),
        findsOneWidget,
      );
    });

    testWidgets('should call onSubmit with valid data',
        (WidgetTester tester) async {
      // Arrange
      String? submittedEmail;
      String? submittedPassword;

      await tester.pumpWidget(
        MaterialApp(
          home: LoginForm(
            onSubmit: (email, password) async {
              submittedEmail = email;
              submittedPassword = password;
            },
          ),
        ),
      );

      // Act
      await tester.enterText(
        find.byType(TextFormField).first,
        'test@example.com',
      );
      await tester.enterText(
        find.byType(TextFormField).last,
        'password123',
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(submittedEmail, equals('test@example.com'));
      expect(submittedPassword, equals('password123'));
    });
  });
}
```

### 3. Integration Tests (Интеграционные тесты)

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('end-to-end test', () {
    testWidgets('login flow test', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Act - Navigate to login
      await tester.tap(find.byKey(Key('loginButton')));
      await tester.pumpAndSettle();

      // Enter credentials
      await tester.enterText(
        find.byKey(Key('emailField')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(Key('passwordField')),
        'password123',
      );
      await tester.tap(find.byKey(Key('submitButton')));
      await tester.pumpAndSettle();

      // Assert - Check if we're on the home screen
      expect(find.byKey(Key('homeScreen')), findsOneWidget);
      expect(find.text('Welcome, Test User'), findsOneWidget);
    });
  });
}
```

## Тестирование по типам компонентов

### 1. Stateless Widgets

```dart
void main() {
  group('UserAvatar', () {
    testWidgets('should display user initials when no image',
        (WidgetTester tester) async {
      // Arrange
      final user = User(
        name: 'John Doe',
        imageUrl: null,
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: UserAvatar(user: user),
        ),
      );

      // Assert
      expect(find.text('JD'), findsOneWidget);
      expect(find.byType(CircleAvatar), findsOneWidget);
    });

    testWidgets('should display user image when available',
        (WidgetTester tester) async {
      // Arrange
      final user = User(
        name: 'John Doe',
        imageUrl: 'https://example.com/avatar.jpg',
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: UserAvatar(user: user),
        ),
      );

      // Assert
      expect(find.byType(Image), findsOneWidget);
      final Image image = tester.widget(find.byType(Image));
      expect(
        image.image,
        isA<NetworkImage>(),
      );
    });
  });
}
```

### 2. Stateful Widgets

```dart
void main() {
  group('CounterWidget', () {
    testWidgets('should increment counter when plus button is pressed',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: CounterWidget(),
        ),
      );

      // Act
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();

      // Assert
      expect(find.text('1'), findsOneWidget);
    });

    testWidgets('should decrement counter when minus button is pressed',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: CounterWidget(initialValue: 1),
        ),
      );

      // Act
      await tester.tap(find.byIcon(Icons.remove));
      await tester.pump();

      // Assert
      expect(find.text('0'), findsOneWidget);
    });

    testWidgets('should not go below zero', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: CounterWidget(),
        ),
      );

      // Act
      await tester.tap(find.byIcon(Icons.remove));
      await tester.pump();

      // Assert
      expect(find.text('0'), findsOneWidget);
    });
  });
}
```

### 3. BLoC/Provider

```dart
void main() {
  group('AuthBloc', () {
    late AuthBloc authBloc;
    late MockAuthRepository mockAuthRepository;

    setUp(() {
      mockAuthRepository = MockAuthRepository();
      authBloc = AuthBloc(authRepository: mockAuthRepository);
    });

    tearDown(() {
      authBloc.close();
    });

    blocTest<AuthBloc, AuthState>(
      'emits [loading, authenticated] when login is successful',
      build: () {
        when(mockAuthRepository.login(
          email: anyNamed('email'),
          password: anyNamed('password'),
        )).thenAnswer((_) async => User(id: 1, name: 'Test User'));
        return authBloc;
      },
      act: (bloc) => bloc.add(LoginEvent(
        email: 'test@example.com',
        password: 'password123',
      )),
      expect: () => [
        AuthLoading(),
        AuthAuthenticated(user: User(id: 1, name: 'Test User')),
      ],
    );

    blocTest<AuthBloc, AuthState>(
      'emits [loading, error] when login fails',
      build: () {
        when(mockAuthRepository.login(
          email: anyNamed('email'),
          password: anyNamed('password'),
        )).thenThrow(AuthException('Invalid credentials'));
        return authBloc;
      },
      act: (bloc) => bloc.add(LoginEvent(
        email: 'test@example.com',
        password: 'wrong_password',
      )),
      expect: () => [
        AuthLoading(),
        AuthError(message: 'Invalid credentials'),
      ],
    );
  });
}
```

### 4. Custom Painters

```dart
void main() {
  group('CircleProgressPainter', () {
    testWidgets('should paint circle with correct progress',
        (WidgetTester tester) async {
      // Arrange
      final painter = CircleProgressPainter(
        progress: 0.75,
        color: Colors.blue,
      );

      // Act
      await tester.pumpWidget(
        CustomPaint(
          painter: painter,
          size: Size(100, 100),
        ),
      );

      // Assert using golden test
      await expectLater(
        find.byType(CustomPaint),
        matchesGoldenFile('circle_progress_75.png'),
      );
    });

    test('should calculate correct angles', () {
      // Arrange
      final painter = CircleProgressPainter(
        progress: 0.5,
        color: Colors.blue,
      );

      // Act
      final sweepAngle = painter.calculateSweepAngle();

      // Assert
      expect(sweepAngle, equals(pi));
    });
  });
}
```

### 5. Animations

```dart
void main() {
  group('FadeAnimation', () {
    testWidgets('should animate opacity from 0 to 1',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: FadeAnimation(
            child: Text('Test'),
          ),
        ),
      );

      // Initial state
      expect(
        tester.widget<AnimatedOpacity>(
          find.byType(AnimatedOpacity),
        ).opacity,
        equals(0.0),
      );

      // Act - Wait for animation
      await tester.pump(Duration(milliseconds: 500));

      // Assert - Mid animation
      expect(
        tester.widget<AnimatedOpacity>(
          find.byType(AnimatedOpacity),
        ).opacity,
        greaterThan(0.0),
      );

      // Complete animation
      await tester.pumpAndSettle();

      // Final state
      expect(
        tester.widget<AnimatedOpacity>(
          find.byType(AnimatedOpacity),
        ).opacity,
        equals(1.0),
      );
    });
  });
}
```

## Пограничные случаи

### 1. Размеры экрана и адаптивность

```dart
void main() {
  group('ResponsiveLayout', () {
    testWidgets('should show mobile layout on small screen',
        (WidgetTester tester) async {
      // Arrange
      tester.binding.window.physicalSizeTestValue = Size(320, 480);
      tester.binding.window.devicePixelRatioTestValue = 1.0;

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: ResponsiveLayout(
            mobileLayout: Text('Mobile'),
            tabletLayout: Text('Tablet'),
            desktopLayout: Text('Desktop'),
          ),
        ),
      );

      // Assert
      expect(find.text('Mobile'), findsOneWidget);
      expect(find.text('Tablet'), findsNothing);
      expect(find.text('Desktop'), findsNothing);
    });

    testWidgets('should show desktop layout on large screen',
        (WidgetTester tester) async {
      // Arrange
      tester.binding.window.physicalSizeTestValue = Size(1920, 1080);
      tester.binding.window.devicePixelRatioTestValue = 1.0;

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: ResponsiveLayout(
            mobileLayout: Text('Mobile'),
            tabletLayout: Text('Tablet'),
            desktopLayout: Text('Desktop'),
          ),
        ),
      );

      // Assert
      expect(find.text('Desktop'), findsOneWidget);
      expect(find.text('Mobile'), findsNothing);
      expect(find.text('Tablet'), findsNothing);
    });
  });
}
```

### 2. Локализация

```dart
void main() {
  group('LocalizedWidget', () {
    testWidgets('should display text in English',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          locale: Locale('en'),
          localizationsDelegates: [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
          ],
          home: LocalizedWidget(),
        ),
      );

      // Assert
      expect(find.text('Welcome'), findsOneWidget);
    });

    testWidgets('should display text in Russian',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          locale: Locale('ru'),
          localizationsDelegates: [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
          ],
          home: LocalizedWidget(),
        ),
      );

      // Assert
      expect(find.text('Добро пожаловать'), findsOneWidget);
    });
  });
}
```

### 3. Темы и стили

```dart
void main() {
  group('ThemedWidget', () {
    testWidgets('should apply light theme colors',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData.light(),
          home: ThemedWidget(),
        ),
      );

      // Assert
      final container = tester.widget<Container>(
        find.byType(Container),
      );
      expect(
        container.color,
        equals(Colors.white),
      );
    });

    testWidgets('should apply dark theme colors',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData.dark(),
          home: ThemedWidget(),
        ),
      );

      // Assert
      final container = tester.widget<Container>(
        find.byType(Container),
      );
      expect(
        container.color,
        equals(Colors.black),
      );
    });
  });
}
```

## Практические примеры

### 1. Тестирование формы авторизации

```dart
void main() {
  group('LoginScreen', () {
    late MockAuthBloc mockAuthBloc;

    setUp(() {
      mockAuthBloc = MockAuthBloc();
    });

    testWidgets('should show validation errors',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginScreen(),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(find.text('Email is required'), findsOneWidget);
      expect(find.text('Password is required'), findsOneWidget);
    });

    testWidgets('should show loading indicator during authentication',
        (WidgetTester tester) async {
      // Arrange
      when(() => mockAuthBloc.state).thenReturn(AuthLoading());

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginScreen(),
          ),
        ),
      );

      // Act
      await tester.enterText(
        find.byKey(Key('emailField')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(Key('passwordField')),
        'password123',
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should navigate to home on successful login',
        (WidgetTester tester) async {
      // Arrange
      final user = User(id: 1, name: 'Test User');
      when(() => mockAuthBloc.state)
          .thenReturn(AuthAuthenticated(user: user));

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginScreen(),
          ),
        ),
      );

      // Assert
      verify(
        () => Navigator.of(any()).pushReplacementNamed('/home'),
      ).called(1);
    });

    testWidgets('should show error message on authentication failure',
        (WidgetTester tester) async {
      // Arrange
      when(() => mockAuthBloc.state)
          .thenReturn(AuthError(message: 'Invalid credentials'));

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginScreen(),
          ),
        ),
      );

      // Assert
      expect(find.text('Invalid credentials'), findsOneWidget);
    });
  });
}
```

### 2. Тестирование списка с бесконечной прокруткой

```dart
void main() {
  group('InfiniteListView', () {
    late MockItemsBloc mockItemsBloc;

    setUp(() {
      mockItemsBloc = MockItemsBloc();
    });

    testWidgets('should load initial items',
        (WidgetTester tester) async {
      // Arrange
      final items = List.generate(
        20,
        (i) => Item(id: i, title: 'Item $i'),
      );
      when(() => mockItemsBloc.state).thenReturn(
        ItemsLoaded(items: items, hasReachedMax: false),
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockItemsBloc,
            child: InfiniteListView(),
          ),
        ),
      );

      // Assert
      expect(find.byType(ListTile), findsNWidgets(20));
    });

    testWidgets('should load more items on scroll',
        (WidgetTester tester) async {
      // Arrange
      final items = List.generate(
        20,
        (i) => Item(id: i, title: 'Item $i'),
      );
      when(() => mockItemsBloc.state).thenReturn(
        ItemsLoaded(items: items, hasReachedMax: false),
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockItemsBloc,
            child: InfiniteListView(),
          ),
        ),
      );

      await tester.drag(
        find.byType(ListView),
        Offset(0, -1000),
      );
      await tester.pump();

      // Assert
      verify(() => mockItemsBloc.add(LoadMoreItems())).called(1);
    });

    testWidgets('should show loading indicator at bottom',
        (WidgetTester tester) async {
      // Arrange
      final items = List.generate(
        20,
        (i) => Item(id: i, title: 'Item $i'),
      );
      when(() => mockItemsBloc.state).thenReturn(
        ItemsLoaded(items: items, hasReachedMax: false, isLoading: true),
      );

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockItemsBloc,
            child: InfiniteListView(),
          ),
        ),
      );

      // Scroll to bottom
      await tester.drag(
        find.byType(ListView),
        Offset(0, -1000),
      );
      await tester.pump();

      // Assert
      expect(
        find.byType(CircularProgressIndicator),
        findsOneWidget,
      );
    });
  });
}
```

### 3. Тестирование кастомной анимации

```dart
void main() {
  group('AnimatedLogo', () {
    testWidgets('should complete rotation animation',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: AnimatedLogo(),
        ),
      );

      // Get initial rotation
      final initialRotation = _getRotationValue(tester);

      // Act - Wait half animation
      await tester.pump(Duration(milliseconds: 500));

      // Get mid rotation
      final midRotation = _getRotationValue(tester);

      // Complete animation
      await tester.pumpAndSettle();

      // Get final rotation
      final finalRotation = _getRotationValue(tester);

      // Assert
      expect(initialRotation, equals(0.0));
      expect(midRotation, greaterThan(0.0));
      expect(midRotation, lessThan(pi));
      expect(finalRotation, equals(2 * pi));
    });

    testWidgets('should restart animation on tap',
        (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: AnimatedLogo(),
        ),
      );

      // Complete first animation
      await tester.pumpAndSettle();

      // Act - Tap to restart
      await tester.tap(find.byType(AnimatedLogo));
      await tester.pump();

      // Get rotation after tap
      final rotationAfterTap = _getRotationValue(tester);

      // Assert
      expect(rotationAfterTap, equals(0.0));
    });
  });
}

double _getRotationValue(WidgetTester tester) {
  final transform = tester.widget<Transform>(
    find.byType(Transform),
  );
  final rotation = transform.transform.getRotation();
  return rotation.z;
}
```

Это руководство охватывает основные аспекты TDD тестирования во Flutter и предоставляет практические примеры для различных типов компонентов. Хотите, чтобы я более подробно раскрыл какой-то конкретный аспект?