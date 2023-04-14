import SQL_analyzer
import SQL_Analyzer_Without_Prepocessing
import SQL_connector
import SQL_union
import data_test

ERRORS = {1: 'Incorrect FROM', 2: 'Incorrect SELECT', 3: 'Incorrect WHERE'}


def main(test_mode=1, in_file=1):
    if in_file:
        file = open("output.txt", "w")
        file.close()
    if test_mode:
        where_data = data_test.huge_data_test
    else:
        print("Enter your SQL query")
        where_data = [input()]
    for query in where_data:
        if in_file:
            with open('output.txt', 'a') as file:
                print(query, file=file)
                if '`' not in query:
                    print('False format', file=file)
                    return
        elif test_mode:
            print(query)
            if '`' not in query:
                print('False format')
                return
        respond = SQL_analyzer.sql_analyzer(query.replace('`', ''))
        if type(respond) is int:
            if in_file:
                with open('output.txt', 'a') as file:
                    print(ERRORS[respond], f' in query "{query}"', file=file)
            else:
                print(ERRORS[respond], f' in query "{query}"')
            return
        sql_queries, heads = respond
        datas = {}
        for db in sql_queries:
            datas[db] = SQL_connector.get_data_from_db(sql_queries[db], db, heads[db])
        result = SQL_union.unite_data(datas, query)
        if in_file:
            with open('output.txt', 'a') as file:
                print('result', file=file)
                print(result, file=file)
        else:
            print(result)


def without_preprocessing(test_mode=1, in_file=1):
    if in_file:
        file = open("output1.txt", "w")
        file.close()
    if test_mode:
        where_data = data_test.huge_data_test
    else:
        print("Enter your SQL query")
        where_data = [input()]
    for query in where_data:
        if in_file:
            with open('output1.txt', 'a') as file:
                print(query, file=file)
        elif test_mode:
            print(query)
        respond = SQL_Analyzer_Without_Prepocessing.sql_analyzer(query.replace('`', ''))
        if type(respond) is int:
            if in_file:
                with open('output1.txt', 'a') as file:
                    print(ERRORS[respond], f' in query "{query}"', file=file)
            else:
                print(ERRORS[respond], f' in query "{query}"')
            return
        sql_queries, heads = respond
        datas = {}
        for db in sql_queries:
            datas[db] = SQL_connector.get_data_from_db(sql_queries[db], db, heads[db])
        with open('output1.txt', 'a') as f:
            for db in datas:
                print(db, file=f)
                print(datas[db], file=f)
        result = SQL_union.unite_data(datas, query, 0)
        if in_file:
            with open('output1.txt', 'a') as file:
                print('result', file=file)
                print(result, file=file)
        else:
            print(result)


if __name__ == '__main__':
    main()
