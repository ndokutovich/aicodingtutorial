# Руководство по TDD тестированию Flutter компонентов

## Оглавление

1. [Введение в TDD для Flutter](#введение-в-tdd-для-flutter)
2. [Настройка тестового окружения](#настройка-тестового-окружения)
3. [Типы тестов во Flutter](#типы-тестов-во-flutter)
4. [Тестирование по типам компонентов](#тестирование-по-типам-компонентов)
5. [Пограничные случаи](#пограничные-случаи)
6. [Практические примеры](#практические-примеры)

## Введение в TDD для Flutter

Test-Driven Development (TDD) во Flutter следует тем же принципам, что и классический TDD:

1. Написать тест
2. Убедиться, что тест не проходит (Red)
3. Написать минимальную реализацию
4. Убедиться, что тест проходит (Green)
5. Провести рефакторинг (Refactor)

Особенности TDD во Flutter:
- Использование специальных тестовых виджетов
- Асинхронное тестирование
- Тестирование состояний и жизненного цикла
- Моки для внешних зависимостей

## Настройка тестового окружения

### 1. Зависимости в pubspec.yaml
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.4
  build_runner: ^2.4.8
  bloc_test: ^9.1.5
  golden_toolkit: ^0.15.0
```

### 2. Структура тестов
```
test/
  ├── unit/
  │   ├── services/
  │   ├── repositories/
  │   └── models/
  ├── widget/
  │   ├── screens/
  │   └── components/
  ├── integration/
  └── golden/
```

### 3. Базовая конфигурация теста
```dart
void main() {
  group('ComponentName', () {
    late MockDependency mockDependency;
    
    setUp(() {
      mockDependency = MockDependency();
    });

    testWidgets('description', (WidgetTester tester) async {
      // Arrange
      // Act
      // Assert
    });
  });
}
```

## Типы тестов во Flutter

### 1. Unit тесты
```dart
void main() {
  group('AuthService', () {
    late AuthService authService;
    late MockAuthRepository mockAuthRepository;

    setUp(() {
      mockAuthRepository = MockAuthRepository();
      authService = AuthService(mockAuthRepository);
    });

    test('login should return user on success', () async {
      // Arrange
      final credentials = LoginCredentials(
        email: 'test@example.com',
        password: 'password123'
      );
      when(mockAuthRepository.login(any))
          .thenAnswer((_) async => User(id: '1', email: credentials.email));

      // Act
      final result = await authService.login(credentials);

      // Assert
      expect(result.id, '1');
      expect(result.email, credentials.email);
      verify(mockAuthRepository.login(credentials)).called(1);
    });

    test('login should throw on invalid credentials', () async {
      // Arrange
      when(mockAuthRepository.login(any))
          .thenThrow(AuthException('Invalid credentials'));

      // Act & Assert
      expect(
        () => authService.login(LoginCredentials(
          email: 'invalid@example.com',
          password: 'wrong'
        )),
        throwsA(isA<AuthException>())
      );
    });
  });
}
```

### 2. Widget тесты
```dart
void main() {
  group('LoginForm', () {
    late MockAuthBloc mockAuthBloc;

    setUp(() {
      mockAuthBloc = MockAuthBloc();
    });

    testWidgets('should show validation errors', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginForm(),
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

    testWidgets('should submit form with valid data', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginForm(),
          ),
        ),
      );

      // Act
      await tester.enterText(
        find.byKey(Key('emailField')),
        'test@example.com'
      );
      await tester.enterText(
        find.byKey(Key('passwordField')),
        'password123'
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      verify(mockAuthBloc.add(LoginSubmitted(
        email: 'test@example.com',
        password: 'password123'
      ))).called(1);
    });
  });
}
```

### 3. Integration тесты
```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('End-to-end test', () {
    testWidgets('complete login flow', (tester) async {
      // Arrange
      app.main();
      await tester.pumpAndSettle();

      // Act - Navigate to login
      await tester.tap(find.byKey(Key('loginButton')));
      await tester.pumpAndSettle();

      // Enter credentials
      await tester.enterText(
        find.byKey(Key('emailField')),
        'test@example.com'
      );
      await tester.enterText(
        find.byKey(Key('passwordField')),
        'password123'
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pumpAndSettle();

      // Assert - Check navigation to home
      expect(find.byType(HomeScreen), findsOneWidget);
      expect(find.byType(LoginScreen), findsNothing);
    });
  });
}
```

## Тестирование по типам компонентов

### 1. Stateless Widgets
```dart
void main() {
  group('UserAvatar', () {
    testWidgets('should display image from URL', (tester) async {
      // Arrange
      const imageUrl = 'https://example.com/avatar.jpg';
      
      await tester.pumpWidget(
        MaterialApp(
          home: UserAvatar(imageUrl: imageUrl),
        ),
      );

      // Assert
      expect(find.byType(Image), findsOneWidget);
      final Image image = tester.widget(find.byType(Image));
      expect(
        image.image,
        isA<NetworkImage>().having(
          (i) => i.url,
          'url',
          imageUrl
        ),
      );
    });

    testWidgets('should show placeholder on error', (tester) async {
      // Arrange
      const invalidUrl = 'invalid-url';
      
      await tester.pumpWidget(
        MaterialApp(
          home: UserAvatar(imageUrl: invalidUrl),
        ),
      );

      // Trigger error
      await tester.pump();

      // Assert
      expect(find.byIcon(Icons.person), findsOneWidget);
    });
  });
}
```

### 2. Stateful Widgets
```dart
void main() {
  group('CounterWidget', () {
    testWidgets('should increment counter', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(home: CounterWidget()),
      );

      // Initial state
      expect(find.text('0'), findsOneWidget);

      // Act
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();

      // Assert
      expect(find.text('1'), findsOneWidget);
    });

    testWidgets('should handle state restoration', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          restorationScopeId: 'root',
          home: CounterWidget(),
        ),
      );

      // Act - Increment and trigger state save
      await tester.tap(find.byIcon(Icons.add));
      await tester.pump();
      
      // Simulate app restart
      await tester.restartAndRestore();

      // Assert
      expect(find.text('1'), findsOneWidget);
    });
  });
}
```

### 3. BLoC/Provider компоненты
```dart
void main() {
  group('TodoList with BLoC', () {
    late MockTodoBloc mockTodoBloc;

    setUp(() {
      mockTodoBloc = MockTodoBloc();
    });

    testWidgets('should render list of todos', (tester) async {
      // Arrange
      final todos = [
        Todo(id: '1', title: 'Task 1'),
        Todo(id: '2', title: 'Task 2'),
      ];

      when(() => mockTodoBloc.state)
          .thenReturn(TodoLoaded(todos: todos));

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockTodoBloc,
            child: TodoList(),
          ),
        ),
      );

      // Assert
      expect(find.text('Task 1'), findsOneWidget);
      expect(find.text('Task 2'), findsOneWidget);
    });

    testWidgets('should handle loading state', (tester) async {
      // Arrange
      when(() => mockTodoBloc.state)
          .thenReturn(TodoLoading());

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockTodoBloc,
            child: TodoList(),
          ),
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should handle error state', (tester) async {
      // Arrange
      when(() => mockTodoBloc.state)
          .thenReturn(TodoError(message: 'Failed to load todos'));

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockTodoBloc,
            child: TodoList(),
          ),
        ),
      );

      // Assert
      expect(find.text('Failed to load todos'), findsOneWidget);
      expect(find.byType(RetryButton), findsOneWidget);
    });
  });
}
```

### 4. Custom Painters
```dart
void main() {
  group('CircleProgressPainter', () {
    testWidgets('should paint progress circle', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: CustomPaint(
            painter: CircleProgressPainter(
              progress: 0.75,
              color: Colors.blue,
            ),
            size: Size(100, 100),
          ),
        ),
      );

      // Assert using Golden test
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
      final angle = painter.calculateAngle();

      // Assert
      expect(angle, pi);
    });
  });
}
```

### 5. Анимации
```dart
void main() {
  group('FadeAnimation', () {
    testWidgets('should animate opacity', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: FadeAnimation(
            child: Text('Fade me'),
          ),
        ),
      );

      // Initial state
      expect(
        tester.widget<AnimatedOpacity>(
          find.byType(AnimatedOpacity)
        ).opacity,
        0.0
      );

      // Act - Wait for animation
      await tester.pump(Duration(milliseconds: 500));

      // Assert - Mid animation
      var opacity = tester.widget<AnimatedOpacity>(
        find.byType(AnimatedOpacity)
      ).opacity;
      expect(opacity, greaterThan(0.0));
      expect(opacity, lessThan(1.0));

      // Complete animation
      await tester.pumpAndSettle();

      // Assert - Final state
      expect(
        tester.widget<AnimatedOpacity>(
          find.byType(AnimatedOpacity)
        ).opacity,
        1.0
      );
    });
  });
}
```

## Пограничные случаи

### 1. Размеры экрана
```dart
void main() {
  group('ResponsiveLayout', () {
    testWidgets('should adapt to different screen sizes', (tester) async {
      // Test small screen
      tester.binding.window.physicalSizeTestValue = Size(320, 480);
      await tester.pumpWidget(
        MaterialApp(home: ResponsiveLayout())
      );
      expect(find.byType(MobileLayout), findsOneWidget);
      expect(find.byType(TabletLayout), findsNothing);

      // Test tablet screen
      tester.binding.window.physicalSizeTestValue = Size(768, 1024);
      await tester.pumpWidget(
        MaterialApp(home: ResponsiveLayout())
      );
      expect(find.byType(TabletLayout), findsOneWidget);
      expect(find.byType(MobileLayout), findsNothing);
    });
  });
}
```

### 2. Локализация
```dart
void main() {
  group('LocalizedWidget', () {
    testWidgets('should display correct translations', (tester) async {
      // Test English
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
      expect(find.text('Welcome'), findsOneWidget);

      // Test Russian
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
      expect(find.text('Добро пожаловать'), findsOneWidget);
    });
  });
}
```

### 3. Темы
```dart
void main() {
  group('ThemeAwareWidget', () {
    testWidgets('should adapt to theme changes', (tester) async {
      // Test light theme
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData.light(),
          home: ThemeAwareWidget(),
        ),
      );
      expect(
        tester.widget<Container>(find.byType(Container)).color,
        Colors.white
      );

      // Test dark theme
      await tester.pumpWidget(
        MaterialApp(
          theme: ThemeData.dark(),
          home: ThemeAwareWidget(),
        ),
      );
      expect(
        tester.widget<Container>(find.byType(Container)).color,
        Colors.black
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

    testWidgets('should validate form fields', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockAuthBloc,
            child: LoginScreen(),
          ),
        ),
      );

      // Act - Submit empty form
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert - Check validation messages
      expect(find.text('Email is required'), findsOneWidget);
      expect(find.text('Password is required'), findsOneWidget);

      // Act - Enter invalid email
      await tester.enterText(
        find.byKey(Key('emailField')),
        'invalid-email'
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert - Check email validation
      expect(find.text('Invalid email format'), findsOneWidget);

      // Act - Enter valid data
      await tester.enterText(
        find.byKey(Key('emailField')),
        'test@example.com'
      );
      await tester.enterText(
        find.byKey(Key('passwordField')),
        'password123'
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert - Form submission
      verify(mockAuthBloc.add(LoginSubmitted(
        email: 'test@example.com',
        password: 'password123'
      ))).called(1);
    });

    testWidgets('should show loading indicator', (tester) async {
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

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.byType(ElevatedButton), findsNothing);
    });

    testWidgets('should show error message', (tester) async {
      // Arrange
      when(() => mockAuthBloc.state)
          .thenReturn(AuthError('Invalid credentials'));

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
  group('InfiniteScrollList', () {
    late MockItemBloc mockItemBloc;

    setUp(() {
      mockItemBloc = MockItemBloc();
    });

    testWidgets('should load more items on scroll', (tester) async {
      // Arrange
      final items = List.generate(
        20,
        (i) => ListItem(id: '$i', title: 'Item $i')
      );

      when(() => mockItemBloc.state).thenReturn(
        ItemLoaded(items: items, hasReachedMax: false)
      );

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockItemBloc,
            child: InfiniteScrollList(),
          ),
        ),
      );

      // Act - Scroll to bottom
      await tester.drag(
        find.byType(ListView),
        Offset(0, -1000)
      );
      await tester.pump();

      // Assert
      verify(mockItemBloc.add(LoadMoreItems())).called(1);
    });

    testWidgets('should show loading indicator', (tester) async {
      // Arrange
      final items = List.generate(
        20,
        (i) => ListItem(id: '$i', title: 'Item $i')
      );

      when(() => mockItemBloc.state).thenReturn(
        ItemLoaded(
          items: items,
          hasReachedMax: false,
          isLoadingMore: true
        )
      );

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockItemBloc,
            child: InfiniteScrollList(),
          ),
        ),
      );

      // Assert
      expect(
        find.byKey(Key('bottomLoader')),
        findsOneWidget
      );
    });

    testWidgets('should handle refresh', (tester) async {
      // Arrange
      when(() => mockItemBloc.state).thenReturn(
        ItemLoaded(items: [], hasReachedMax: false)
      );

      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider.value(
            value: mockItemBloc,
            child: InfiniteScrollList(),
          ),
        ),
      );

      // Act - Pull to refresh
      await tester.drag(
        find.byType(RefreshIndicator),
        Offset(0, 100)
      );
      await tester.pump();

      // Assert
      verify(mockItemBloc.add(RefreshItems())).called(1);
    });
  });
}
```

### 3. Тестирование навигации
```dart
void main() {
  group('AppNavigator', () {
    late MockNavigatorObserver mockObserver;

    setUp(() {
      mockObserver = MockNavigatorObserver();
    });

    testWidgets('should handle navigation flow', (tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          navigatorObservers: [mockObserver],
          home: AppNavigator(),
        ),
      );

      // Act - Navigate to login
      await tester.tap(find.byKey(Key('loginButton')));
      await tester.pumpAndSettle();

      // Assert
      verify(mockObserver.didPush(any, any));
      expect(find.byType(LoginScreen), findsOneWidget);

      // Act - Navigate back
      await tester.tap(find.byKey(Key('backButton')));
      await tester.pumpAndSettle();

      // Assert
      verify(mockObserver.didPop(any, any));
      expect(find.byType(HomeScreen), findsOneWidget);
    });

    testWidgets('should handle deep linking', (tester) async {
      // Arrange
      final uri = Uri.parse('myapp://products/123');

      await tester.pumpWidget(
        MaterialApp(
          navigatorObservers: [mockObserver],
          home: AppNavigator(initialUri: uri),
        ),
      );

      // Assert
      expect(find.byType(ProductScreen), findsOneWidget);
      expect(
        find.byKey(Key('productId-123')),
        findsOneWidget
      );
    });
  });
}
```

Это руководство охватывает основные аспекты TDD тестирования во Flutter и предоставляет практические примеры для различных типов компонентов и сценариев. Хотите, чтобы я более подробно раскрыл какой-то конкретный аспект? 