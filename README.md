
# Transport Monitor

Backend by Django, for RESTAPI only

Better use daphne CoreRoot.asgi:application to start

GDAL is REQUIRED for this app

This is the link to download the data, https://drive.google.com/file/d/1vB1FeXLCC7dl6Onbp2SaJ0ZwEk2Ji166/view?usp=drive_link



## API Reference


#### Example
#### LOGIN first

```http
  POST /api/auth/login/
  {
	"username": "web001",
	"password":"123456"
  }
```

#### Get all locationpoints, need token from LOGIN
```http
  GET /api/locationpoints/?route_name=Morning%20Express&date=2025-07-03
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `route_name` | `string` | route_name |
| `date` | `string` | date |

## Run Locally

Clone the project

```bash
  git clone https://github.com/rookie4now123/transport.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
pip install --upgrade -r requirements.txt

```

Start the server

```bash
  daphne CoreRoot.asgi:application
```

