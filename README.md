# Full Stack Coffee Shop Project 
This project part Full Stack Web Developer Nanodegree from Udacity.

App's features:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## Backend
All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

### Installing Python3 and Dependencies

The backend uses [Python v3.10](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
All required packages are included in the requirements file. From the `backend` folder run `pip3 install -r requirements.txt`.

- Key Dependencies:
  - [Flask](https://flask.palletsprojects.com)
  - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)
  - [Flask-Testing](https://pythonhosted.org/Flask-Testing/)
  - [Flask-Expects-Json](https://pypi.org/project/flask-expects-json/)
  - [Requests](https://docs.python-requests.org/en/latest/)
  - [Jose](https://pypi.org/project/python-jose/)

### Database Setup
The backend based on SQLite DBMS. No action required. On the first app run the database will be created with some seed data, if it is not exists.


### Auth0 Account
The application uses [Auth0](https://auth0.com) for authentication and session management. If you want to use your own service then you need to update the related information in the `backend/src/auth/auth.py file`:
```shell
AUTH0_DOMAIN = 'fsnd-tota.us.auth0.com' 
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'
```

And in the frontend as well: `/frontend/src/environments/environments.ts`:
```js
auth0: {
  url: '', // the auth0 domain prefix
  audience: '', // the audience set for the auth0 app
  clientId: '', // the client id generated for the auth0 app
  callbackURL: '', // the base url of the running ionic application. 
}
```

### Running the Server
Start the backend application with the following commands from the `/backend/src` folder: 
 ```shell
export FLASK_APP=api
export FLASK_ENV=development
flask run
```

These commands put the application in development mode and directs the application to use the `api.py` file in  `backend/src` folder. If running locally on Windows, look for the commands in the [Flask documentation](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/).

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

## Frontend
### Installing Dependencies
Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.

Installing Ionic Cli
The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the Ionic Framework Docs.

Installing project dependencies
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

```shell
npm install
```

## Tests
You can use the following command to run all test cases from the `backend` folder:
```shell
python3 -m unittest -v
```
Also, you can test the application endpoint with Postman collection: `backend/udacity-fsnd-udaspicelatte.postman_collection_test_run.json`

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API reference
### Getting started
**Base URL:** At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000, which is set as a proxy in the frontend configuration.

**Authentication:** This version of the application requires authentication.

### Error handling
Errors are returned as JSON objects in the following format:
```json
{
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

- [400](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400): Bad Request
- [404](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404): Resource Not Found
- [405](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405): Method Not Allowed
- [409](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409): Conflict
- [422](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422): Not Processable

### Endpoints
#### GET `/drinks`
**Permission:** `None`
- Fetches all drinks from the database and returns them in an array

**Example response:**
```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "Water"
        }
    ]
}
```
#### GET `/drinks-detail`
**Permission:** `get:drinks-detail`
- Fetches all drinks from the database and returns them in an array with extended details

**Example response:**
```shell
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Water"
        },
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Blue Water"
        }
    ]
}
```
#### POST `/drinks`
**Permission:** `post:drinks`
- Inserts drink data based on the information provided

**Example request:**
```shell
{
    title: "Manager Coffee",
    recipe: [
        {
            name: "Milk",
            color: "white",
            parts: 1
        },
        {
            name: "Coffee",
            color: "brown",
            parts: 2
        }
    ]
}
```
**Example response:**
```shell
{
    "drinks": [
        {
            "id": 3,
            "recipe": [
                {
                    "color": "white",
                    "name": "Milk",
                    "parts": 1
                },
                {
                    "color": "brown",
                    "name": "Coffee",
                    "parts": 2
                }
            ],
            "title": "Manager Coffee"
        }
    ]
}
```

#### DELETE `/drinks/<id>`
**Permission:** `delete:drinks`
- Removes all drink information of the given drink <id>
**Example response:**
```shell
{
    "delete": 1
}
```
#### PATCH `/drinks/<id>`
**Permission:** `patch:drinks`
- Updates drink data and saves the changes into database

**Example body request:**
```shell
{
  "title": "Flat white"
}
```
**Example response:**
```shell
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Manager's Coffee"
        }
    ]
}
```