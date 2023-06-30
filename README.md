# Journal Recommendation System

Welcome to the Journal Recommendation System! This system sends personalized journal papers to users based on their interests.
Here is a video to demonstrate how to run this project

[<img src="![Black White Video Centric YouTube Icon](https://github.com/naveenrk7/journal_automation/assets/94048894/8d0dd57d-9fed-4896-84a8-5b82703f598b)
" width="50%">](https://youtu.be/gYiiRj4i-j4 "Journal_ai")

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

## 1. Clone the repository:

         git clone https://github.com/your-username/your-repo.git   

or you can download it in zip format.

## 2. Set up environment variables:
-Enter your sender's Mail_ID
-Enter your app password
-Then enter your Springer_API_key 
 for example

        EMAIL_USER = your-email@gmail.com
        EMAIL_PASS = your_app_password
        SPRINGER_API_KEY = springer-api-key(23782147123)


## 3.Install the dependencies:
After updating the env file install the dependencies by entering entering the given code in server.js file terminal

      npm install

After installing the dependencies successfully run the application by 

      npm start

The application should now be running at http://localhost:3000.

![Screenshot (301)](https://github.com/naveenrk7/journal_automation/assets/94048894/89aad617-1731-4c5f-98b4-166781f0cf51)




## 4. User registration:
In the application the users will enter their mail_id and thier interests
        
After registering the users detials will be saved in the database

![Screenshot (299)](https://github.com/naveenrk7/journal_automation/assets/94048894/fd51454e-d168-4f9e-ab7b-8d085c11cf61)


## 5. Run the python script:

After registering run the python in your code editor         
After executing the application it will send mail to the user according to their interests.

![Screenshot (300)](https://github.com/naveenrk7/journal_automation/assets/94048894/29084605-846a-4c32-9b58-73bbe4e5dcb9)

 

## Usage
1.Open your web browser and navigate to http://localhost:3000.
2.Follow the on-screen instructions to register your interests.
3.You will receive weekly email updates with journal papers related to your interests.

## License
This project is licensed under the MIT License.
