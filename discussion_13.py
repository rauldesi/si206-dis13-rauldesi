import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):

    cur.execute("DROP TABLE IF EXISTS employees")
    cur.execute("CREATE TABLE employees (" +
                "employee_id INTEGER PRIMARY KEY, " +
                "first_name TEXT, " +
                "last_name TEXT, " +
                "job_id INTEGER, " +
                "hire_date TEXT, " +
                "salary NUMERIC)")

    conn.commit()

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    
    emp_dict = json.loads(file_data)

    for emp in emp_dict:    
        cur.execute("INSERT INTO employees " +
                    "(employee_id, first_name, last_name, job_id, hire_date, salary)" +
                    "VAlUES (?,?,?,?,?,?)",
                    (emp['employee_id'], emp['first_name'], emp['last_name'], emp['job_id'], emp['hire_date'], emp['salary'])
                    )
    conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    row = cur.execute("SELECT e.hire_date, j.job_title FROM employees e " +
                       "JOIN jobs j " +
                       "ON e.job_id = j.job_id " +
                       "ORDER BY e.hire_date").fetchone()
    return row[1]

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    rows = cur.execute("SELECT e.first_name, e.last_name FROM employees e " +
                       "JOIN jobs j on e.job_id = j.job_id " +
                       "WHERE e.salary < j.min_salary " +
                       "OR e.salary > j.max_salary").fetchall()
    return rows

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    rows = cur.execute("SELECT j.job_title, e.salary " +
                       "FROM employees e " +
                       "JOIN jobs j " + 
                       "ON e.job_id = j.job_id").fetchall()
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])
    plt.scatter(x, y)

    jobs = cur.execute("SELECT job_title, min_salary, max_salary " +
                       "FROM jobs").fetchall()
    x1 = []
    y1 = []
    for job in jobs:
        x1.append(job[0])
        y1.append(job[1])
        x1.append(job[0])
        y1.append(job[2])
    plt.scatter(x1, y1, color='red', marker='x')

    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)
    
    visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

