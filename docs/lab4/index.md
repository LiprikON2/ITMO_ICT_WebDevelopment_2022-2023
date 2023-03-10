# Laboratory work 4
> Рейнгеверц В.А. - K33401

## Lab work part


### Desktop
Главная страница
![](https://i.imgur.com/PdgBMOr.png)

- Боковое меню с навигацией, авторизацией и сменой светлой/темной темы

Пошаговая регистрация
![](https://i.imgur.com/TrtGrrn.png)

- Client-side & server-side валидация на каждом шагу
- Динамически подгружаются варианты выбора для choice полей модели 
- Динамически подгружаются варианты выбора для foreign key полей модели 

Выбор библиотеки
![](https://i.imgur.com/ZluRXoj.png)

- У каждой библиотеки свои читательские залы

Авторизация
![](https://i.imgur.com/dXZmSVQ.png)

- По djoser токену, хранящемся в Local Storage/Session Storage

Уведомления
![](https://i.imgur.com/eTeD7Oe.png)

- Об ошибках, успешных действиях

Кнопка "выйти"
![](https://i.imgur.com/86ehkyw.png)

- Инвалидизирует djoser токен

Читательские залы библиотеки
![](https://i.imgur.com/PYSBVoE.png)

- Динамически подгружаются

Зарезервированные пользователем книги
![](https://i.imgur.com/Vw47MD0.png)


### Mobile & dark/light mode

![](https://i.imgur.com/3iUcDAr.png)

![](https://i.imgur.com/L135jtQ.png)


### Django backend + React frontend integration

![](https://i.imgur.com/xyXEBPv.png)

`index.html`
```html
{% load static %}
{% load env_utils %}
{% load django_vite %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0, maximum-scale=1.0"/>
        <title>Librarian</title>
        {% comment %} https://vitejs.dev/guide/backend-integration.html {% endcomment %}
        <script type="module">
            import RefreshRuntime from 'http://{% get_env "host" "localhost" %}:{% get_env "frontend_port" 3000 %}/@react-refresh'
            RefreshRuntime.injectIntoGlobalHook(window)
            window.$RefreshReg$ = () => {}
            window.$RefreshSig$ = () => (type) => type
            window.__vite_plugin_react_preamble_installed__ = true
        </script>
        {% comment %} https://github.com/MrBin99/django-vite#template-tags {% endcomment %}
        {% vite_hmr_client %}
        {% vite_asset 'src/core/index.jsx' %}
        <style type="text/css">
            #root {
                overflow: hidden;
            }
        </style>
    </head>
    <body>
        <div id="root"></div>
    </body>
</html>
```

`vite.config.js`
```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

const backendPort = process.env.backend_port ?? 8000;
const host = process.env.host ?? "localhost";

// https://vitejs.dev/config/
// https://github.com/MrBin99/django-vite-example/blob/master/vite.config.js
export default defineConfig({
    plugins: [react()],
    root: resolve("./static"),
    base: "/static/",
    server: {
        strictPort: true,
        port: 3000,
        open: false,
        watch: {
            usePolling: true,
            disableGlobbing: false,
        },
        origin: `http://${host}:${backendPort}`,
    },
    resolve: {
        extensions: [".js", ".jsx", ".json"],
        alias: {
            "~": resolve("./static/src"),
        },
    },
    build: {
        outDir: resolve("./static/dist"),
        assetsDir: "",
        manifest: true,
        emptyOutDir: true,
        target: "es2015",
        rollupOptions: {
            input: {
                main: resolve("./static/src/core/index.js"),
            },
            output: {
                chunkFileNames: undefined,
            },
        },
    },
    define: {
        backendPort: JSON.stringify(backendPort),
    },
});
```

`index.js`
```js
import "vite/modulepreload-polyfill";
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "~/core/App";

const queryClient = new QueryClient();

const root = createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <App queryClient={queryClient} />
            </BrowserRouter>
        </QueryClientProvider>
    </React.StrictMode>
);
```

#### Reference
- [Getting Started | Vite](https://vitejs.dev/guide/#index-html-and-project-root)
- [Backend Integration | Vite](https://vitejs.dev/guide/backend-integration.html) 
- [Django Vite](https://github.com/MrBin99/django-vite) 
- [Django Vite Example](https://github.com/MrBin99/django-vite-example)

### Running

Makes migrations, migrates, runs django backend server and react frontend server
```bash
bash run.sh
```

- Default backend port: 8000 (can be changed in `run.sh`)
- Default frontend port: 3000 (can be changed in `run.sh`)


Passes any command to the django's `manage.py`
```bash
bash run.sh <any django manage.py command>
```

E.g.
```bash
bash run.sh createsuperuser
```

Passes any command to the npm
```bash
bash run.sh npm <any npm command>
```

E.g.
```bash
bash run.sh npm install react
```

Passes any command to the pip
```bash
bash run.sh npm <any npm command>
```

E.g.
```bash
bash run.sh pip install pandas
```



### Screenshots

ER Diagram
![](https://i.imgur.com/X3vlFdG.png)

Backend urls
![](https://i.imgur.com/nEVRsl4.png)

### Требования к представлениям
Пользователь может:

- Зайти
- Найти книгу
- Выбрать книгу
- Получить книгу
- Сдать книгу

Nice-to-haves:

- Личный кабинет с книгами и фильтром по дате 
- Представление для библиотекаря



### Description
> Задание 2

Создать программную систему, предназначенную для работников библиотеки. Такая система должна обеспечивать хранение сведений об имеющихся в библиотеке книгах, о читателях библиотеки и читальных залах.

Для каждой книги в БД должны храниться следующие сведения: название книги, автор (ы), издательство, год издания, раздел, число экземпляров этой книги в каждом зале библиотеки, а также шифр книги и дата закрепления книги за читателем. Книги могут перерегистрироваться в другом зале.

Сведения о читателях библиотеки должны включать номер читательского билета, ФИО читателя, номер паспорта, дату рождения, адрес, номер телефона, образование, наличие ученой степени.

Читатели закрепляются за определенным залом, могут переписаться в другой зал и могут записываться и выписываться из библиотеки. 

Библиотека имеет несколько читальных залов, которые характеризуются номером, названием и вместимостью, то есть количеством людей, которые могут одновременно работать в зале.

Библиотека может получать новые книги и списывать старые. Шифр книги может измениться в результате переклассификации, а номер читательского билета в результате перерегистрации.


Библиотекарю могут потребоваться следующие сведения о текущем состоянии библиотеки:

- Какие книги закреплены за заданным читателем?
- Кто из читателей взял книгу более месяца тому назад?
- За кем из читателей закреплены книги, количество экземпляров которых в библиотеке не превышает 2?
- Сколько в библиотеке читателей младше 20 лет?
- Сколько читателей в процентном отношении имеют начальное образование, среднее, высшее, ученую степень?

Библиотекарь может выполнять следующие операции:

- Записать в библиотеку нового читателя.
- Исключить из списка читателей людей, записавшихся в библиотеку более года назад и не прошедших - перерегистрацию.
- Списать старую или потерянную книгу.
- Принять книгу в фонд библиотеки.

Необходимо предусмотреть возможность выдачи отчета о работе библиотеки в течение месяца. Отчет должен включать в себя следующую информацию: 

- Количество книг и читателей на каждый день в каждом из залов и в библиотеке в целом
- Количество читателей, записавшихся в библиотеку в каждый зал и в библиотеку за отчетный месяц.


### Python requirements

- django-phonenumber-field[phonenumberslite]
- djoser
- djangorestframework_simplejwt
- drf_yasg
- django-cors-headers
- django-vite
