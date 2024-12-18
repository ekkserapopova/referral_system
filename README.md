# API документация для риферальной системы

Данный API предназначен для реализации риферальной системы, включающей верификацию номеров телефонов, генерацию кодов для приглашений, создание и управление пользователями, а также аутентификацию через JWT токены.

## Оглавление

1. [Описание эндпоинтов](#описание-эндпоинтов)
    - [POST /auth/send_code/](#post-authsendcode)
    - [POST /auth/check_code/](#post-authcheckcode)
    - [POST /invite/](#post-invite)
    - [GET /users/](#get-users)
2. [Пример использования API](#пример-использования-api)
3. [Логирование](#логирование)

## Описание эндпоинтов

### POST /auth/send_code/

**Описание:**  
Имитирует отправку 4-значного кода верификации на указанный телефонный номер.

**Метод:** `POST`

**Параметры:**  
- `phone_number` (обязательный): Телефонный номер, на который будет отправлен код.

**Ответы:**
- `200 OK`: Код успешно отправлен.
- `400 Bad Request`: Неверный запрос, если не указан номер телефона.

### POST /auth/check_code/

**Описание:**  
Проверяет код, отправленный на номер телефона. Если код правильный, генерируется код приглашения для нового пользователя, а также выдаются JWT токены для аутентификации.

**Метод:** `POST`

**Параметры:**  
- `phone_number` (обязательный): Телефонный номер, на который будет отправлен код.
- `verification_code` (обязательный): Верификационный код, отправленный на номер.

**Ответы:**
- `200 OK`: спешная верификация кода.
- `400 Bad Request`: Неверный код или номер телефона.
  
### POST /invite/

**Описание:**  
Позволяет пользователю ввести код приглашения от другого пользователя.

**Метод:** `POST`

**Параметры:**  
- `invited_code` (обязательный): Код приглашения.

**Ответы:**
- `200 OK`: Код приглашения успешно принят.
- `400 Bad Request`: Неверный или отсутствующий код приглашения или ошибка с аутентификацией.
- `401 Unauthorized`: Неавторизованный пользователь.
  
### GET /users/

**Описание:**  
Получение списка пользователей, которых пригласил авторизованный пользователь.

**Метод:** `GET`

**Ответы:**
- `200 OK`: Список пользователей, приглашенных текущим пользователем.
- `400 Bad Request`:  Ошибка с аутентификацией.
- `401 Unauthorized`: Неавторизованный пользователь.

  
## Пример использования API

**1. Получение кода верификации для номера телефона:**
Отправьте запрос на эндпоинт /auth/sendCode/ с номером телефона в теле запроса. В ответ вы получите код верификации.

**2. Проверка верификационного кода:**
После получения кода, отправьте запрос на эндпоинт /auth/code/ с номером телефона и кодом верификации. В ответ вы получите новый код приглашения и токены для аутентификации.

**3. Использование кода приглашения:**
Если вы хотите ввести код приглашения, отправьте запрос на эндпоинт /post/code/ с кодом приглашения. В ответ вы получите информацию о пользователе, который вас пригласил.

**4. Получение списка пользователей, которых пригласил авторизованный пользователь:**
Отправьте GET запрос на эндпоинт /users/. В ответ получите список пользователей, которых пригласил текущий авторизованный пользователь.

## Логирование

Все действия в API сопровождаются логированием:
- `Info`: Сообщения о успешных операциях, например, отправка кода, успешная верификация, генерация токенов.
- `Warning`: Предупреждения о возможных ошибках, например, истекший код верификации или неверный код приглашения.
- `Error`: Ошибки при выполнении операций, такие как отсутствие телефонного номера или недействительный токен.

Логи выводятся в консоль для отслеживания ошибок и событий в реальном времени.
