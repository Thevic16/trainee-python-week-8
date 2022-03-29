#  Eighth Week Assignment.

# Logic Diagram of the project.
![Diagram](https://gitlab.com/t7501/fifth-week-assignment/-/blob/feature/django/models/img/Fifth%20Week%20Assignement%20UML.drawio.png)

# Instruction to run the app.

- You have to specify the environment variables (see .env-example).
- There are some details to consider when specifying those variables:
    - The environment variable "DEBUG_STATE" (True / False) defines if the
      Flask app runs in debugger mode or not.
    
- Run "docker-compose up" to start the app. 

# Heroku app credential (pre-created-accounts) for testing JWT.
- Account with administrator permission. <br />
Email: admin@filmrentalsystem.com <br />
Password: admin12345678 

- Account with employee permission. <br />
Email: employee@filmrentalsystem.com <br />
Password: employee12345678 

Also, If you wish you can create your accounts using the followings links.<br />

- Register your account. <br />
link: https://week8-film-rental-system.herokuapp.com/api/account/

Note: using the verb POST see Postman collection for more information. 

# Heroku URLs for generate the JWT token.
Note: This is using "Bearer" as the JWT prefix. (see Postman collection) 

link: https://week8-film-rental-system.herokuapp.com/api/authentication


# Heroku URl for API documentation. 
link: https://week8-film-rental-system.herokuapp.com/api/doc/

# Heroku URLs API apps (accounts, categories, films, seasons, chapters, persons, roles, films-persons-roles, clients and rents).
link: https://week8-film-rental-system.herokuapp.com/api/accounts/

link: https://week8-film-rental-system.herokuapp.com/api/categories/

link: https://week8-film-rental-system.herokuapp.com/api/films/

link: https://week8-film-rental-system.herokuapp.com/api/seasons/

link: https://week8-film-rental-system.herokuapp.com/api/chapters/

link: https://week8-film-rental-system.herokuapp.com/api/persons/

link: https://week8-film-rental-system.herokuapp.com/api/roles/

link: https://week8-film-rental-system.herokuapp.com/api/films-persons-roles/

link: https://week8-film-rental-system.herokuapp.com/api/clients/

link: https://week8-film-rental-system.herokuapp.com/api/rents/

# Note about Phone number format in clients App.
The app receive phone number of the following format: "XXX-XXXX-XXXX" 
where X = number

# Note about Date format.
Year-mouth-day example 2020-03-24

