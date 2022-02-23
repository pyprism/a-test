# a-test

#### Create config and put appropriate values
```
cp backend/config.json backend/config.local.json
```

#### Run locally
```
docker-compose up
```

#### Run migration and create test user
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser 
```
#### Run test
```
docker-compose exec backend python manage.py test
```

After running docker compose frontend will be available at http://0.0.0.0:3000/


# Workflow for API
  - Go to `http://127.0.0.1:8000/v1/api/account/` and login, after login superuser can create other account.
  - Go to `http://0.0.0.0:8000/v1/api/company/` and create company, example : `{"name: "Test company"}`
  - Go to `http://0.0.0.0:8000/v1/api/employee/` and create multiple employee, example: `{ "name": "example 1", "employee_type": "cto", "company_name": "Test company"}`
  - Visit `http://0.0.0.0:8000/v1/api/employee/get_all_employee/?cto_id={cto pk}` to get desired result as mentioned in instruction
