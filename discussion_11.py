import unittest
import sqlite3
import json
import os
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
    cur.execute("CREATE TABLE IF NOT EXISTS employees (employee_id INTEGER UNIQUE PRIMARY KEY, first_name TEXT, last_name TEXT, hire_date TEXT, job_id INTEGER, salary INTEGER)")
    conn.commit()
# ADD EMPLOYEE'S INFORMTION TO THE TABLE


def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    data = json.loads(file_data)
    for item in data:
        id = item['employee_id']
        f_name = item['first_name']
        l_name = item['last_name']
        date = item['hire_date']
        job = item['job_id']
        sal = item['salary']
        cur.execute(
            """ 
            INSERT OR IGNORE INTO employees (employee_id, first_name, last_name, job_id, hire_date, salary)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id, f_name, l_name, job, date, sal)
        )
    conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute(
            """ 
            SELECT employees.hire_date, jobs.job_title
            FROM jobs JOIN employees
            ON employees.job_id = jobs.job_id
            ORDER BY employees.hire_date ASC
            """
    )
    res = cur.fetchall()

    conn.commit()
    return res[0][1]

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute(
            """ 
            SELECT employees.first_name, employees.last_name, employees.salary
            FROM jobs JOIN employees
            ON employees.job_id = jobs.job_id
            ORDER BY employees.hire_date ASC
            """
    )

    


class TestDiscussion11(unittest.TestCase):
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

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

