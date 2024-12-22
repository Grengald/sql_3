import sqlite3
import os

class UniversityDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        if not os.path.exists(self.db_name):
            self._initialize_database()
        else:
            self._connect_to_database()

    def _initialize_database(self):
        self._connect_to_database()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time_start TEXT NOT NULL,
            time_end TEXT NOT NULL
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_courses (
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (id),
            FOREIGN KEY (course_id) REFERENCES Courses (id)
        );
        ''')

        
        self.cursor.execute('SELECT COUNT(*) FROM Courses;')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''INSERT INTO Courses (id, name, time_start, time_end) VALUES (1, 'python', '21.07.21', '21.08.21');''')
            self.cursor.execute('''INSERT INTO Courses (id, name, time_start, time_end) VALUES (2, 'java', '13.07.21', '16.08.21');''')

        self.cursor.execute('SELECT COUNT(*) FROM Students;')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''INSERT INTO Students (id, name, surname, age, city) VALUES (1, 'Max', 'Brooks', 24, 'Spb');''')
            self.cursor.execute('''INSERT INTO Students (id, name, surname, age, city) VALUES (2, 'John', 'Stones', 15, 'Spb');''')
            self.cursor.execute('''INSERT INTO Students (id, name, surname, age, city) VALUES (3, 'Andy', 'Wings', 45, 'Manhester');''')
            self.cursor.execute('''INSERT INTO Students (id, name, surname, age, city) VALUES (4, 'Kate', 'Brooks', 34, 'Spb');''')

        self.cursor.execute('SELECT COUNT(*) FROM Student_courses;')
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute('''INSERT INTO Student_courses (student_id, course_id) VALUES (1, 1);''')
            self.cursor.execute('''INSERT INTO Student_courses (student_id, course_id) VALUES (2, 1);''')
            self.cursor.execute('''INSERT INTO Student_courses (student_id, course_id) VALUES (3, 1);''')
            self.cursor.execute('''INSERT INTO Student_courses (student_id, course_id) VALUES (4, 2);''')

        self.connection.commit()

    def _connect_to_database(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.fetchall()

    def get_students_over_30(self):
        query = '''SELECT * FROM Students WHERE age > 30;'''
        return self.execute_query(query)

    def get_students_in_python(self):
        query = '''
        SELECT Students.* FROM Students
        JOIN Student_courses ON Students.id = Student_courses.student_id
        JOIN Courses ON Courses.id = Student_courses.course_id
        WHERE Courses.name = 'python';
        '''
        return self.execute_query(query)

    def get_students_in_python_from_spb(self):
        query = '''
        SELECT Students.* FROM Students
        JOIN Student_courses ON Students.id = Student_courses.student_id
        JOIN Courses ON Courses.id = Student_courses.course_id
        WHERE Courses.name = 'python' AND Students.city = 'Spb';
        '''
        return self.execute_query(query)

    def close_connection(self):
        if self.connection:
            self.connection.close()

п
if __name__ == "__main__":
    db = UniversityDatabase("university.db")

    print("Студенты старше 30 лет:", db.get_students_over_30())
    print("Студенты, проходящие курс по python:", db.get_students_in_python())
    print("Студенты, проходящие курс по python и из Spb:", db.get_students_in_python_from_spb())

    db.close_connection()
