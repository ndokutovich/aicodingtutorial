# Руководство по TDD тестированию

## Оглавление

1. [Введение в TDD](#введение-в-tdd)
2. [Алгоритм написания тестов](#алгоритм-написания-тестов)
3. [Типы тестов по области видимости](#типы-тестов-по-области-видимости)
4. [Типы тестов по сценариям](#типы-тестов-по-сценариям)
5. [Тестирование по типам классов](#тестирование-по-типам-классов)
6. [Пограничные случаи](#пограничные-случаи)
7. [Практические примеры](#практические-примеры)

## Введение в TDD

Test-Driven Development (TDD) - это методология разработки, где тесты пишутся до реализации функционала. Цикл TDD:

1. Написать тест
2. Убедиться, что тест не проходит (Red)
3. Написать минимальную реализацию
4. Убедиться, что тест проходит (Green)
5. Провести рефакторинг (Refactor)

## Алгоритм написания тестов

### 1. Анализ требований
1. Определить основные функциональные требования
2. Выделить пограничные случаи
3. Определить ожидаемое поведение при ошибках
4. Составить список всех возможных сценариев

### 2. Планирование тестов
1. Разбить функциональность на атомарные части
2. Определить зависимости
3. Спланировать моки и стабы
4. Определить порядок написания тестов

### 3. Структура тестового класса
```typescript
describe('ClassName', () => {
    describe('MethodName', () => {
        describe('Scenario', () => {
            it('should behave as expected when...', () => {
                // Arrange
                // Act
                // Assert
            });
        });
    });
});
```

## Типы тестов по области видимости

### 1. Открытое тестирование (Public API)
- Тестирование публичных методов и интерфейсов
- Проверка контрактов класса
- Тестирование взаимодействия с другими компонентами

Пример:
```typescript
describe('UserService', () => {
    it('should create user with valid data', () => {
        const service = new UserService();
        const user = service.createUser({
            name: 'John',
            email: 'john@example.com'
        });
        expect(user.id).toBeDefined();
    });
});
```

### 2. Закрытое тестирование (Private Implementation)
- Тестирование приватных методов через публичные интерфейсы
- Проверка внутренней логики
- Тестирование состояния объекта

Пример:
```typescript
describe('PasswordHasher', () => {
    it('should properly salt password', () => {
        const hasher = new PasswordHasher();
        const result = hasher.hash('password');
        // Проверяем результат хеширования через публичный метод
        expect(hasher.verify('password', result)).toBe(true);
    });
});
```

## Типы тестов по сценариям

### 1. Позитивные тесты
- Проверка корректных входных данных
- Ожидаемое поведение
- Стандартные сценарии использования

```typescript
describe('Calculator', () => {
    it('should add two positive numbers', () => {
        const calc = new Calculator();
        expect(calc.add(2, 3)).toBe(5);
    });
});
```

### 2. Негативные тесты
- Некорректные входные данные
- Обработка ошибок
- Проверка валидации

```typescript
describe('Calculator', () => {
    it('should throw error when dividing by zero', () => {
        const calc = new Calculator();
        expect(() => calc.divide(5, 0)).toThrow(DivisionByZeroError);
    });
});
```

### 3. Пограничные случаи
- Минимальные/максимальные значения
- Пустые значения
- Специальные символы

```typescript
describe('ArrayUtils', () => {
    it('should handle empty array', () => {
        expect(ArrayUtils.sum([])).toBe(0);
    });
    
    it('should handle array with MAX_SAFE_INTEGER', () => {
        expect(ArrayUtils.sum([Number.MAX_SAFE_INTEGER])).toBe(Number.MAX_SAFE_INTEGER);
    });
});
```

## Тестирование по типам классов

### 1. Entity классы
- Тестирование конструктора
- Валидация полей
- Бизнес-правила
- Методы сравнения

```typescript
describe('User', () => {
    describe('constructor', () => {
        it('should create valid user', () => {
            const user = new User('John', 'john@example.com');
            expect(user.name).toBe('John');
        });

        it('should throw on invalid email', () => {
            expect(() => new User('John', 'invalid-email'))
                .toThrow(ValidationError);
        });
    });

    describe('equals', () => {
        it('should return true for same ID', () => {
            const user1 = new User('John', 'john@example.com');
            const user2 = new User('John', 'john@example.com');
            user1.id = user2.id = 1;
            expect(user1.equals(user2)).toBe(true);
        });
    });
});
```

### 2. Value Objects
- Неизменяемость
- Валидация
- Сравнение
- Форматирование

```typescript
describe('Money', () => {
    describe('immutability', () => {
        it('should create new instance on operations', () => {
            const money1 = new Money(100, 'USD');
            const money2 = money1.add(new Money(50, 'USD'));
            expect(money1.amount).toBe(100);
            expect(money2.amount).toBe(150);
        });
    });

    describe('validation', () => {
        it('should not allow negative amounts', () => {
            expect(() => new Money(-100, 'USD'))
                .toThrow(ValidationError);
        });

        it('should not allow invalid currency', () => {
            expect(() => new Money(100, 'INVALID'))
                .toThrow(ValidationError);
        });
    });
});
```

### 3. Service классы
- Бизнес-логика
- Интеграция с другими сервисами
- Обработка ошибок
- Транзакции

```typescript
describe('PaymentService', () => {
    let paymentService: PaymentService;
    let paymentGatewayMock: jest.Mocked<PaymentGateway>;
    let userRepositoryMock: jest.Mocked<UserRepository>;

    beforeEach(() => {
        paymentGatewayMock = {
            processPayment: jest.fn(),
            refund: jest.fn()
        };
        userRepositoryMock = {
            findById: jest.fn(),
            save: jest.fn()
        };
        paymentService = new PaymentService(
            paymentGatewayMock,
            userRepositoryMock
        );
    });

    describe('processPayment', () => {
        it('should process successful payment', async () => {
            // Arrange
            const userId = 1;
            const amount = new Money(100, 'USD');
            userRepositoryMock.findById.mockResolvedValue(new User('John'));
            paymentGatewayMock.processPayment.mockResolvedValue({
                success: true,
                transactionId: 'tx_123'
            });

            // Act
            const result = await paymentService.processPayment(userId, amount);

            // Assert
            expect(result.success).toBe(true);
            expect(paymentGatewayMock.processPayment).toHaveBeenCalledWith(
                amount,
                expect.any(String)
            );
        });

        it('should handle payment failure', async () => {
            // Arrange
            paymentGatewayMock.processPayment.mockRejectedValue(
                new PaymentError('Insufficient funds')
            );

            // Act & Assert
            await expect(
                paymentService.processPayment(1, new Money(100, 'USD'))
            ).rejects.toThrow(PaymentError);
        });

        it('should rollback on partial failure', async () => {
            // Arrange
            paymentGatewayMock.processPayment.mockResolvedValue({
                success: true,
                transactionId: 'tx_123'
            });
            userRepositoryMock.save.mockRejectedValue(new Error('DB Error'));

            // Act
            try {
                await paymentService.processPayment(1, new Money(100, 'USD'));
            } catch {
                // Assert
                expect(paymentGatewayMock.refund).toHaveBeenCalledWith('tx_123');
            }
        });
    });
});
```

### 4. Repository классы
- CRUD операции
- Поиск и фильтрация
- Транзакции
- Кэширование

```typescript
describe('UserRepository', () => {
    let repository: UserRepository;
    let dbMock: jest.Mocked<Database>;
    let cacheMock: jest.Mocked<Cache>;

    beforeEach(() => {
        dbMock = {
            query: jest.fn(),
            transaction: jest.fn()
        };
        cacheMock = {
            get: jest.fn(),
            set: jest.fn(),
            delete: jest.fn()
        };
        repository = new UserRepository(dbMock, cacheMock);
    });

    describe('findById', () => {
        it('should return from cache if available', async () => {
            // Arrange
            const user = new User('John');
            cacheMock.get.mockResolvedValue(user);

            // Act
            const result = await repository.findById(1);

            // Assert
            expect(result).toBe(user);
            expect(dbMock.query).not.toHaveBeenCalled();
        });

        it('should fetch from DB and cache on cache miss', async () => {
            // Arrange
            const user = new User('John');
            cacheMock.get.mockResolvedValue(null);
            dbMock.query.mockResolvedValue([user]);

            // Act
            const result = await repository.findById(1);

            // Assert
            expect(result).toBe(user);
            expect(cacheMock.set).toHaveBeenCalledWith(
                expect.any(String),
                user,
                expect.any(Number)
            );
        });
    });

    describe('save', () => {
        it('should save to DB and invalidate cache', async () => {
            // Arrange
            const user = new User('John');

            // Act
            await repository.save(user);

            // Assert
            expect(dbMock.query).toHaveBeenCalled();
            expect(cacheMock.delete).toHaveBeenCalled();
        });

        it('should handle transaction rollback', async () => {
            // Arrange
            dbMock.query.mockRejectedValue(new Error('DB Error'));

            // Act & Assert
            await expect(repository.save(new User('John')))
                .rejects.toThrow('DB Error');
        });
    });
});
```

### 5. Controller/Handler классы
- Валидация входных данных
- Маппинг DTO
- Обработка ошибок
- HTTP коды ответов

```typescript
describe('UserController', () => {
    let controller: UserController;
    let userServiceMock: jest.Mocked<UserService>;
    let validatorMock: jest.Mocked<Validator>;

    beforeEach(() => {
        userServiceMock = {
            createUser: jest.fn(),
            updateUser: jest.fn(),
            deleteUser: jest.fn()
        };
        validatorMock = {
            validate: jest.fn()
        };
        controller = new UserController(userServiceMock, validatorMock);
    });

    describe('createUser', () => {
        it('should return 201 on successful creation', async () => {
            // Arrange
            const dto = { name: 'John', email: 'john@example.com' };
            validatorMock.validate.mockResolvedValue(true);
            userServiceMock.createUser.mockResolvedValue(new User('John'));

            // Act
            const response = await controller.createUser(dto);

            // Assert
            expect(response.statusCode).toBe(201);
            expect(response.body).toHaveProperty('id');
        });

        it('should return 400 on validation failure', async () => {
            // Arrange
            validatorMock.validate.mockResolvedValue(false);

            // Act
            const response = await controller.createUser({});

            // Assert
            expect(response.statusCode).toBe(400);
        });

        it('should return 409 on duplicate email', async () => {
            // Arrange
            validatorMock.validate.mockResolvedValue(true);
            userServiceMock.createUser.mockRejectedValue(
                new DuplicateEmailError()
            );

            // Act
            const response = await controller.createUser({
                name: 'John',
                email: 'existing@example.com'
            });

            // Assert
            expect(response.statusCode).toBe(409);
        });
    });
});
```

## Пограничные случаи

### 1. Числовые значения
- Минимальные/максимальные значения типа
- Ноль
- Отрицательные числа
- Дроби
- NaN/Infinity

```typescript
describe('NumberValidator', () => {
    const validator = new NumberValidator();

    describe('validate', () => {
        it.each([
            [Number.MIN_SAFE_INTEGER, true],
            [Number.MAX_SAFE_INTEGER, true],
            [0, true],
            [-1, true],
            [0.1, true],
            [NaN, false],
            [Infinity, false],
            [-Infinity, false]
        ])('should validate %p as %p', (input, expected) => {
            expect(validator.validate(input)).toBe(expected);
        });
    });
});
```

### 2. Строки
- Пустая строка
- Очень длинная строка
- Спецсимволы
- Многострочный текст
- Unicode символы

```typescript
describe('StringValidator', () => {
    const validator = new StringValidator();

    describe('validate', () => {
        it.each([
            ['', false],
            ['a'.repeat(1000), false],
            ['Hello\nWorld', true],
            ['Hello!@#$%^&*()', true],
            ['Привет мир', true],
            ['🌍🌎🌏', true]
        ])('should validate %p as %p', (input, expected) => {
            expect(validator.validate(input)).toBe(expected);
        });
    });
});
```

### 3. Массивы
- Пустой массив
- Один элемент
- Много элементов
- Дубликаты
- Вложенные массивы

```typescript
describe('ArrayUtils', () => {
    describe('unique', () => {
        it.each([
            [[], []],
            [[1], [1]],
            [[1, 1, 2, 2], [1, 2]],
            [[1, [2, 2], 3], [1, [2, 2], 3]]
        ])('should handle %p and return %p', (input, expected) => {
            expect(ArrayUtils.unique(input)).toEqual(expected);
        });
    });
});
```

### 4. Объекты
- Пустой объект
- Отсутствующие поля
- Null значения
- Циклические ссылки
- Наследование

```typescript
describe('ObjectValidator', () => {
    describe('validate', () => {
        it('should handle empty object', () => {
            expect(ObjectValidator.validate({})).toBe(false);
        });

        it('should handle missing optional fields', () => {
            const obj = { required: 'value' };
            expect(ObjectValidator.validate(obj)).toBe(true);
        });

        it('should handle null values', () => {
            const obj = { field: null };
            expect(ObjectValidator.validate(obj)).toBe(false);
        });

        it('should handle inherited properties', () => {
            class Parent {
                parentField = 'value';
            }
            class Child extends Parent {
                childField = 'value';
            }
            expect(ObjectValidator.validate(new Child())).toBe(true);
        });
    });
});
```

## Практические примеры

### 1. Тестирование аутентификации

```typescript
describe('AuthService', () => {
    let authService: AuthService;
    let userRepositoryMock: jest.Mocked<UserRepository>;
    let tokenServiceMock: jest.Mocked<TokenService>;
    let hasherMock: jest.Mocked<PasswordHasher>;

    beforeEach(() => {
        userRepositoryMock = {
            findByEmail: jest.fn(),
            save: jest.fn()
        };
        tokenServiceMock = {
            generateToken: jest.fn(),
            verifyToken: jest.fn(),
            revokeToken: jest.fn()
        };
        hasherMock = {
            hash: jest.fn(),
            verify: jest.fn()
        };
        authService = new AuthService(
            userRepositoryMock,
            tokenServiceMock,
            hasherMock
        );
    });

    describe('login', () => {
        it('should authenticate valid credentials', async () => {
            // Arrange
            const credentials = {
                email: 'user@example.com',
                password: 'password123'
            };
            const user = new User('Test User');
            userRepositoryMock.findByEmail.mockResolvedValue(user);
            hasherMock.verify.mockResolvedValue(true);
            tokenServiceMock.generateToken.mockResolvedValue('token');

            // Act
            const result = await authService.login(credentials);

            // Assert
            expect(result.success).toBe(true);
            expect(result.token).toBe('token');
        });

        it('should fail with invalid email', async () => {
            // Arrange
            userRepositoryMock.findByEmail.mockResolvedValue(null);

            // Act & Assert
            await expect(authService.login({
                email: 'invalid@example.com',
                password: 'password123'
            })).rejects.toThrow(AuthenticationError);
        });

        it('should fail with invalid password', async () => {
            // Arrange
            userRepositoryMock.findByEmail.mockResolvedValue(new User('Test'));
            hasherMock.verify.mockResolvedValue(false);

            // Act & Assert
            await expect(authService.login({
                email: 'user@example.com',
                password: 'wrongpass'
            })).rejects.toThrow(AuthenticationError);
        });

        it('should handle locked account', async () => {
            // Arrange
            const lockedUser = new User('Locked User');
            lockedUser.locked = true;
            userRepositoryMock.findByEmail.mockResolvedValue(lockedUser);

            // Act & Assert
            await expect(authService.login({
                email: 'locked@example.com',
                password: 'password123'
            })).rejects.toThrow(AccountLockedError);
        });
    });

    describe('logout', () => {
        it('should revoke token', async () => {
            // Arrange
            const token = 'valid_token';
            tokenServiceMock.verifyToken.mockResolvedValue({ userId: 1 });

            // Act
            await authService.logout(token);

            // Assert
            expect(tokenServiceMock.revokeToken).toHaveBeenCalledWith(token);
        });

        it('should handle invalid token', async () => {
            // Arrange
            tokenServiceMock.verifyToken.mockRejectedValue(
                new TokenValidationError()
            );

            // Act & Assert
            await expect(authService.logout('invalid_token'))
                .rejects.toThrow(TokenValidationError);
        });
    });
});
```

### 2. Тестирование валидации форм

```typescript
describe('FormValidator', () => {
    let validator: FormValidator;

    beforeEach(() => {
        validator = new FormValidator();
    });

    describe('validateRegistrationForm', () => {
        const validForm = {
            username: 'johndoe',
            email: 'john@example.com',
            password: 'Password123!',
            confirmPassword: 'Password123!',
            age: 25
        };

        it('should pass with valid data', () => {
            expect(validator.validate(validForm)).toEqual({
                valid: true,
                errors: {}
            });
        });

        describe('username validation', () => {
            it.each([
                ['', 'Username is required'],
                ['a', 'Username must be at least 3 characters'],
                ['a'.repeat(51), 'Username must be at most 50 characters'],
                ['user@name', 'Username can only contain letters, numbers and underscores'],
                ['admin', 'Username is reserved']
            ])('should validate username %p', (username, expectedError) => {
                const form = { ...validForm, username };
                const result = validator.validate(form);
                expect(result.valid).toBe(false);
                expect(result.errors.username).toBe(expectedError);
            });
        });

        describe('email validation', () => {
            it.each([
                ['', 'Email is required'],
                ['notanemail', 'Invalid email format'],
                ['test@', 'Invalid email format'],
                ['@example.com', 'Invalid email format'],
                ['a'.repeat(100) + '@example.com', 'Email is too long']
            ])('should validate email %p', (email, expectedError) => {
                const form = { ...validForm, email };
                const result = validator.validate(form);
                expect(result.valid).toBe(false);
                expect(result.errors.email).toBe(expectedError);
            });
        });

        describe('password validation', () => {
            it.each([
                ['', 'Password is required'],
                ['short', 'Password must be at least 8 characters'],
                ['onlylowercase', 'Password must contain at least one uppercase letter'],
                ['ONLYUPPERCASE', 'Password must contain at least one lowercase letter'],
                ['NoNumbers!', 'Password must contain at least one number'],
                ['NoSpecial1', 'Password must contain at least one special character']
            ])('should validate password %p', (password, expectedError) => {
                const form = { ...validForm, password, confirmPassword: password };
                const result = validator.validate(form);
                expect(result.valid).toBe(false);
                expect(result.errors.password).toBe(expectedError);
            });

            it('should validate password confirmation', () => {
                const form = {
                    ...validForm,
                    confirmPassword: 'DifferentPassword123!'
                };
                const result = validator.validate(form);
                expect(result.valid).toBe(false);
                expect(result.errors.confirmPassword)
                    .toBe('Passwords do not match');
            });
        });

        describe('age validation', () => {
            it.each([
                [null, 'Age is required'],
                [-1, 'Age must be positive'],
                [17, 'Must be at least 18 years old'],
                [151, 'Invalid age'],
                [25.5, 'Age must be a whole number']
            ])('should validate age %p', (age, expectedError) => {
                const form = { ...validForm, age };
                const result = validator.validate(form);
                expect(result.valid).toBe(false);
                expect(result.errors.age).toBe(expectedError);
            });
        });
    });
});
```

### 3. Тестирование бизнес-логики

```typescript
describe('OrderService', () => {
    let orderService: OrderService;
    let productRepositoryMock: jest.Mocked<ProductRepository>;
    let orderRepositoryMock: jest.Mocked<OrderRepository>;
    let paymentServiceMock: jest.Mocked<PaymentService>;
    let inventoryServiceMock: jest.Mocked<InventoryService>;

    beforeEach(() => {
        productRepositoryMock = {
            findById: jest.fn(),
            save: jest.fn()
        };
        orderRepositoryMock = {
            create: jest.fn(),
            save: jest.fn(),
            findById: jest.fn()
        };
        paymentServiceMock = {
            processPayment: jest.fn(),
            refundPayment: jest.fn()
        };
        inventoryServiceMock = {
            checkAvailability: jest.fn(),
            reserveItems: jest.fn(),
            releaseItems: jest.fn()
        };

        orderService = new OrderService(
            productRepositoryMock,
            orderRepositoryMock,
            paymentServiceMock,
            inventoryServiceMock
        );
    });

    describe('createOrder', () => {
        const orderData = {
            userId: 1,
            items: [
                { productId: 1, quantity: 2 },
                { productId: 2, quantity: 1 }
            ],
            shippingAddress: {
                street: '123 Main St',
                city: 'Test City',
                country: 'Test Country',
                postalCode: '12345'
            },
            paymentMethod: {
                type: 'CREDIT_CARD',
                cardNumber: '**** **** **** 1234',
                expiryDate: '12/25'
            }
        };

        const mockProducts = [
            { id: 1, price: 100, name: 'Product 1' },
            { id: 2, price: 150, name: 'Product 2' }
        ];

        beforeEach(() => {
            // Setup common mock responses
            productRepositoryMock.findById.mockImplementation(async (id) => 
                mockProducts.find(p => p.id === id)
            );
            inventoryServiceMock.checkAvailability.mockResolvedValue(true);
            inventoryServiceMock.reserveItems.mockResolvedValue(true);
            paymentServiceMock.processPayment.mockResolvedValue({
                success: true,
                transactionId: 'tx_123'
            });
        });

        it('should create order successfully', async () => {
            // Arrange
            const expectedTotal = 350; // (100 * 2) + (150 * 1)

            // Act
            const result = await orderService.createOrder(orderData);

            // Assert
            expect(result.success).toBe(true);
            expect(result.order.total).toBe(expectedTotal);
            expect(inventoryServiceMock.reserveItems).toHaveBeenCalled();
            expect(paymentServiceMock.processPayment).toHaveBeenCalledWith(
                expectedTotal,
                orderData.paymentMethod
            );
        });

        it('should fail when product not found', async () => {
            // Arrange
            productRepositoryMock.findById.mockResolvedValue(null);

            // Act & Assert
            await expect(orderService.createOrder(orderData))
                .rejects.toThrow(ProductNotFoundError);
        });

        it('should fail when insufficient inventory', async () => {
            // Arrange
            inventoryServiceMock.checkAvailability.mockResolvedValue(false);

            // Act & Assert
            await expect(orderService.createOrder(orderData))
                .rejects.toThrow(InsufficientInventoryError);
        });

        it('should rollback on payment failure', async () => {
            // Arrange
            paymentServiceMock.processPayment.mockRejectedValue(
                new PaymentError('Payment declined')
            );

            // Act
            try {
                await orderService.createOrder(orderData);
            } catch (error) {
                // Assert
                expect(error).toBeInstanceOf(PaymentError);
                expect(inventoryServiceMock.releaseItems).toHaveBeenCalled();
            }
        });

        it('should handle concurrent inventory updates', async () => {
            // Arrange
            let firstCheck = true;
            inventoryServiceMock.checkAvailability.mockImplementation(() => {
                if (firstCheck) {
                    firstCheck = false;
                    return Promise.resolve(true);
                }
                return Promise.resolve(false);
            });

            // Act & Assert
            await expect(orderService.createOrder(orderData))
                .rejects.toThrow(ConcurrencyError);
        });
    });

    describe('calculateDiscount', () => {
        it.each([
            [100, 0, 100],    // No discount
            [100, 10, 90],    // 10% discount
            [100, 100, 0],    // 100% discount
            [100, 110, 0]     // Discount > 100%
        ])('should calculate total %p with discount %p% as %p', 
            (amount, discountPercent, expected) => {
                expect(orderService.calculateDiscount(amount, discountPercent))
                    .toBe(expected);
        });
    });
});
```

Это руководство охватывает основные аспекты TDD тестирования и предоставляет практические примеры для различных типов классов и сценариев. Хотите, чтобы я более подробно раскрыл какой-то конкретный аспект? 

# Руководство по TDD тестированию Flutter компонентов

## Типы тестов во Flutter

| Тип теста | Описание | Инструменты | Применение | Особенности |
|-----------|----------|-------------|------------|-------------|
| Unit тесты | Тестирование отдельных классов и функций | `test`, `mockito` | Бизнес-логика, сервисы, утилиты | - Изолированное тестирование<br>- Быстрое выполнение<br>- Легкое поддержание |
| Widget тесты | Тестирование отдельных виджетов | `flutter_test`, `WidgetTester` | UI компоненты, формы, анимации | - Тестирование рендеринга<br>- Симуляция взаимодействия<br>- Проверка состояний |
| Integration тесты | Тестирование взаимодействия компонентов | `integration_test` | Полные экраны, навигация, бизнес-процессы | - End-to-end тестирование<br>- Реальное окружение<br>- Проверка интеграции |
| Golden тесты | Тестирование визуального соответствия | `golden_toolkit` | UI дизайн, верстка, темизация | - Пиксельное сравнение<br>- Разные размеры экрана<br>- Разные платформы |
| Performance тесты | Тестирование производительности | `flutter_driver` | Скорость работы, память, CPU | - Метрики производительности<br>- Профилирование<br>- Оптимизация |

### 1. Unit тесты
```typescript
describe('ClassName', () => {
    describe('MethodName', () => {
        describe('Scenario', () => {
            it('should behave as expected when...', () => {
                // Arrange
                // Act
                // Assert
            });
        });
    });
});
```

### 2. Widget тесты
```typescript
describe('ClassName', () => {
    describe('MethodName', () => {
        describe('Scenario', () => {
            it('should behave as expected when...', () => {
                // Arrange
                // Act
                // Assert
            });
        });
    });
});
```

### 3. Integration тесты
```typescript
describe('ClassName', () => {
    describe('MethodName', () => {
        describe('Scenario', () => {
            it('should behave as expected when...', () => {
                // Arrange
                // Act
                // Assert
            });
        });
    });
});
```

### 4. Golden тесты
```typescript
describe('ClassName', () => {
    describe('MethodName', () => {
        describe('Scenario', () => {
            it('should behave as expected when...', () => {
                // Arrange
                // Act
                // Assert
            });
        });
    });
});
```

### 5. Performance тесты
```typescript
describe('ClassName', () => {
    describe('MethodName', () => {
        describe('Scenario', () => {
            it('should behave as expected when...', () => {
                // Arrange
                // Act
                // Assert
            });
        });
    });
}); 