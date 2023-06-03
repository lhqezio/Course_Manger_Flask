# Course Manager App Readme
## This is a Course Manager App that allows users to manage their courses and its dependencies
### Features
1. User registration and login and avatar
2. Course creation, editing, and deletion
3. User profile management
4. Admin Dashboard (Edit other users, blocking etc...)
5. Working but unimplemented API
### Known Bugs (TBF if we have time)
1. Avatar hardly works after changing user's email address, will revert to default
2. Little bugs here and there interacting with Database
2. TBD...
## Deployment Steps
1. Set up venv with "python venv -m .venv"
2. Run the correct Script file (activate or activate.bat) in .venv/Scripts/
3. pip install -r requirements.txt to install all the required dependencies
4. "flask --app CourseMananger run" to deploy
##Add or Edit course, comptency, or element
(courses/elements/competencies)/edit-(course/element/competency)/<id> - edit
(courses/elements/competencies)/new-(course/element/competency) - add

