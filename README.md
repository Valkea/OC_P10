# SoftDesk

This project aims to provide a project manager API.

Using the various endpoints the users will be able to manage projects along with their contributors, issues and comments.

## Installation

In order to use this project locally, you need to follow the steps below:

### First, 
let's duplicate the project github repository

```bash
>>> git clone https://github.com/Valkea/OC_P10.git
>>> cd OC_P10
```

### Secondly,
let's create a virtual environment and install the required Python libraries

(Linux or Mac)
```bash
>>> python3 -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

(Windows):
```bash
>>> py -m venv venv
>>> .\venv\Scripts\activate
>>> py -m pip install -r requirements.txt
```

## Running the project

Once installed, the only required command is the following one

```bash
>>> python manage.py runserver
```

## Using the project

### as a user of the API

visit *http://127.0.0.1:8000/login/* and use the one of the demo credentials below:

*demo-login :* demo_user

*demo-password :* demopass

(or create your own user account: *http://127.0.0.1:8000/signup/*)

#### then read the API documentation

The API documentation introduce the available endpoints with many examples and the expected HTTP status code.
*https://documenter.getpostman.com/view/13202435/TWDWJcvC*

#### and test using the Postman of directly by browsing the API.

The easiest way to test the endpoints once the local server is running is by using them in Postman.

However, you can also browse the API directly in your browser as long as you provide a valid JWT token in the header (except for signup & login).
This can be done in many ways, such as using the 'ModHeader' browser plugin (wildly available). In this case, once installed, create an "Authorization" key and set the value as "JWT token" (where token is the access token returned when loggin-in). Then the API can be visited just like a simple website (as long as the token is valid and the user has right to use the endpoint).

### as an admin of the API

visit *http://127.0.0.1:8000/zadmin* and use the demo credentials to access the admin content:

*demo-login :* supadmin

*demo-password :* demopass

**this account need to be removed / changed before going into production !**

Once in the admin, you will be able to add, edit or remove 'users', 'projects', 'issues', 'collaborators' and 'comments'.

"PROJECT MANAGER" block
Even if all elements of the projects are available in this menu, the real main entry point is the "Projects" list, because when editing a project, we can also see and edit the associated issues, collaborators and comments.

However the "Issues", "Collaborators" and "Comments" are still available in the menu just in case the API admin prefers to access them that way. Finally, the comments are in 'read-only' mode, because admin shouldn't be able to edit user's comments (and I wanted to test an admin section with read-only...).

"USERS" block
In the Users section you can indeed manage the user's informations but you can also see their comments, assigned issues, and created issues or projects.
These informations are read-only from the users' profiles (but they can be edited from the projects entries).


## Documentation

The applications views are documented using the Django admindoc format.

However the admindoc module is not activated at the moment.


## PEP8

The project was developped using 'vim-Flake8' and 'black' modules to enforce the PEP8 rules.


## License
[MIT](https://choosealicense.com/licenses/mit/)
