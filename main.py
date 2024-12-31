import http.server
import socketserver
import urllib.parse
from database import *

# Fetch all records from the database
def fetch_all_customers():
    query = "SELECT id ,fullName, email, password ,phoneNumber,dateOfBirth,address,profilePicture,gender,interests,country,expectedSalary FROM customers_data"
    mycursor.execute(query)
    return mycursor.fetchall()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":  # Default route for index.html
            # Fetch data from the database
            data = fetch_all_customers()
            print(f' the data is {data}')
            # Dynamically generate the content for index.html
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Customer Records</title>
            </head>
            <body>
                <a href="user_input.html">click to create record</a>
                <h1>Customer Records</h1>
                <table border="1">
                    <tr>
                        <th>ID</th>
                        <th>Full Name</th>
                        <th>Email</th>
                        <th>Password</th>
                        <th>phoneNumber</th>
                        <th>dateOfBirth</th>
                        <th>address</th>
                        <th>profilePicture</th>
                        <th>gender</th>
                        <th>interests</th>
                        <th>country</th>
                        <th>expectedSalary</th>
                        <th>Actions</th>
                    </tr>
            """
            for row in data:
                id ,full_name, email, password , phoneNumber,dateOfBirth,address,profilePicture,gender,interests,country,expectedSalary= row
                html_content += f"""
            <tr>
                <td>{id}</td>
                <td>{full_name}</td>
                <td>{email}</td>
                <td>{password}</td>
                <td>{phoneNumber}</td>
                <td>{dateOfBirth}</td>
                <td>{address}</td>
                <td>{profilePicture}</td>
                <td>{gender}</td>
                <td>{interests}</td>
                <td>{country}</td>
                <td>{expectedSalary}</td>
                <td>
                    <button onclick="window.location.href='/edit?id={id}'">edit</button>
                    <button onclick="window.location.href='/delete?id={id}'">Delete</button>
                </td>
            </tr>
            """
            html_content += """
                </table>
                <br>
                <button onclick="window.location.href='/create'">Create New Record</button>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        elif self.path == "/create":  # Serve the form page
            form_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Create New Record</title>
            </head>
            <body>
                <h1>Create New Record</h1>
                <form method="POST" action="/">
                    <div>
            <label for="fullName">Full Name:</label>
            <input type="text" id="fullName" name="fullName" required>
        </div>
        <div>
            <label for="email">Email Address:</label>
            <input type="email" id="email" name="email">
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" >
        </div>
        <div>
            <label for="phoneNumber">Phone Number:</label>
            <input type="tel" id="phoneNumber" name="phoneNumber" >
        </div>
        <div>
            <label for="dateOfBirth">Date of Birth:</label>
            <input type="date" id="dateOfBirth" name="dateOfBirth">
        </div>
        <div>
            <label for="address">Address:</label>
            <textarea id="address" name="address" rows="4"></textarea>
        </div>
        <div>
            <label for="profilePicture">Profile Picture:</label>
            <input type="file" id="profilePicture" name="profilePicture">
        </div>
        <div>
            <label>Gender:</label>
            <input type="radio" id="male" name="gender" value="Male"> Male
            <input type="radio" id="female" name="gender" value="Female"> Female
            <input type="radio" id="other" name="gender" value="Other"> Other
        </div>
        <div>
            <label>Interests:</label><br>
            <input type="checkbox" name="interests" value="Technology"> Technology<br>
            <input type="checkbox" name="interests" value="Sports"> Sports<br>
            <input type="checkbox" name="interests" value="Music"> Music<br>
            <input type="checkbox" name="interests" value="Travel"> Travel<br>
            <input type="checkbox" name="interests" value="Reading"> Reading<br>
        </div>
        <div>
            <label for="country">Country:</label>
            <select id="country" name="country">
                <option value="">Select Country</option>
                <option value="India">India</option>
                <option value="USA">USA</option>
            </select>
        </div>
        <div>
            <label for="expectedSalary">Expected Salary:</label>
            <input type="number" id="expectedSalary" name="expectedSalary">
        </div>
            <button type="submit">Submit</button>
                </form>
                <button onclick="window.location.href='/'">Back to Records</button>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(form_html.encode('utf-8'))
         
        elif self.path.startswith("/edit"):
            # Extract customer ID from query string
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            customer_id = params.get('id', [None])[0]

            if customer_id:
                # Fetch customer record from the database
                query = f"SELECT * FROM customers_data WHERE id = {customer_id}"
                mycursor.execute(query)
                customer = mycursor.fetchone()
                print(f'the customer data is {customer}')

                if customer:
                    # Pre-fill the form with data from the database
                    id, full_name, email, password, phone_number, date_of_birth, address, profile_picture, gender, interests, country, expected_salary = customer
                    profile_picture = profile_picture.decode('utf-8')  # Convert binary to string
                    print(f'the profile_picture is {profile_picture}')
                    form_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Edit Record</title>
                    </head>
                    <body>
                        <h1>Edit Customer Record</h1>
                        <form method="POST" action="/update?id={id}">
                            <div>
                                <label for="fullName">Full Name:</label>
                                <input type="text" id="fullName" name="fullName" value="{full_name}" required>
                            </div>
                            <div>
                                <label for="email">Email Address:</label>
                                <input type="email" id="email" name="email" value="{email}">
                            </div>
                            <div>
                                <label for="password">Password:</label>
                                <input type="password" id="password" name="password" value="{password}">
                            </div>
                            <div>
                                <label for="phoneNumber">Phone Number:</label>
                                <input type="tel" id="phoneNumber" name="phoneNumber" value="{phone_number}">
                            </div>
                            <div>
                                <label for="dateOfBirth">Date of Birth:</label>
                                <input type="date" id="dateOfBirth" name="dateOfBirth" value="{date_of_birth}">
                            </div>
                            <div>
                                <label for="address">Address:</label>
                                <textarea id="address" name="address" rows="4">{address}</textarea>
                            </div>
                            
                            <div>
                                <label>Gender:</label>
                                <input type="radio" id="male" name="gender" value="Male" {'checked' if gender == 'Male' else ''}> Male
                                <input type="radio" id="female" name="gender" value="Female" {'checked' if gender == 'Female' else ''}> Female
                                <input type="radio" id="other" name="gender" value="Other" {'checked' if gender == 'Other' else ''}> Other
                            </div>
                            <div>
                                <label>Interests:</label><br>
                                <input type="checkbox" name="interests" value="Technology" {'checked' if 'Technology' in interests else ''}> Technology<br>
                                <input type="checkbox" name="interests" value="Sports" {'checked' if 'Sports' in interests else ''}> Sports<br>
                                <input type="checkbox" name="interests" value="Music" {'checked' if 'Music' in interests else ''}> Music<br>
                                <input type="checkbox" name="interests" value="Travel" {'checked' if 'Travel' in interests else ''}> Travel<br>
                                <input type="checkbox" name="interests" value="Reading" {'checked' if 'Reading' in interests else ''}> Reading<br>
                            </div>
                            <div>
                                <label for="country">Country:</label>
                                <select id="country" name="country">
                                    <option value="India" {'selected' if country == 'India' else ''}>India</option>
                                    <option value="USA" {'selected' if country == 'USA' else ''}>USA</option>
                                </select>
                            </div>
                            <div>
                                <label for="expectedSalary">Expected Salary:</label>
                                <input type="number" id="expectedSalary" name="expectedSalary" value="{expected_salary}">
                            </div>
                            <button type="submit">Update Record</button>
                        </form>
                        <br>
                        <button onclick="window.location.href='/'">Back to Records</button>
                    </body>
                    </html>
                    """
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(form_html.encode('utf-8'))
        
        elif self.path.startswith("/delete"):
            # Extract customer ID from query string
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            customer_id = params.get('id', [None])[0]

            if customer_id:
                # Delete the customer record from the database
                delete_query = f"DELETE FROM customers_data WHERE id = {customer_id}"
                mycursor.execute(delete_query)
                mydb.commit()

                # Redirect to the index page after deleting
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()

        else:  # Default behavior for other URLs
            super().do_GET()

    def do_POST(self):
        if self.path == "/create":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            # Extract form fields
            full_name = parsed_data.get('fullName', [None])[0]
            email = parsed_data.get('email', [None])[0]
            password = parsed_data.get('password', [None])[0]
            phone_number = parsed_data.get('phoneNumber', [None])[0]
            date_of_birth = parsed_data.get('dateOfBirth', [None])[0]
            address = parsed_data.get('address', [None])[0]
            gender = parsed_data.get('gender', [None])[0]
            country = parsed_data.get('country', [None])[0]
            expected_salary = parsed_data.get('expectedSalary', [None])[0]

            # Handle checkboxes (e.g., Interests)
            interests = parsed_data.get('interests', [])
            interests_str = ", ".join(interests)  # Convert list to string

            # Handle file upload (Profile Picture)
            # Assuming the file upload is handled separately
            profile_picture = parsed_data.get('profilePicture', [None])[0]  # This is just a placeholder

            # Insert into database
            insert_query = """
                INSERT INTO customers_data 
                (fullName, email, password, phoneNumber, dateOfBirth, address, gender, country, expectedSalary, interests, profilePicture) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            mycursor.execute(insert_query, (
             full_name, email, password, phone_number, date_of_birth, address,
               gender, country, expected_salary, interests_str, profile_picture
            ))
            mydb.commit()

            # Redirect back to index.html
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        elif self.path.startswith("/update"):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            customer_id = self.path.split('=')[1]  # Extract the ID from the URL
            
            # Extract form fields from the POST data
            full_name = parsed_data.get('fullName', [None])[0]
            email = parsed_data.get('email', [None])[0]
            password = parsed_data.get('password', [None])[0]
            phone_number = parsed_data.get('phoneNumber', [None])[0]
            date_of_birth = parsed_data.get('dateOfBirth', [None])[0]
            address = parsed_data.get('address', [None])[0]
            gender = parsed_data.get('gender', [None])[0]
            country = parsed_data.get('country', [None])[0]
            expected_salary = parsed_data.get('expectedSalary', [None])[0]

            interests = parsed_data.get('interests', [])
            interests_str = ", ".join(interests)

            # Prepare SQL UPDATE query
            update_query = """
                UPDATE customers_data 
                SET fullName = %s, email = %s, password = %s, phoneNumber = %s, dateOfBirth = %s, 
                    address = %s, gender = %s, country = %s, expectedSalary = %s, interests = %s
                WHERE id = %s
            """
            mycursor.execute(update_query, (full_name, email, password, phone_number, date_of_birth, 
                                           address, gender, country, expected_salary, interests_str, customer_id))
            mydb.commit()

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

# Define the port
PORT = 8000

# Create an HTTP server with the custom handler
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()


