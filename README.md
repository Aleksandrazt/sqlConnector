# sqlConnector
Дипломная
Программа для реализации распределенных запросов к гетерогенным СУБД (mySQL, SQLite, PostgreSQL) с предварительной фильрацией на уровне базы данных для уменьшения времени передачи и требуемого места на главном узле,
последующим объединением и повторной фильтрацией перед выводом.
SQL_analyzer - анализирует гетерогенный запрос и разбивает его на запросы к каждой базе данных
SQL_connector - выполняяет подключение, отправляет запрос и возвращает DataFrame с данными
SQL_union - объединяет DataFrame, повторно проверяет условия и удаляет лишние столбцы, нужные для фильтрации
main - считывает и выводит данные, вызывает другие модули
