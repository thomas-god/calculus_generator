import sqlite3

def init_db():
    """
    If no database exists, create it along with the table 
    for storing previously generated sets.
    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS parenthesis;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS parenthesis(
            alpha TINYINT,
            beta TINYINT,
            xi TINYINT,
            PRIMARY KEY (alpha, beta, xi)
        );
    """)

    c.execute("DROP TABLE IF EXISTS exercices;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS exercices(
            parenthesis1_id INT,
            parenthesis2_id INT,
            FOREIGN KEY (parenthesis1_id) REFERENCES parenthesis(rowid),
            FOREIGN KEY (parenthesis2_id) REFERENCES parenthesis(rowid),
            PRIMARY KEY (parenthesis1_id, parenthesis2_id)
        );
    """)
    conn.close()

def populate_dummy_data():
    """
    Populate the db with dummy parenthesis and exercices data.
    """
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO parenthesis
        VALUES 
            (1, 5, 1),
            (1, 5, 0);
    """)

    c.execute("""
        INSERT INTO exercices
        VALUES 
            (1, 2),
            (1, 1),
            (2, 2);
    """)
    conn.commit()
    conn.close()

def insert_parenthesis(c, a, b, x):
    """
    Insert a parenthesis record (a, b, x) into the parenthesis table
    using the cursor object `c` and returns its rowid, even if the record
    already exists in table.
    """
    try:
        c.execute("INSERT INTO parenthesis VALUES (?, ?, ?);", (a, b , x))
    except sqlite3.IntegrityError as e:
        if e.args[0] == 'UNIQUE constraint failed: parenthesis.alpha, parenthesis.beta, parenthesis.xi':
            print(f"Parenthesis record ({a}, {b}, {x}) already exists, fetching id of existing row.")
            idx = c.execute(
                "SELECT rowid FROM parenthesis WHERE alpha = ? AND beta = ? AND xi = ?;",
                (a, b, x)
            ).fetchone()[0]
    else:
        print(f"Parenthesis record ({a}, {b}, {x}) successfully inserted.")
        idx = c.lastrowid
    return idx

if __name__ == '__main__':
    init_db()
    populate_dummy_data()

    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    a1, b1, x1 = 1, 5, 1
    idx_1 = insert_parenthesis(c, a1, b1, x1)
    
    a2, b2, x2 = 1, 2, 3
    idx_2 = insert_parenthesis(c, a2, b2, x2)

    try:
        c.execute("INSERT INTO exercices VALUES (?, ?)", (idx_1, idx_2))
    except sqlite3.IntegrityError:
        print("Trying to insert a record that already exists, rollback previous transactions.")
        conn.rollback()
    else:
        print("New record successfully into exercices table.")


    conn.close()