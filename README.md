# Online Registration System + Voting System & API
This project consists of a website for the YCA students at the university. 
The website is divided into three main key areas that include:
(i). Online Registration Portal +  Membership card generator system
(ii).  Voting System
(iii). Admin Portal
(iv). API

///////////////----- DESCRIPTION ------////////////////////////////////////////////////////////////

 The website have got a portal where the students can create account, login and update their details that will be used to generate their membership card. The system can generte an official membership card which can be downloaded and printed by registered members only after approval by the system admin. 
 The system admin can access to all the members accounts through the admin portal. He/she can delete, deactivate or approve accounts.
 The system also have a voting sytem where members can elect their leaders via online. One will have to register first and be approved by the system admin before voting. The system also comprises of an api that exposes the members details to be consumed by other parties.

 <<---- Instructions on how to use this project -->>
1. Create a folder and clone the project in it 
2. Install a virtual environment in the folder using the following command
    ** pip install virtualenv env 
3. Then we create our virtual environment
    ** virtualenv env

4. Activate the virtual environment 
    ** env\scripts\activate
5. Install all the requirements below using pip install -r requirements.txt
    ** Django==4.2
    ** gunicorn==20.0.4
    ** Pillow==9.5.0
    ** charset-normalizer==3.1.0
    ** django-cors-headers==4.0.0
    ** djangorestframework==3.14.0
    ** requests==2.30.0
    ** sqlparse==0.4.3

6. Finally run "python manage.py runserver" command to start the project
    You can find the full working project at:
     # www.tumcathcom.com