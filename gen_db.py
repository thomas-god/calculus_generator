import sqlite3

def init_db():
    """
    If no database exists, create it along with the table 
    for storing previously generated sets.
    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS test;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS test(
            alpha TINYINT,
            beta TINYINT,
            xi TINYINT,
            PRIMARY KEY (alpha, beta, xi)
        );
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO test
        VALUES 
            (1, 5, 1),
            (1, 5, 0);
    """)
    conn.commit()

    c.execute("""
        SELECT * FROM test
        WHERE alpha = 1 AND beta = 5 AND xi = 0;
    """)
    a = c.fetchall()
    print(len(a))

    conn.close()