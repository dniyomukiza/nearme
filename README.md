## Project Overview

This Flask-based web application allows users to register, login, and make reservations. It includes features such as OTP (One-Time Password) verification, email notifications, and a contact form.

## Key Features

1. **User Authentication**
   - Registration with username and password validation
   - Login with OTP verification sent via email

2. **Reservation System**
   - Users can make reservations specifying date, time, and location
   - Automatic calculation of reservation duration and cost

3. **Email Notifications**
   - OTP sent for login verification
   - Reservation details sent to user and admin

4. **Contact Form**
   - Allows visitors to send messages to the admin

5. **Price Estimation**
   - Simple calculator on the home page for estimating reservation costs

## Main Components

### Routes

1. **Home** (`/`): Displays the main page with a price estimation tool
2. **Register** (`/register`): User registration page
3. **Login** (`/login`): User login page
4. **OTP Verification** (`/otp`): OTP entry page for login verification
5. **Reserve** (`/reserve`): Reservation form for logged-in users
6. **Contact** (`/contact`): Contact form for visitors
7. **About** (`/about`): Information page about the service

### Key Functions

- `send_email()`: Sends OTP via email for login verification
- `send_details()`: Sends reservation details to user and admin
- `otp_generate()`: Generates a random 5-digit OTP

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy (ORM)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF,HTML/CSS 
- **Email**: smtplib for sending emails via Gmail SMTP

## Security Features

- Password hashing (implementation not shown in the provided code)
- OTP verification for login
- Environment variables for sensitive information (email credentials)

## Setup and Configuration

To run this project:

1. Clone the repository to your local machine
2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables for email configuration:
   - CONF_EMAIL
   - CONF_CODE
   - SENDER_EMAIL
   - MY_EMAIL
4. Configure the database (ensure SQLAlchemy is properly set up)
5. Run the Flask application:
   ```
   flask run
   ```

Note: Ensure all necessary environment variables are properly set before running the application.

The `requirements.txt` file should contain all the necessary packages for the project, including Flask, Flask-Login, Flask-WTF, SQLAlchemy, and any other dependencies used in the application.

## Future Improvements

1. Implement rate limiting for OTP requests
2. Enhance reservation system with availability checking
3. Implement admin dashboard for managing reservations
4. Integrate Third-Part payment system