test_data = ["SELECT `db1.books.name`, `db1.authors.name`, `db2.books.book_col`, `db3.pick_up_points.name` "
             "FROM `db1.books` "
             "JOIN `db1.authors` ON `db1.authors.id`=`db1.books.author` JOIN `db2.books` "
             "ON  `db1.books.name`=`db2.books.book_name` JOIN `db3.point_book` "
             "ON `db3.point_book.book_id`=`db2.books.id` JOIN `db3.pick_up_points` "
             "ON `db3.point_book.point_id`=`db3.pick_up_points.id` WHERE `db2.books.book_col` < 50  "
             "and `db1.authors.name` = 'James Joyce'",
             "SELECT * FROM `db1.authors where `db1.authors.id` between 1 and 10 ORDER BY `db1.authors.name` ",
             "SELECT * FROM `db1.authors where `db1.authors.name` = 'James Joyce'",
             "SELECT * FROM db1.books JOIN `db2.books` ON `db1.books.name`=`db2.books.book_name`",
             "SELECT `db1.books.name`,`db2.books.book_col`  FROM db1.books JOIN `db2.books` ON  "
             "`db1.books.name`=`db2.books.book_name`",
             "SELECT `db1.books.name`, `db1.authors.name`, `db1.authors.country` FROM `db1.books` JOIN `db1.authors` "
             "ON `db1.authors.id`=`db1.books.author`",
             "SELECT `db1.books.name`, `db1.authors.name`, `db2.books.book_col` FROM `db1.books` JOIN `db1.authors` "
             "ON `db1.authors.id`=`db1.books.author` JOIN `db2.books` ON  `db1.books.name`=`db2.books.book_name`",
             "SELECT `db1.books.name`, `db1.authors.name`, `db2.books.book_col` FROM `db1.books` JOIN `db1.authors` "
             "ON `db1.authors.id`=`db1.books.author` JOIN `db2.books` ON  `db1.books.name`=`db2.books.book_name` "
             "WHERE `db2.books.book_col` BETWEEN 20 AND 100 OR `db2.books.book_col`>600",
             "SELECT `db1.books.name`, `db1.authors.name`, `db2.books.book_col`, `db3.pick_up_points.name` "
             "FROM `db1.books` "
             "JOIN `db1.authors` ON `db1.authors.id`=`db1.books.author` JOIN `db2.books` "
             "ON  `db1.books.name`=`db2.books.book_name` JOIN `db3.point_book` "
             "ON `db3.point_book.book_id`=`db2.books.id` JOIN `db3.pick_up_points` "
             "ON `db3.point_book.point_id`=`db3.pick_up_points.id` ORDER BY `db2.books.book_col` LIMIT 1"]

test_time = ["SELECT `db4.books.title`, `db4.books.authors`, `db5.rating.published_year` "
             "FROM `db4.books JOIN db5.rating` "
             "ON `db4.books.isbn13`=`db5.rating.isbn13` "
             "WHERE `db5.rating.average_rating` > 4 and `db4.books.num_pages` < 200"]

test_analyzer = [{'multiquery': "SELECT `db1.books.name`,`db2.books.book_col`  FROM db1.books JOIN `db2.books` ON  "
                                "`db1.books.name`=`db2.books.book_name`",
                  'respond': ({'db1': 'SELECT books.name FROM db1.books', 'db2': 'SELECT books.book_col, '
                                                                                 'books.book_name FROM db2.books'},
                              {'db1': ['db1.books.name'], 'db2': ['db2.books.book_col', 'db2.books.book_name']})},
                 {'multiquery': "SELECT * FROM `db1.authors where `db1.authors.name` = 'James Joyce'",
                  'respond': ({'db1': "SELECT authors.id, authors.name, authors.country FROM db1.authors WHERE "
                                      "db1.authors.name='James Joyce';"}, {'db1': ['db1.authors.id',
                                                                                   'db1.authors.name',
                                                                                   'db1.authors.country']})},
                 {'multiquery': "SELECT * FROM `db11.authors where `db1.authors.name` = 'James Joyce'",
                  'respond': 1}
                 ]

