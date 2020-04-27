# Invest Now App API

A Django REST framework application task.

## Description
```
"INVEST NOW" is a virtual trading tool that allows people to invest in the Organic Food
production companies. As the part of building the functionality of "INVEST NOW"
```

## Technologies
- Python
- Django
- MYSQL

## API Endpoints

**User Accounts**
- /api/accounts/ (User registration endpoint) - POST Operation
- /api/accounts/login/ (User login endpoint) - POST Operation
- /api/tokens/{auth-token}/ (User logout endpoint) - DELETE Operation

**Company information**

- /api/admin/company/ (Create Company endpoint) - POST Operation
- /api/admin/company_lists?name={name}&location={location} (Company Lists endpoint) - GET Operation
- /api/admin/company/{company-id}/ (Edit Company endpoint) - PUT Operation
- /api/admin/delete_company/{company-id}/ (Delete Company endpoint) - DELETE Operation

**Investment**

- /api/investments/ (Create Investment endpoint) - POST Operation
- /api/investment_lists (Investment Lists) - GET Operation
- /api/investments/{investment-id}/ (Edit Investment endpoint) - PUT Operation
- /api/delete_investments/{investment-id}/ (Delete Investment endpoint) - DELETE Operation

**Testcase Scenarios**
- Test to verify registration with invalid password.
- Test to verify registration with already exists username.
- Test to verify registration with valid datas.
- Tested API authentication endpoint validations.

### Important
```
In this application, the user will type in their username and password (credentials), 
and the server will generate a token based on those credentials. The server then sends 
this token out to the user. Now the user doesn't need to send in login credentials
with every request.
```


### Install
```
pip install -r requirements.txt
```
****
### Migrations
```
- python manage.py makemigrations
- python manage.py migrate
```

### Note
```
Except for user registation and login endpoint. 
Pass Authorization Token in HEADER. Otherwise your request will be failed.
```
