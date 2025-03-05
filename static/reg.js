// Скрипт для регистрации пользователя
//
// Максимально возможно проверяет введённые данные,
// затем отправляет запрос на backend.

async function handleFormSubmit(event) {
    // Предотвращаем обычную отправку формы
    event.preventDefault();

    // Выведем лог
    console.log("Пытаюсь регнуть пользователя.");

    // Получаем обекты логина и паролей
    const login = document.getElementById('login');
    const password_1 = document.getElementById('password_1');
    const password_2 = document.getElementById('password_2');

    // Мини-валидация

    // Сразу установим пустые значения классов для обектов
    login.className = "";
    password_1.className = "";
    password_2.className = "";

    // Если не указан логин
    if ( !login.value ) {
        // Подсвечиваем окошко логина красным
        login.className = "error";

        // Выводим alert
        alert("Необходимо указать логин.");
    }
    else {
        // Если не указан password_1
        if ( !password_1.value ) {
            // Подсвечиваем окошки красным
            password_1.className = "error";

            // Выводим alert
            alert('Необходимо указать пароль в поле "Пароль".');
        }
        else {
            // Если не указан password_2
            if ( !password_2.value ) {
                // Подсвечиваем окошки красным
                password_2.className = "error";

                // Выводим alert
                alert('Необходимо указать пароль в поле "Повторите пароль".');
            }
            else {
                // Если пароли не совпадают
                if ( password_1.value != password_2.value ) {
                    // Подсвечиваем окошки красным
                    password_1.className = "error";
                    password_2.className = "error";

                    // Выводим alert
                    alert("Пароли должны совпадать.");
                }
                else {
                    // Валидация пройдена успешно

                    // Отправляем запрос на backend
                    const request = await fetch(
                        "/api/reg",
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                "login": login.value,
                                "password": password_1.value,
                            })
                        }
                    );

                    // Дисериализуем json
                    const r = await request.json()

                    // Успешный ли ответ
                    if ( !r.ok ) {
                        // Если логин уже занят
                        if ( r.message == "Этот логин занят, используйте другой." ) {
                            // Красим окошечко в красный
                            login.className = "error";
                        }

                        // Выводим сообщение об ошибке
                        alert(r.message);

                        // Выводим лог об ошибке
                        console.log("Ошибка во время регистрации:", r.message);
                    }
                    else {
                        // Выводим лог в консоль
                        console.log("Регистрация прошла успешно.");

                        // Красим рамочки полей в зелёный
                        login.className = "ok";
                        password_1.className = "ok";
                        password_2.className = "ok";

                        // Редиректим на главную
                        document.location.href = "/";
                    }
                }
            }
        }
    }
}

// Создаём объект формы
const applicant_form = document.getElementById('reg_form');

// Если обект формы не пуст
if ( applicant_form ) {
    // Подключаем "прослушку действий"
    applicant_form.addEventListener('submit', handleFormSubmit);
}