connector_test = {'request': "SELECT db1.authors.name, db1.authors.country "
                             "FROM db1.authors where db1.authors.country = 'France'",
                  'db': 'db1',
                  'head': ['db1.authors.name', 'db1.authors.country']}

union_test = ["SELECT `db1.books.name`, `db2.books.book_col` FROM `db1.books` JOIN `db2.books` "
              "ON `db1.books.name`=`db2.books.book_name` WHERE `db2.books.book_col`<20"]

test_eq_class = ["SELECT `db1.books.name` FROM `db1.books` ",
                 "SELECT `db1.books.name`, `db1.authors.country` FROM `db1.books` JOIN `db1.authors` "
                 "ON `db1.books.author`=`db1.authors.id`",
                 "SELECT `db1.books.name`, `db2.books.book_col` FROM `db1.books` JOIN `db2.books` "
                 "ON `db1.books.name`=`db2.books.book_name`",
                 "SELECT `db1.books.name`, `db1.authors.country`, `db2.books.book_col` "
                 "FROM `db1.books` JOIN `db1.authors` ON `db1.books.author`=`db1.authors.id` "
                 "JOIN `db2.books` ON `db1.books.name`=`db2.books.book_name`",
                 "SELECT `db1.books.name`, `db1.authors.country` FROM `db1.books` JOIN `db1.authors` "
                 "ON `db1.books.author`=`db1.authors.id` WHERE `db1.authors.country`='US'",
                 "SELECT `db1.books.name`, `db1.authors.country`, `db2.books.book_col` "
                 "FROM `db1.books` JOIN `db1.authors` ON `db1.books.author`=`db1.authors.id` "
                 "JOIN `db2.books` ON `db1.books.name`=`db2.books.book_name` WHERE `db1.authors.country`='US'",
                 "SELECT * "
                 "FROM `db1.books` JOIN `db1.authors` ON `db1.books.author`=`db1.authors.id` "
                 "JOIN `db2.books` ON `db1.books.name`=`db2.books.book_name`",
                 "SELECT `db1.books.name`, `db1.authors.country`, `db2.books.book_col` "
                 "FROM `db1.books` JOIN `db1.authors` ON `db1.books.author`=`db1.authors.id` "
                 "JOIN `db2.books` ON `db1.books.name`=`db2.books.book_name` WHERE `db1.authors.country`='US'"
                 "GROUP BY `db2.books.book_col`"
                 ]

test_error = ["SELECT db1.books.name FROM db1.books ",
              "SELECT `db1.books1.name` FROM `db1.books` ",
              "SELECT `db1.books.name` FROM `db11.books` ",
              "SELECT `db1.books.name` FROM `db1.books` WHERE `db1.book2s.id`=1"
              ]

huge_data_test = ['select `db7.weight.weight`, `db6.height.height` FROM `db7.weight` JOIN `db6.height` '
                  'ON `db7.weight.id`=`db6.height.id`',
                  'select `db7.weight.weight`, `db6.height.height` FROM `db7.weight` JOIN `db6.height` '
                  'ON `db7.weight.id`=`db6.height.id` WHERE `db7.weight.weight`<100',
                  'select * FROM `db7.weight`',
                  'select * FROM `db7.weight` WHERE `db7.weight.weight`<100'
                  ]
test_compatibility = ['SELECT `db1.books.name` FROM `db1.books` WHERE `db1.books.author` <6',
                      'SELECT `db8.books.book_name` FROM `db8.books` WHERE `db8.books.book_col` between 100 and 400;',
                      "SELECT `db9.authors.name` FROM `db9.authors` WHERE `db9.authors.country` ='US'",
                      "SELECT `db1.books.name`, `db9.authors.name`, `db8.books.book_col` FROM `db9.authors` "
                      "JOIN `db1.books ON `db1.books.author`=`db9.authors.id` "
                      "JOIN `db8.books ON `db1.books.name`=`db8.books.book_name` "
                      "WHERE `db9.authors.country` ='US'"]

