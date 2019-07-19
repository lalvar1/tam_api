import sqlite3
import json
import os


DATABASE = "C:\\Users\\lalvar1\\Documents\\codes\\tam_api"

def create_connection2():
    """ create a database connection to a database that resides
        in the memory
    """
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    #finally:
    #    conn.close()

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        return sqlite3.connect(db_file + '\\reporter.db')
    except sqlite3.Error as e:
        print(e)

    #finally:
    #    conn.close()

def create_database(DATABASE):
    sql_create_jobs_table = "CREATE TABLE IF NOT EXISTS Reports_Table (Author text PRIMARY KEY,\
        Commiter text NOT NULL,\
        Comment text NOT NULL,\
        Report_counter integer NOT NULL,\
        Quote text NULL \
        );"

    # create a my_database connection
    create_folder(DATABASE)
    conn = create_connection(DATABASE)
    if conn is not None:
        create_table(conn, sql_create_jobs_table)
    else:
        print("Error! cannot create the my_database connection.")
    return conn

def create_folder(folder_name):
    """Receives a folder_name. If that folder doesn't exist, it is created."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        cur.close()
        conn.commit()
    except sqlite3.Error as err:
        print(err)


def get_lynx(DATABASE):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    str_db = "SELECT * " \
             "FROM 'Reports_Table' "
    #return cur.execute(str_db, (Author, Quote)).fetchone()[0]
    return cur.execute(str_db)

def update_lynx(DATABASE):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    if conn:
        sql = "UPDATE 'Reports_Table' " \
              "SET Author = ?"
    cur.execute(sql)
    cur.close()
    conn.commit()

def insert_job(DATABASE):
    conn = create_connection(DATABASE)
    #sql = 'INSERT INTO Reports_Table(Author,Quote)'
    sql = 'INSERT INTO Reports_Table(Author, Quote, Commiter, Report_counter, Comment) VALUES(?,?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, ('lalvar','go to the stadium', 'asd', 'asd3', 'asd2'))
    cur.close()
    conn.commit()


    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)


if __name__ == '__main__':
    #insert_job(DATABASE)
    #update_lynx(DATABASE)
    print(get_lynx(DATABASE))
    #create_database(DATABASE)
