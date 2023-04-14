import known_databases_conf
from moz_sql_parser import parse


OPERATIONS = {'eq', 'mul', 'div', 'mod', 'binary_and', 'binary_or', 'gte', 'lte', 'lt', 'gt', 'neq', 'between', 'in',
              'nin', 'is', 'like', 'nlike'}
meta_join = {}


def sql_analyzer(query: str):
    """
    Make dict with sql queries for each db and dict with needed columns for each db
    :param query: multi query as string
    :return: dict with sql queries for each db and dict with needed columns for each db
    """
    sql_tree = parse(query)
    respond = analyze_from_part(sql_tree['from'], {})
    if respond:
        from_parts = respond
    else:
        return 1
    respond = analyze_select_part(sql_tree['select'], from_parts, {})
    if respond:
        select_parts = respond
    else:
        return 2
    if 'where' in sql_tree:
        respond = analyze_where_part(sql_tree['where'], from_parts, {})
        if respond:
            where_parts = respond
        else:
            return 3
    else:
        where_parts = {}
    extend_sql(select_parts, sql_tree['from'], where_parts)
    heads = make_head(select_parts)
    sql_queries = make_queries(select_parts, from_parts, where_parts)
    return sql_queries, heads


def analyze_from_part(from_part, from_parts: dict, mode=1):
    """
    Get from part of multi query. Work recursively
    :param mode: call it for normal query(1) or extend query(0)
    :param from_part: if it's str,split, check and get info, if it's list call itself in iteration, if it's dict
    there's join, get meta and call itself
    :param from_parts: dict of db with their from parts
    :return: 0 if there's error or dict of db with their from parts
    """
    if type(from_part) is str:
        try:
            db, table = from_part.split('.')
        except ValueError:
            return 0
        if not check_existence(db, table):
            return 0
        if db not in from_parts:
            from_parts[db] = [f'{db}.{table}']
        else:
            from_parts[db].append(f'{db}.{table}')
    elif type(from_part) is dict:
        meta = analyze_join(from_part)
        if meta and mode:
            db, on_part = meta
            from_parts[db].append(on_part)
        else:
            if mode == 1:
                if 'join' in from_part:
                    from_parts = analyze_from_part(from_part['join'], from_parts, mode)
                elif 'left join' in from_part:
                    from_parts = analyze_from_part(from_part['left join'], from_parts, mode)
                elif 'right join' in from_part:
                    from_parts = analyze_from_part(from_part['right join'], from_parts, mode)
            elif mode == 2:
                return from_part
            else:
                return from_part['on']
    elif type(from_part) is list:
        join_parts = []
        for part in from_part:
            from_parts = analyze_from_part(part, from_parts, mode)
            if not mode:
                join_parts.append(from_parts)
        if not mode:
            return join_parts
    else:
        return 0
    return from_parts


def analyze_join(join_on_part: dict):
    """
    Check if join in one db or meta join
    :param join_on_part:
    :return: 1 if it's in one db and 0 if it's different db
    """
    on_part = join_on_part['on']
    operation = list(on_part.keys())[0]
    if on_part[operation][0].split('.')[0] == on_part[operation][1].split('.')[0]:
        db = on_part[operation][0].split('.')[0]
        on_part = make_token(operation, 1, *on_part[operation])
        if 'join' in join_on_part:
            res = f' join {join_on_part["join"]} on {on_part}'
        elif 'left join' in join_on_part:
            res = f' left join {join_on_part["left join"]} on {on_part}'
        elif 'right join' in join_on_part:
            res = f' right join {join_on_part["right join"]} on {on_part}'
        else:
            res = 0
        return db, res
    make_meta_join(join_on_part)
    return 0


def make_meta_join(join_on_part):
    if 'join' in join_on_part:
        join_type = 'inner'
        right_db = join_on_part['join'].split('.')[0]
    elif 'left join' in join_on_part:
        join_type = 'left'
        right_db = join_on_part['left join'].split('.')[0]
    elif 'right join' in join_on_part:
        join_type = 'right'
        right_db = join_on_part['right join'].split('.')[0]
    else:
        right_db = ''
        join_type = ''
    on_part = join_on_part['on']
    operation = list(on_part.keys())[0]
    db = on_part[operation][0].split('.')[0]
    if right_db == db:
        left_part = on_part[operation][1]
        left_db = on_part[operation][1].split('.')[0]
        right_part = on_part[operation][0]
    else:
        left_part = on_part[operation][0]
        left_db = db
        right_part = on_part[operation][1]
    meta_join[f'{right_db}'] = {'left_db': left_db, 'right_db': right_db, 'join_type': join_type,
                                'left_part': left_part,
                                'right_part': right_part}
    return


