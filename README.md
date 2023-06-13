# Journal Recommendation System

Welcome to the Journal Recommendation System! This system sends personalized journal papers to users based on their interests.

## Features

- User registration and interest configuration
- Weekly email updates with relevant journal papers
- Automatic mailing system
- User-friendly interface for managing interests

## Prerequisites

Before running the project, ensure you have the following installed:

- Node.js (version X.X.X)
- npm (version X.X.X)
- SQLite (version X.X.X)
- Node.js installed
- API keys for Springer and IEEE APIs (update the `.env` file)
- Gmail account credentials (update the `.env` file)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/your-repo.git

2.Install the dependencies:

        cd your-repo
        npm install
        
3. Set up environment variables:
- Create a .env file in the project root directory.
- Add the following variables to the .env file and replace the values with your own:
 
        EMAIL_USER=your-email@gmail.com
        EMAIL_PASS=your-email-password
        SPRINGER_API_KEY=your-springer-api-key
        IEEE_API_KEY=your-ieee-api-key

4. Start the application:
   
        npm start
        
The application should now be running at http://localhost:3000.

## Usage
1.Open your web browser and navigate to http://localhost:3000.
2.Follow the on-screen instructions to register your interests.
3.You will receive weekly email updates with journal papers related to your interests.

##License
This project is licensed under the MIT License.
