import psycopg2
 
def initDB(db_config, sql_file):
    try:
        conn = psycopg2.connect(db_config)
        cursor = conn.cursor()
        
        with open(sql_file, 'r') as file:
            sql_script = file.read()
        
        cursor.execute(sql_script)
        conn.commit()
        print("SQL script executed successfully.")
    
    except Exception as e:
        print(f"Error executing SQL file: {e}")
    
    finally:
        cursor.close()
        conn.close()
 
if __name__ == "__main__":
    db_config = {
        "dbname": "nds",
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": 5432
    }
    sql_file = "db.sql"
    initDB(db_config, sql_file)