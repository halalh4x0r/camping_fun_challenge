## Camping Fun API
A Flask REST API for managing campers, activities, and signups for Access Camp. This API allows you to track campers, their activities, and signups that link campers to activities at specific times.

## Features
RESTful API with proper HTTP status codes

SQLAlchemy ORM with Flask-Migrate for database management

Data Validation for campers and signups

Cascade Deletes for maintaining data integrity

MVC Architecture pattern implementation

## API Endpoints
Method	Endpoint	Description	Status Codes
GET	/campers	List all campers	200
GET	/campers/<id>	Get camper details with signups	200, 404
POST	/campers	Create a new camper	201, 400
PATCH	/campers/<id>	Update camper information	202, 400, 404
GET	/activities	List all activities	200
DELETE	/activities/<id>	Delete an activity and its signups	204, 404
POST	/signups	Create a signup for camper & activity	201, 400
## Setup Instructions
Prerequisites
Python 3.8+

pip (Python package manager)

Installation
Clone the repository

bash
git clone <repository-url>
cd camping_fun_challenge
Create and activate virtual environment

bash
python3 -m venv env
source env/bin/activate  # Mac/Linux
# OR
.\env\Scripts\activate  # Windows
Install dependencies

bash
pip install -r requirements.txt
Set up the database

bash
python setup.py
Run the application

bash
python app.py
The API will be available at http://localhost:5555

## Database Models
# Camper
id (Integer, Primary Key)

name (String, Required)

age (Integer, Required, 8-18)

# Activity
id (Integer, Primary Key)

name (String, Required)

difficulty (Integer, Required)

# Signup
id (Integer, Primary Key)

time (Integer, Required, 0-23)

camper_id (Integer, Foreign Key)

activity_id (Integer, Foreign Key)

## API Usage Examples
Get All Campers
bash
curl http://localhost:5555/campers
Create a New Camper
bash
curl -X POST http://localhost:5555/campers \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 12}'
Get Camper Details
bash
curl http://localhost:5555/campers/1
Create a Signup
bash
curl -X POST http://localhost:5555/signups \
  -H "Content-Type: application/json" \
  -d '{"camper_id": 1, "activity_id": 1, "time": 14}'
Delete an Activity
bash
curl -X DELETE http://localhost:5555/activities/1
## Validation Rules
Camper Validations
Name: Required field

Age: Must be between 8 and 18 (inclusive)

Signup Validations
Time: Must be between 0 and 23 (hour of day)

Error Responses
Validation failures return:

json
{
  "errors": ["validation errors"]
}
With HTTP status code 400.