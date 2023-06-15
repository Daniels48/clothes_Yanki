add_cls = {"add": "unview"}
del_cls = {"del": "unview"}
error = {"error": {**add_cls, "text": ""}}
not_val = {"value": ""}

data = {"1": {"title": {"text": 'Забыли пароль?'},
              "text": {
                  "text": "Введите свою почту и мы отправим вам код для сброса пароля и восстановления аккаунта:",
                  **del_cls,
                  "type": "11"},
              "ul": add_cls,
              "email": not_val,
              "pass": {**add_cls, **not_val},
              "button": {"value": "ПРОДОЛЖИТЬ"},
              **error,
              },
        "11": {
            "text": {"text": "Код из сообщения:", "add": "modals__none", "type": "12"},
            "email": {"placeholder": "Код*", **not_val},
            "pass": {**del_cls, "placeholder": "Новый пароль*", **not_val},
            "button": {"value": "УСТАНОВИТЬ ПАРОЛЬ"},
            **error,
        },
        "12": {
            "title": {"text": "Вы успешно сменили пароль!", "add": "modals__margin", "type": "0"},
            "email": {**add_cls, **not_val},
            "pass": {**add_cls, **not_val},
            "text": add_cls,
            "button": add_cls,
            **error,
        },
        "2": {
            "title": {"text": "Регистрация", "type": "21"},
            "ul": add_cls,
            "email": not_val,
            "pass": not_val,
            "button": {"value": "ПРОДОЛЖИТЬ"},
            **error,
        },
        "21": {
            "title": {"text": "Регистрация - шаг 2", "type": "22"},
            "text": {"text": "Мы отправили вам на почту код для подтверждения регистации. Введите его, пожалуйста",
                     **del_cls},
            "pass": {**add_cls, **not_val},
            "email": {"placeholder": "Код с e-mail*", **not_val},
            "button": {"value": "ЗАРЕГИСТРИРОВАТЬСЯ"},
            **error,
        },
        "22": {
            "title": {"text": "Регистрация - успешно!", "type": "0"},
            "text": {"text": "Вы успешно зарегестрировались! Приятных покупок!",
                     "add": "modals__margin"},
            "email": {**add_cls, **not_val},
            "pass": not_val,
            "button": add_cls,
            **error,
            "time": {"time": "true"}
        },
        "error0": {"error": {"text": "Неверный логин или пароль.", **del_cls}},
        "error1": {"error": {"text": "Пользователь с таким email не найден.", **del_cls}},
        "error11": {"error": {"text": "Неверный код.", **del_cls}},
        "error2": {"error": {"text": "Пользователь с таким Email уже существует.", **del_cls}},
        "register": {"username": 0, "password": 0},
        "recovery": {"username": 0, "password": 0},
        "0": "0",
        }
