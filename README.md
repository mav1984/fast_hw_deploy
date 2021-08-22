# fast_hw_deploy

Скрипт предназначен для быстрого развертывания на локальном компьютере домашних работ для 3-6 спринтов. 
(Если непонятно, о чем это, значит вы случайно зашли не туда)

Скрипт берет из указанного в настройках каталога с загрузками последний созданный zip-файл, 
распаковывает в текущую директорию каталог `yatube`, копирует в новый каталог файл БД,
вставляет нужный тег в базовый шаблон для корректного отображения стилей.


## Подготовительные шаги:

1. Склонируйте этот репозиторий или же определите директорию, 
в которой вы будете проверять работы, разместите туда `fast_deploy.py` (далее - Рабочая директория)
NB. Не пишите в названии директории слово `yatube`.

2. Пропишите свои пользовательские настройки внутри файла `fast_deploy.py` (сразу после импортов)

3. Настройте виртуальное окружение с зависимостями для 6 спринта

4. Создайте в Рабочей директории "образцовый" файл БД `db.sqlite3` со всеми миграциями как для 6 спринта. 
В базе должны быть записи Льва Николаевича, также в ней нужно завести своего пользователя с простым цифровым паролем
(надо будет отключить штатный валидатор паролей джанго), добавить от имени этого пользователя несколько записей, создать группу, добавить к ней записи.


## Порядок использования:
Скачайте архив с работой студента, запустите скрипт `fast_deploy.py`.


## Возможные проблемы:
Если ругается на то, что не может найти load static tag, убедитесь, что в названии Рабочей директории нет слова `yatube`
Но иногда бывает, что студенты редактируют файл и удаляют этот тег. Тогда вручную.
