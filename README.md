# Secure File Sharing System

This is a backend application developed using Python and FastAPI for a secure file-sharing system.  
There are two types of users involved:
- Operations (Ops) User – Responsible for uploading specific file types.
- Client User – Can sign up, verify email, and securely download files.

---

## Features

- Login functionality for Ops User
- Upload functionality for `.pptx`, `.docx`, `.xlsx` files (Ops User only)
- Signup functionality for Client User with encrypted download URL generation
- Email verification for Client User (mocked)
- Secure file download with encrypted link (Client User only)
- List all uploaded files for a Client User

---

## Tech Stack

- Backend: Python, FastAPI
- Database: SQLite (via SQLAlchemy)
- Authentication: Password Hashing with PassLib, Secure token via Fernet encryption
- Environment Config: python-dotenv
- Testing: Postman (API collection provided)

---

1. Folder Structure
secure_file_sharing/
│

├── app/

│ ├── models/

│ ├── routes/

│ └── schemas.py

├── main.py

├── requirements.txt

├── .env (not included in the repository)

├── client_uploaded_files/

2. Install dependencies: pip install -r requirements.txt
3. Create a .env file in the root directory with the following content: FERNET_KEY=your_generated_key_here
4. Run the FastAPI server: uvicorn main:app --reload
5. API Endpoints 
Ops User:
Method	      Endpoint	          Description
POST	      /ops/login	          Login for operations user
POST	      /ops/upload	          Upload file (pptx, docx, xlsx only)

Client User:
Method	      Endpoint	                      Description
POST	        /client/signup	                Signup client and get encrypted URL
GET	          /client/list-files/{email}	    List uploaded files for a client
GET	          /client/download-file/{id}	    Download latest uploaded file securely

6.Postman Collection
All API endpoints have been tested and included in the Postman collection: secure_file_sharing.postman_collection.json (included in the repository).You can import this file into Postman and test each route with appropriate request bodies.

7.Dummy Credentials (For Testing)
Ops User
Email: ops@example.com
Password: ops123

8.Important Notes
-This project is created as part of a backend internship assignment at EZ Labs.
-The .env file should not be committed to any public repository.
-Email verification is simulated and does not send real emails.
-The encrypted download link is accessible only by the respective client.


Author:
Manjeet Bamel
Email: manjeet.bamal07@gmail.com
GitHub: M4NJ3ET
LinkedIn: [Manjeet Bamel](https://www.linkedin.com/in/manjeet-bamel-787695227/)

Acknowledgements:
-The project was developed with some external guidance to follow best practices and understand the required implementation.
-Help from ChatGPT was used mainly for understanding concepts, identifying bugs, and optimizing code where necessary.
-All logic and implementation were reviewed and written by me for learning and development purposes.
