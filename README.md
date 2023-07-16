
# Flashcards

This web application, built on Flask framework, is designed to allow users to create customized study cards. With the ability to create collections and associated study cards, the user can conveniently test their knowledge by accessing the cards without the content at first.


In addition to the core functionality, there is a secure registration and authentication system, and a password-changing option. 
<br>
The authentication mechanism has been implemented with rate-limiting, salted passwords, and testing to ensure robust security.


The application is backed by a relational database that utilizes SQLite. 
<br>
On the client side, AJAX has been implemented using the jQuery JavaScript library.
<br>

[YouTube Demo](https://www.youtube.com/watch?v=Ft2HY2mb088&t=30s)

![Alt text](documentation/screenshot.png "Entity Relationship Diagram")
<br><br>

## Getting Started
Clone the repository:
```bash
git clone https://github.com/hanit-com/cs50.git
```
Install the required packages:
```bash
pip install -r requirements.txt
```

## Running
```bash
python app.py
flask run
```

## Testing
```bash
pytest
```

## Database

Interact with the local DB:
```bash
sqlite3 project.db
```

![Alt text](documentation/entity_relationship_diagram.png "Entity Relationship Diagram")
<br><br>

## API
**All parameters are required**

#### Get the login page

```http
  GET /login
```
Returns rendered template of "login.html".


#### Log into the app

```http
  POST /login
```
| Parameter | Type     |
| :-------- | :------- |
| `username`| `string` |
| `password`| `string` |

Saves user ID in sesison and redirects to initial page.


#### Get registration page
```http
  GET /register
```
Returns rendered template of "register.html".


#### Register to the system
```http
  POST /register
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`| `string` | |
| `password`| `string` | |
| `confirmation`| `string` | User input for new password confirmation|

Redirects to initial page.


#### Get initial page
```http
  GET /
```
Returns rendered template of "index.html" if logged in or "login.html" if not.


#### Getting user collections
```http
  GET /collections
```
JSON response.
Internaly usses the session for user ID, no parameters needed.


#### Create new collection
```http
  POST /createCollection
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`| `string` | Name for the new collection.|

JSON response.


#### Delete a collection
```http
  DELETE /deleteCollection
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`| `string` | Collection ID.|

JSON response.


#### Get collection page
```http
  GET /collection
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`| `string` | Collection ID.|

Returns rendered template of "collection.html".


#### Get collection cards
```http
  GET /cards
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`| `string` | Collection ID.|

JSON response.


#### Delete a card
```http
  DELETE /deleteCard
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`| `string` | Card ID.|

JSON response.


#### Create a new card
```http
  POST /createCard
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`| `string` | |
| `content`| `string` | |
| `collection_id`| `string` | The collection the card is related to.|

JSON response.


#### Get password changing page
```http
  GET /changePassword
```

Returns rendered template of "change_password.html".


#### Change password

```http
  POST /changePassword
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `current_password`| `string` | |
| `new_password`| `string` | |
| `confirmation`| `string` | |

Redirects to initial page.


#### Log out of the app and redirect to the initial page
```http
  POST /logout
```
Clears the session and redirects to intial page.
