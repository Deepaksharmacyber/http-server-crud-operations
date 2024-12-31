import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql123deepak",
  database = 'student_data_django',
)

mycursor = mydb.cursor()

mycursor.execute("""
CREATE TABLE IF NOT EXISTS customers_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullName VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phoneNumber VARCHAR(20),
    dateOfBirth DATE,
    address TEXT,
    profilePicture LONGBLOB,
    gender VARCHAR(10),
    interests TEXT,
    country VARCHAR(50),
    expectedSalary FLOAT
)
""")
