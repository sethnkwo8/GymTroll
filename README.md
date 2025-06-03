# GYMTROLL web application
#### Video Demo: https://youtu.be/D919CVIKqnA

####  Description: 
Gymtroll is a workout web application that helps users start their workout journey to get to their ideal or dream body goal and aid them in their fitness journey.
 
 It's built for anyone who wants to start working out whether at home or at the gym and doesn't know how to go about it or users who are already regular gym members looking to find an ideal split and exercises to add to their routine. 

 It takes input from users based on their goal, how many days they want to workout, their current weight, their desired weight and where they prefer to exercise either at home or at the gym, it then provides a personalised workout plan based on the criterias provided which helps the user reach their goal in a structured manner. Users can also view the workout library which contains links to videos for every exercise provide where they can get a step by step instruction on how to correctly perform these exercises to maximise results, users can also view the nutrition page which gives a breakdown of the importance of nutrition to fitness and also gives a macronutrient breakdown and provides a link to a calorie and macro calculator users can use to calculate the caloric intake needed to reach their goals. Users can also calculate the Body Mass Index(BMI) using the BMI calculator and after calculating it users can compare it with the BMI range table to see their classification. 
 
 I chose to build this web application as I am someone who likes to go to the gym and an application with these functions would've been really helpful in my journey when starting out and creating my routine.

---
##  Technologies Used

The main languages I used were:
- Python/Flask
- HTML/CSS/JavaScript
- SQLite
- Bootstrap
- bcrypt,smtplib, datetime, functools

---

##  Features
The key features of this project are:
- User registration and login: Where users can create an account and login to access the web application functions.
- Get your personalized plan: Where users choose their goal, split, current weight, desired weight and where the prefer to workout to get their personalized plan
- About Us page: Users can read a brief information about GYMTROLL
- Contact Us page: Users can write short messages to contact me.
- Workout Library: Users can get access to videos for each exercise
- Nutrition: Users can learn about nutrition and how it aids their journey.
- BMI calculator: Users can calculate their Body Mass Index
- Users can also cancel their plan and get a different one if their goal changes.
---

##  How to Run
```bash
# Clone the repository
git clone https://github.com/sethnkwo8/GymTroll

# Navigate into the project directory

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run
