# Full Stack Coffee Shop Project 
Features:

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

### Running the Server
Start the backend application with the following commands from the `/backend/src` folder: 
 ```shell
export FLASK_APP=api
export FLASK_ENV=development
flask run
```
These commands put the application in development mode and directs the application to use the `api.py` file in  `backend/src` folder. If running locally on Windows, look for the commands in the [Flask documentation](https://flask.palletsprojects.com/en/1.0.x/tutorial/factory/).

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

## Tests
You can use the following command to run all test cases from the `backend` folder:
```shell
python3 -m unittest -v
```

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
`Permission:` None
- Fetches all drinks
- test
- test

- **Example response:**
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
- **Example response:**
#### POST `/drinks`

#### DELETE `/drinks/<id>`

#### PATCH `/drinks/<id>`