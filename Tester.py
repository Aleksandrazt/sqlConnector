import main
import time
import SQL_analyzer
import SQL_connector
import SQL_union
import data_test
import pandas as pd


def time_tester():
    start = time.time()
    for i in range(1000):
        main.main()
    end = time.time()
    print("Время исполнения 1000 тестов с предобработкой")
    print(end - start)
    start = time.time()
    for i in range(1000):
        main.without_preprocessing()
    end = time.time()
    print("Время исполнения 1000 тестов без предобработки")
    print(end - start)


def sql_analyzer_test():
    query = data_test.test_analyzer[0]['multiquery']
    print(query)
    respond = SQL_analyzer.sql_analyzer(query.replace('`', ''))
    print('Type of respond:', type(respond))
    print('Queries:', respond[0])
    print('Heads:', respond[1])
    assert respond == data_test.test_analyzer[0]['respond'], 'SQL_analyzer work incorrect'
    print('SQL_analyzer works correct')
    query = data_test.test_analyzer[1]['multiquery']
    print(query)
    respond = SQL_analyzer.sql_analyzer(query.replace('`', ''))
    print('Type of respond:', type(respond))
    print('Queries:', respond[0])
    print('Heads:', respond[1])
    assert respond == data_test.test_analyzer[1]['respond'], 'SQL_analyzer work incorrect'
    print(query)
    print('SQL_analyzer works correct')
    query = data_test.test_analyzer[2]['multiquery']
    respond = SQL_analyzer.sql_analyzer(query.replace('`', ''))
    print('Type of respond:', type(respond))
    print('Code:', respond)
    assert respond == data_test.test_analyzer[2]['respond'], 'SQL_analyzer work incorrect'
    print('SQL_analyzer works correct')


def sql_connector_test():
    data = SQL_connector.get_data_from_db(**data_test.connector_test)
    right_data = pd.DataFrame({'db1.authors.name': ['Victor Hugo', 'Albert Camus', 'Marcel Proust'],
                               'db1.authors.country': ['France', 'France', 'France']})
    print(type(data))
    print(data)
    assert data.equals(right_data), 'SQL_connector work incorrect'
    print('SQL_connector work correct')


def sql_union_test():
    query = data_test.union_test[0]
    sql_queries, heads = SQL_analyzer.sql_analyzer(query.replace('`', ''))
    datas = {}
    for db in sql_queries:
        datas[db] = SQL_connector.get_data_from_db(sql_queries[db], db, heads[db])
    right_data = pd.DataFrame({'db1.books.name': ['The Rum Diary', 'Finnegans Wake'],
                               'db2.books.book_col': [0, 10]})
    data = SQL_union.unite_data(datas, query)
    print(type(data))
    print(data)
    assert data.equals(right_data), 'SQL_union work incorrect'
    print('SQL_union work correct')


if __name__ == '__main__':
    sql_union_test()
