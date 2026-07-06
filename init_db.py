import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def initialize_database():
    # Connect to MySQL Server (without specifying DB name first to create it)
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "")
    )
    cursor = conn.cursor()
    
    # 1. Create Database if it doesn't exist
    db_name = os.getenv("DB_NAME", "loan_approval_db")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database '{db_name}' verified/created.")
    
    # Switch to the new database
    cursor.execute(f"USE {db_name}")
    
    # 2. Create Table based on your Capstone input requirements
    create_table_query = """
    CREATE TABLE IF NOT EXISTS applicants (
        applicant_id VARCHAR(50) PRIMARY KEY,
        age INT,
        income DECIMAL(12, 2),
        employment_type VARCHAR(50),
        credit_score INT,
        loan_amount DECIMAL(12, 2),
        tenure INT,
        existing_liabilities DECIMAL(12, 2),
        location VARCHAR(100),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    print("Table 'applicants' verified/created.")
    
    # 3. Insert Sample Test Records
    sample_records = [
        ("APP-1001", 34, 95000.00, "Full-Time", 740, 25000.00, 36, 1200.00, "New York, USA"),
        ("APP-1002", 23, 32000.00, "Part-Time", 580, 10000.00, 12, 400.00, "Los Angeles, USA"),
        ("APP-1003", 45, 120000.00, "Self-Employed", 630, 80000.00, 60, 4500.00, "Chicago, USA"),
        ("APP-1004", 29, 0.00, "Unemployed", 510, 5000.00, 6, 200.00, "Miami, USA")
    ]
    
    insert_query = """
    INSERT INTO applicants 
    (applicant_id, age, income, employment_type, credit_score, loan_amount, tenure, existing_liabilities, location)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    credit_score=VALUES(credit_score), income=VALUES(income), loan_amount=VALUES(loan_amount);
    """
    
    cursor.executemany(insert_query, sample_records)
    conn.commit()
    print(f"Successfully seeded {cursor.rowcount} sample records into the database.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()