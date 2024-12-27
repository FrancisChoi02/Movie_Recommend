import pandas as pd
import sqlite3

#Task_Name,Complexity,Task_type,Maker,Maker_Lock

def import_task_data():
    try:
        with open('./static/Task.csv', 'r') as f:
            data = pd.read_csv(f)

        conn = sqlite3.connect('./da/task_db.sqlite')
        cursor = conn.cursor()

        # Create a table for tasks
        cursor.execute('''CREATE TABLE IF NOT EXISTS task_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            complexity TEXT,
            task_type TEXT,
            maker TEXT,
            maker_lock TEXT
        )''')

        for index, row in data.iterrows():
            task_name = row['Task_Name']
            complexity = row['Complexity']
            task_type = row['Task_type']
            maker = row['Maker']
            maker_lock = row['Maker_Lock']
            cursor.execute("INSERT INTO task_data (task_name, complexity, task_type, maker,maker_lock) VALUES (?, ?, ?, ?,?)", (task_name,complexity,task_type,maker,maker_lock))

        conn.commit()
        return "Data imported successfully"
    except sqlite3.Error as e:
        return f"An error occurred with the database: {e}"
    except FileNotFoundError:
        return "The Excel file was not found."
    except pd.errors.EmptyDataError:
        return "The Excel file is empty."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Maker,Module,Status
def import_permission_data():
    try:
        with open('./static/Maker.csv', 'rb') as f:
            data = pd.read_csv(f)

        conn = sqlite3.connect('./da/task_db.sqlite')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS permission (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maker TEXT,
            module TEXT,
            status TEXT
        )''')

        for index, row in data.iterrows():
            maker = row['Maker']
            module = row['Module']
            status = row['Status']
            cursor.execute("INSERT INTO permission (maker, module, status) VALUES (?, ?, ?)", (maker, module, status))

        conn.commit()
        return "Data imported successfully"
    except sqlite3.Error as e:
        return f"An error occurred with the database: {e}"
    except FileNotFoundError:
        return "The Excel file was not found."
    except pd.errors.EmptyDataError:
        return "The Excel file is empty."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
   
if __name__ == "__main__":
    # result1 = import_task_data()
    # print(result1)

    result2 = import_permission_data()
    print(result2)

    
    