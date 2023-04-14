from pandasql import sqldf
import SQL_analyzer, SQL_Analyzer_Without_Prepocessing
import pandas as pd


def unite_data(datas: dict, query: str, processing=1):
    if processing:
        analyzer = SQL_analyzer
    else:
        analyzer = SQL_Analyzer_Without_Prepocessing
    pd.set_option('display.max_columns', 6)
    pd.options.display.expand_frame_repr = False
    if len(datas) > 1:
        base_db = list(set(datas.keys()).difference(set(analyzer.meta_join.keys())))[0]
        res = datas[base_db]
        for db in analyzer.meta_join:
            res = res.merge(datas[db], left_on=analyzer.meta_join[db]['left_part'],
                            right_on=analyzer.meta_join[db]['right_part'],
                            how=analyzer.meta_join[db]['join_type'])
    else:
        db = list(datas.keys())[0]
        res = datas[db]
    analyzer.meta_join = {}
    query = make_new_query(query)
    query = f'''{query}'''
    res = sqldf(query)
    return res


def make_new_query(query):
    from_index = query.lower().find("from")
    where_index = query.lower().find("where")
    if where_index > 0:
        query = query[:from_index] + "FROM res " + query[where_index:]
    else:
        query = query[:from_index] + "FROM res "
    return query
