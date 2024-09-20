import sqlite3
import pandas as pd

def import_task_data():
    with open('../static/Sample_Task.xlsx', 'rb') as f:
        data = pd.read_excel(f)

    conn = sqlite3.connect('task_db.sqlite')
    cursor = conn.cursor()

    # Create a table for tasks
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT,
        complexity TEXT,
        task_type TEXT,
        maker TEXT
    )''')

    for index, row in data.iterrows():
        task_name = row['Task']
        complexity = row['Complexity']
        task_type = row['Task Type']
        maker = row['Maker']
        cursor.execute("INSERT INTO tasks (task_name, complexity, task_type, maker) VALUES (?, ?, ?, ?)", (task_name,complexity,task_type,maker))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_task_data()