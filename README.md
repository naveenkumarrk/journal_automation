# Journal Recommendation System

Welcome to the Journal Recommendation System! This system sends personalized journal papers to users based on their interests.

## Features

- User registration and interest configuration
- Weekly email updates with relevant journal papers
- Automatic mailing system
- User-friendly interface for managing interests

## Prerequisites

Before running the project, ensure you have the following installed:

- Node.js 
- npm 
- SQLite 
- Node.js installed
- API keys for Springer and IEEE APIs (update the `.env` file)
- Gmail account credentials (update the `.env` file)
- Gmail account app passwords for EMAIL_PASS

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/your-repo.git
  or you can download it in zip format.

2. Set up environment variables:
-Enter your sender's Mail_ID
-Enter your app password
-Then enter your Springer_API_key 
 for example

        EMAIL_USER = your-email@gmail.com
        EMAIL_PASS = your_app_password
        SPRINGER_API_KEY = springer-api-key(23782147123)


3.Install the dependencies:
After updating the env file install the dependencies by entering entering the given code in server.js file terminal

      npm install

After installing the dependencies successfully run the application by 

      npm start

 The application should now be running at http://localhost:3000.


4. User registration:
   In the application the users will enter their mail_id and thier interests
    
        npm start
        
   After registering the users detials will be saved in the database

   https://user-images.githubusercontent.com/94048894/250009083-05b22480-5dfa-4a44-b570-1099d9a3a199.png



4. Run the python script:
   
 After registering run the python in your code editor         
 After executing the application it will send mail to the user according to their interests.

## Usage
1.Open your web browser and navigate to http://localhost:3000.
2.Follow the on-screen instructions to register your interests.
3.You will receive weekly email updates with journal papers related to your interests.

## License
This project is licensed under the MIT License.
