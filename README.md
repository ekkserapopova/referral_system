# API документация для риферальной системы

Данный API предназначен для реализации риферальной системы, включающей верификацию номеров телефонов, генерацию кодов для приглашений, создание и управление пользователями, а также аутентификацию через JWT токены.

## Оглавление

1. [Описание эндпоинтов]
    - [POST /auth/send_code/]
    - [POST /auth/check_code/]
    - [POST /invite/]
    - [GET /users/]
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
- `400 Bad Request`: Неверный или отсутствующий код приглашения.
- `401 Unauthorized`: Ошибка с аутентификацией.
  
### GET /users/

**Описание:**  
Получение списка пользователей, которых пригласил авторизованный пользователь.

**Метод:** `GET`

**Ответы:**
- `200 OK`: Список пользователей, приглашенных текущим пользователем.
- `400 Bad Request`:  Ошибка с аутентификацией.

  
