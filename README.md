Я улучшил маленько докер, подготовил его к работе и в дев и в продакшене

Разворачивать надо с ветки logic
```bash
docker-compose up
```

Есть пара вопросов

— По сессии, которая от aiohttp при запросе создаётся (клиент)
<ul>
Сейчас создаётся новая каждый раз когда запрос прилетает
<li>
Создавать при запуске приложения сессию(on startap, on shutdown) или при каждом вызове функции. Непонятно стоит ли заморачиваться с одной сессией на все ручки. Подумал, что это может влиять если сервис на один домен ходит, тогда наверное наоборот лучше разные и под каждую свою проксю, но если разные, то, по идее можно сделать одну сессию и это ведь быстрее должно работать и всякие куки можно гонять. Короче не уверен, что об этом стоит париться, тем более я задачу не знаю, она тут особо никакая и не стояла) Но просто задумался об этом, когда писал
</li>
</ul>

— Тесты - тесты вообще корявые короче (сейчас вся логика по эндпоинтам, но достаточно коряво)
<ul>
<li>
тестировать функции отдельно клиентские и ручки апи отдельно
или сразу всю логику по эндпоинтам
</li>
</ul>

-- Новый пул вопросов
<ul>
<li>
Пытался с асинхронными запросами внутрь map от executor'а, но, по-видимому, так нельзя действовать
</li>
<li>
Есть ли разница где получать луп - при запросе, при объявлении сессии или при объявлении функции вообще
</li>
</ul>


-- Улучшения
<ul>
<li>
</li>
</ul>