def analyze_select_part(select_part, from_parts: dict, select_parts: dict):
    """
    Get select part of multi query. Work recursively
    :param select_part: if it's str,split, check and get info, if it's list call itself in iteration, if it's dict
    call itself from 'value'
    :param from_parts: dict of db with their from parts
    :param select_parts: dict of db with their select parts
    :return: 0 if there's error or dict of db with their select parts
    """
    if type(select_part) is str:
        if select_part == '*':
            select_parts = make_select_star(from_parts, select_parts)
            return select_parts
        try:
            db, table, col = select_part.split('.')
        except ValueError:
            return 0
        if not check_existence(db, table, col, from_parts):
            return 0
        if db not in select_parts:
            select_parts[db] = [f'{table}.{col}']
        else:
            select_parts[db].append(f'{table}.{col}')
    elif type(select_part) is dict:
        select_parts = analyze_select_part(select_part['value'], from_parts, select_parts)
    elif type(select_part) is list:
        for part in select_part:
            select_parts = analyze_select_part(part, from_parts, select_parts)
    else:
        return 0
    return select_parts


def make_select_star(from_parts: dict, select_parts: dict):
    for db in from_parts:
        from_part = ''.join(from_parts[db])
        for table in known_databases_conf.DB_STRUCTURE[db]:
            if f'{db}.{table}' in from_part:
                if db not in select_parts:
                    select_parts[db] = []
                for column in known_databases_conf.DB_STRUCTURE[db][table]:
                    if f'{table}.{column}' not in select_parts[db]:
                        select_parts[db].append(f'{table}.{column}')
    return select_parts


def extend_sql(select_parts: dict, from_parts, where_parts: dict):
    if type(from_parts) is list:
        on_part = analyze_from_part(from_parts, {}, 0)
        for part in on_part:
            operation = list(part.keys())[0]
            if operation not in OPERATIONS:
                continue
            part = make_token(operation, 0, *part[operation])
            part = part.split()
            for elem in part:
                db, table, col = elem.split('.')
                if db in select_parts:
                    t_and_c = f'{table}.{col}'
                    if t_and_c not in select_parts[db]:
                        select_parts[db].append(t_and_c)
    if where_parts:
        for db in where_parts:
            if db in select_parts:
                for elem in where_parts[db]:
                    needed = elem[0]
                    needed = find_needed_part(needed)
                    for s in needed:
                        try:
                            _, table, col = s.split('.')
                        except ValueError:
                            continue
                        t_and_c = f'{table}.{col}'
                        if t_and_c not in select_parts[db]:
                            select_parts[db].append(t_and_c)


def find_needed_part(s: str):
    s = s.replace('=', ' ')
    s = s.replace('>', ' ')
    s = s.replace('!=', ' ')
    s = s.replace('<', ' ')
    s = s.replace('<=', ' ')
    s = s.replace('>=', ' ')
    return s.split()


def analyze_where_part(where_part, from_parts: dict, where_parts: dict, meta_operation=''):
    """
        Get where part of multi query. Work recursively
        :param meta_operation:
        :param where_part: if there are dict as values call itself if there's elements turn it to clause
        :param from_parts: dict of db with their from parts
        :param where_parts: dict of db with their where parts
        :return: 0 if there's error or dict of db with their where parts
        """
    if type(where_part) is dict:
        operations = where_part.keys()
        for operation in operations:
            for elem in where_part[operation]:
                if type(elem) is dict:
                    where_parts = analyze_where_part(elem, from_parts, where_parts, operation)
                else:
                    one_db = []
                    if type(elem) is str:
                        try:
                            db, table, col = elem.split('.')
                        except ValueError:
                            continue
                        if not check_existence(db, table, col, from_parts):
                            return 0
                        if db not in one_db:
                            one_db.append(db)
                    if len(one_db) == 1:
                        sql_token = make_token(operation, 1, *where_part[operation])
                        if one_db[0] not in where_parts:
                            where_parts[one_db[0]] = [(sql_token, meta_operation)]
                        else:
                            where_parts[one_db[0]].append((sql_token, meta_operation))

    else:
        return 0
    return where_parts


