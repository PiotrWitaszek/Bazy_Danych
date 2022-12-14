import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """create a database connection to the SQLite databes
    specified by db_file
    :param db_file: database file
    :return Connection object or none
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql, args=None):
    """Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :param args: a tuple of arguments
    :return:
    """
    try:
        c = conn.cursor()
        if args:
            c.execute(sql, args)
        else:
            c.execute(sql)
        return c
    except Error as e:
        print(e)


def add_scorers(conn, scorers):
    """
    Create a new scorers into highest_scorers table
    :param conn:
    :param scorers:
    return: project id
    """
    cur = conn.cursor()
    cur.executemany("INSERT INTO highest_scorers VALUES(?, ?, ?)", scorers)
    conn.commit()


def select_all(conn):
    """
    Query all rows in the table
    :param conn: the Conmnection object
    :return:
    """
    sql = """SELECT * FROM highest_scorers"""
    cur = execute_sql(conn, sql)
    rows = cur.fetchall()

    print(rows)


def select_where(conn, points):
    cur = execute_sql(conn, "SELECT * FROM highest_scorers WHERE points=?", (points,))
    rows = cur.fetchall()

    print(rows)


def update(conn, points, id):
    execute_sql(conn, "UPDATE highest_scorers SET points=? WHERE id=?", (points, id))
    conn.commit()


def delete_where(conn, id):
    execute_sql(conn, "DELETE FROM highest_scorers WHERE id=?", (id,))
    conn.commit()


def delete_all(conn):
    """
    Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    execute_sql(conn, f"DELETE FROM highest_scorers")
    conn.commit()
    print("Deleted")


if __name__ == "__main__":
    create_highest_scorers_sql = """
    -- highest_scorers table
    CREATE TABLE IF NOT EXISTS highest_scorers (
        id INTEGER PRIMARY KEY ASC,
        points number(2,0) NOT NULL,
        name varchar(20) DEFAULT ''
        );
        """

    db_file = "NBA.db"

    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_highest_scorers_sql)
        scorers = (
            (None, 100, "Wilt Chambarlain"),
            (None, 81, "Kobe Bryant"),
            (None, 78, "Wilt Chambarlain"),
            (None, 73, "David Thompson"),
            (None, 73, "Wilt Chambarlain"),
            (None, 73, "Wilt Chambarlain"),
            (None, 72, "Wilt Chambarlain"),
            (None, 71, "David Robinson"),
            (None, 71, "Elgin Baylor"),
        )
        add_scorers(conn, scorers)
        select_all(conn)
        print("======")
        delete_where(conn, 1)
        select_all(conn)
        print("======")
        update(conn, 85, 3)
        select_all(conn)
        print("======")
        select_where(conn, 73)
        print("======")
        delete_all(conn)
        select_all(conn)
