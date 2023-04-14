ALL_POSSIBLE_CONFIGS = {'db1': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db1', 'raise_on_warnings': True},
                        'db2': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db2', 'raise_on_warnings': True},
                        'db3': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db3', 'raise_on_warnings': True},
                        'db4': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db4', 'raise_on_warnings': True},
                        'db5': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db5', 'raise_on_warnings': True},
                        'db6': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db6', 'raise_on_warnings': True},
                        'db7': {'user': 'root', 'password': '100', 'host': 'localhost',
                                'database': 'db7', 'raise_on_warnings': True},
                        'db8': {'database': 'db8.db'}
    ,
                        'db9': {'user': 'postgres', 'password': '100', 'host': 'localhost',
                                'dbname': 'db9', 'port': '5432'}
                        }

DB_TYPES = {'db1': 'mysql', 'db2': 'mysql', 'db3': 'mysql', 'db4': 'mysql', 'db5': 'mysql',
            'db6': 'mysql', 'db7': 'mysql', 'db8': 'sqlite', 'db9': 'postgres'}
DB_STRUCTURE = {'db1': {'authors': ['id', 'name', 'country'],
                        'books': ['id', 'name', 'author']},
                'db2': {'books': ['id', 'book_name', 'book_col']},
                'db3': {'pick_up_points': ['id', 'name'],
                        'point_book': ['id', 'book_id', 'point_id']},
                'db4': {'books': ['isbn13', 'title', 'subtitle', 'authors', 'categories', 'num_pages']},
                'db5': {'rating': ['isbn13', 'title', 'published_year', 'average_rating']},
                'db6': {'height': ['id', 'height']},
                'db7': {'weight': ['id', 'weight']},
                'db8': {'books': ['id', 'book_name', 'book_col']},
                'db9': {'authors': ['id', 'name', 'country']}
                }