def make_queries(select_parts: dict, from_parts: dict, where_parts: dict):
    sql_queries = {}
    for db in from_parts:
        select_part = 'SELECT ' + ', '.join(select_parts[db])
        if len(from_parts[db]) == 1:
            from_part = ' FROM ' + from_parts[db][0]
        else:
            from_part = ' FROM ' + from_parts[db][0] + ' '.join(from_parts[db][1:])
        sql_queries[db] = select_part + from_part
        if db in where_parts:
            if len(where_parts[db]) == 1:
                where_part = ' WHERE ' + where_parts[db][0][0]
            else:
                or_group = []
                and_group = []
                for part in where_parts[db]:
                    if part[1] == 'or':
                        or_group.append(part[0])
                    else:
                        and_group.append(part[0])
                where_part = ' WHERE ' + ' or '.join(or_group) + ' and '.join(and_group)
            sql_queries[db] += where_part + ';'
    return sql_queries


def make_token(operation: str, mode: int, *elem):
    """
    Make string with needed operation and elements
    :param mode: if 1 - normal, if  0 only spaces
    :param operation: name of operation
    :param elem: list of elements
    :return:  string with needed operation
    """
    elem = list(elem)
    for i in range(len(elem)):
        if type(elem[i]) is dict:
            elem[i] = f"'{elem[i]['literal']}'"
    if mode == 0:
        return f'{elem[0]} {elem[1]}'
    if operation == 'eq':
        return f'{elem[0]}={elem[1]}'
    if operation == 'mul':
        return f'{elem[0]}*{elem[1]}'
    if operation == 'div':
        return f'{elem[0]}/{elem[1]}'
    if operation == 'mod':
        return f'{elem[0]}%{elem[1]}'
    if operation == 'binary_and':
        return f'{elem[0]}&{elem[1]}'
    if operation == 'binary_or':
        return f'{elem[0]}|{elem[1]}'
    if operation == 'gte':
        return f'{elem[0]}>={elem[1]}'
    if operation == 'lte':
        return f'{elem[0]}<={elem[1]}'
    if operation == 'lt':
        return f'{elem[0]}<{elem[1]}'
    if operation == 'gt':
        return f'{elem[0]}>{elem[1]}'
    if operation == 'neq':
        return f'{elem[0]}!={elem[1]}'
    if operation == 'between':
        return f'{elem[0]} between {elem[1]} and {elem[2]}'
    if operation == 'in':
        return f'{elem[0]} IN ({",".join(elem[1:])})'
    if operation == 'nin':
        return f'{elem[0]} NOT IN ({",".join(elem[1:])})'
    if operation == 'is':
        return f'{elem[0]} IS {elem[1]}'
    if operation == 'like':
        return f'{elem[0]} LIKE {elem[1]}'
    if operation == 'nlike':
        return f'{elem[0]} NOT LIKE {elem[1]}'
    return ''


def check_existence(db: str, table: str, col='', place=known_databases_conf.DB_STRUCTURE):
    """
    Check if database, table and column exists in our structure
    :param place: where we check default db structure
    :param db: database name as str
    :param table: table name as str
    :param col: column name as str, can be missed
    :return: 0 if there is an error or 1 if all exists
    """
    if db not in place:
        print(f'Unknown database "{db}"')
        return 0
    if table not in known_databases_conf.DB_STRUCTURE[db]:
        print(f'Unknown table "{table}"')
        return 0
    if col and col not in known_databases_conf.DB_STRUCTURE[db][table]:
        if col == '*':
            return 1
        print(f'Unknown column "{col}"')
        return 0
    return 1


def make_head(select_parts: dict):
    """
    Make list of needed columns from select
    :param select_parts: select parts with db
    :return: list of columns from select
    """
    columns = {}
    for db in select_parts:
        for elem in select_parts[db]:
            table, col = elem.split('.')
            if db in columns:
                columns[db].append(f'{db}.{table}.{col}')
            else:
                columns[db] = [f'{db}.{table}.{col}']
    return columns
