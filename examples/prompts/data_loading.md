# Промт: Загрузка и парсинг данных

На основе данного HTML создай модель данных и парсер, который извлечет данные о сотрудниках и их отпусках. Создай репозиторий отпусков с 3 вариантами загрузки: на сегодня, на завтра, на 1 год вперед.

HTML для парсинга:
```html
<table class="vacations-table">
  <thead>
    <tr>
      <th>ID</th>
      <th>Сотрудник</th>
      <th>Отдел</th>
      <th>Тип отсутствия</th>
      <th>Дата начала</th>
      <th>Дата окончания</th>
      <th>Статус</th>
    </tr>
  </thead>
  <tbody>
    <tr class="vacation-row">
      <td>12345</td>
      <td>Иванов Иван Иванович</td>
      <td>Разработка</td>
      <td>Отпуск</td>
      <td>2024-04-15</td>
      <td>2024-04-28</td>
      <td>Утвержден</td>
    </tr>
    <tr class="vacation-row">
      <td>12346</td>
      <td>Петрова Анна Сергеевна</td>
      <td>Маркетинг</td>
      <td>Больничный</td>
      <td>2024-04-10</td>
      <td>2024-04-12</td>
      <td>Утвержден</td>
    </tr>
    <tr class="vacation-row">
      <td>12347</td>
      <td>Сидоров Алексей Петрович</td>
      <td>Продажи</td>
      <td>Командировка</td>
      <td>2024-04-20</td>
      <td>2024-04-30</td>
      <td>В обработке</td>
    </tr>
  </tbody>
</table>
```

Требования:
1. Создай модель данных `VacationRecord` со следующими полями:
   - id: String
   - employeeName: String
   - department: String
   - absenceType: AbsenceType (enum с вариантами: Vacation, SickLeave, BusinessTrip, Other)
   - startDate: DateTime
   - endDate: DateTime
   - status: VacationStatus (enum с вариантами: Approved, Pending, Rejected)

2. Реализуй парсер HTML с использованием библиотеки html или BeautifulSoup (если Python) или html_parser (если Dart/Flutter)

3. Создай репозиторий `VacationRepository` со следующими методами:
   - `Future<List<VacationRecord>> getVacationsForToday()`
   - `Future<List<VacationRecord>> getVacationsForTomorrow()`
   - `Future<List<VacationRecord>> getVacationsForYear()`
   - `Future<List<VacationRecord>> getVacationsByDateRange(DateTime start, DateTime end)`
   - `Future<List<VacationRecord>> getVacationsByEmployee(String employeeName)`

4. Добавь кэширование данных для оптимизации загрузки

5. Реализуй обработку ошибок при загрузке и парсинге

6. Структура должна позволять легко заменить источник данных (например, с HTML на JSON API)

7. Используй паттерн Repository и Factory для создания моделей данных

Пример использования ожидаемого результата:
```dart
final repository = VacationRepository();

// Получение отпусков на сегодня
final todayVacations = await repository.getVacationsForToday();

// Фильтрация по отделу
final devDepartmentVacations = todayVacations
    .where((vacation) => vacation.department == "Разработка")
    .toList();

// Получение отпусков в определенном диапазоне
final nextMonthVacations = await repository.getVacationsByDateRange(
  DateTime.now(),
  DateTime.now().add(Duration(days: 30))
);
```

Важно учесть возможные изменения в структуре HTML в будущем и сделать парсер достаточно гибким. 