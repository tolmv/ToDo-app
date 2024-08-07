# API Documentation

## Endpoints

### /openapi.json
* Methods: GET, HEAD
* Summary: openapi

### /docs
* Methods: GET, HEAD
* Summary: swagger_ui_html

### /docs/oauth2-redirect
* Methods: GET, HEAD
* Summary: swagger_ui_redirect

### /redoc
* Methods: GET, HEAD
* Summary: redoc_html

### /register
* Methods: POST
* Summary: register

### /login
* Methods: POST
* Summary: login

### /todos
* Methods: POST
* Summary: create_todo

### /todos/{todo_id}
* Methods: GET
* Summary: read_todo

### /todos/{todo_id}
* Methods: PUT
* Summary: update_todo

### /todos/{todo_id}
* Methods: DELETE
* Summary: delete_todo

### /todos/{todo_id}/permissions
* Methods: POST
* Summary: set_todo_permissions
