# Commander MTG API
This service handles CRUD operations for Magic: The Gathering Commander games, commanders, games (partidas), and user-commander relationships.
The user/Log in is handeled in the Login_service ! INSERTAR LINK DEL SERVEI

**⚠️ Requirements:** PostgreSQL database is required.

## Configuration

Create a `settings.py` file in the `SRC/` directory with the following database configuration:

```python
db_config = {
    'host': 'localhost',        # Database host (e.g., localhost)
    'user': 'postgres',         # Database username
    'password': 'your_password', # Database password
    'database': 'proj',         # Database name
    'port': 5432             # Database port (5432 default)
}
```

## Database Schema


```sql
CREATE DATABASE proj;
\c proj;
CREATE TABLE usuari(
	id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL UNIQUE,
    mail VARCHAR(60) NOT NULL UNIQUE,
    hash VARCHAR(60) NOT NULL UNIQUE
);
CREATE TABLE commander(
	id SERIAL PRIMARY KEY,
	commander VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE partida(
	id SERIAL PRIMARY KEY,
    winner INT
);
CREATE TABLE usuari_commander (
    id SERIAL PRIMARY KEY,                    
    id_usuari INT NOT NULL,                   
    id_commander INT NOT NULL,                   
    id_partida INT NOT NULL,                   
    
    CONSTRAINT fk_usuari                   
        FOREIGN KEY (id_usuari)         
        REFERENCES usuari (id)         
        ON DELETE CASCADE,

    CONSTRAINT fk_commander         
        FOREIGN KEY (id_commander)
        REFERENCES commander (id)
        ON DELETE CASCADE,

    CONSTRAINT fk_partida
        FOREIGN KEY (id_partida)
        REFERENCES partida (id)
        ON DELETE CASCADE
);
```

## API Endpoints

### Root Endpoint
- **GET /** - Check API status
  ```bash
  curl http://localhost:8442/
  ```

### Commander Management

#### Get All Commanders
- **GET /commanders/** - Retrieve all commanders with pagination and filtering
  ```bash
  curl "http://localhost:8442/commanders/?pag=1&limit=10&name=Atraxa"
  ```

#### Get Commander by ID
- **GET /commanders/{id}** - Get specific commander by ID
  ```bash
  curl http://localhost:8442/commanders/1
  ```

#### Create New Commander
- **POST /commanders/** - Create a new commander
  ```bash
  curl -X POST http://localhost:8442/commanders/ \
    -H "Content-Type: application/json" \
    -d '{
      "commander": "Atraxa, Praetors Voice"
    }'
  ```

#### Update Commander 
- **PUT /commanders/{id}** - Update of commander
  ```bash
  curl -X PUT http://localhost:8442/commanders/1 \
    -H "Content-Type: application/json" \
    -d '{
      "commander": "Atraxa, Praetors Voice (Updated)"
    }'
  ```

#### Delete Commander
- **DELETE /commanders/{id}** - Delete commander by ID
  ```bash
  curl -X DELETE http://localhost:8442/commanders/1
  ```

### Game Management (Partidas)

#### Get All Games
- **GET /partidas/** - Retrieve all games with pagination and filtering
  ```bash
  curl "http://localhost:8442/partidas/?pag=1&limit=10&winner=1"
  ```

#### Get Game by ID
- **GET /partidas/{id}** - Get specific game by ID
  ```bash
  curl http://localhost:8442/partidas/1
  ```

#### Create New Game
- **POST /partidas/** - Create a new game
  ```bash
  curl -X POST http://localhost:8442/partidas/ \
    -H "Content-Type: application/json" \
    -d '{
      "winner": 1
    }'
  ```

#### Update Game 
- **PUT /partidas/{id}** - Update of game
  ```bash
  curl -X PUT http://localhost:8442/partidas/1 \
    -H "Content-Type: application/json" \
    -d '{
      "winner": 2
    }'
  ```

#### Delete Game
- **DELETE /partidas/{id}** - Delete game by ID
  ```bash
  curl -X DELETE http://localhost:8442/partidas/1
  ```

### User-Commander Relationships

#### Get All User-Commander Relationships
- **GET /usuaris_commanders/** - Retrieve all relationships with pagination
  ```bash
  curl "http://localhost:8442/usuaris_commanders/?pag=1&limit=10"
  ```

#### Get Relationship by ID
- **GET /usuaris_commanders/{id}** - Get specific relationship by ID
  ```bash
  curl http://localhost:8442/usuaris_commanders/1
  ```

#### Create New Relationship
- **POST /usuaris_commanders/** - Create a new user-commander relationship
  ```bash
  curl -X POST http://localhost:8442/usuaris_commanders/ \
    -H "Content-Type: application/json" \
    -d '{
      "id_usuari": 1,
      "id_commander": 1,
      "id_partida": 1
    }'
  ```

#### Update Relationship 
- **PUT /usuaris_commanders/{id}** - Update of relationship
  ```bash
  curl -X PUT http://localhost:8442/usuaris_commanders/1 \
    -H "Content-Type: application/json" \
    -d '{
      "id_usuari": 1,
      "id_commander": 2,
      "id_partida": 1
    }'
  ```

#### Delete Relationship
- **DELETE /usuaris_commanders/{id}** - Delete relationship by ID
  ```bash
  curl -X DELETE http://localhost:8442/usuaris_commanders/1
  ```

## Usage

### Setup and Installation
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the FastAPI server
# Make sure that the database is running
./venv/bin/uvicorn SRC.main:app --reload --host 0.0.0.0 --port 8442
```

### Access the API
When the api is running you can use:

- **API Base URL**: http://localhost:8442
- **Interactive Documentation**: http://localhost:8442/docs
- **Alternative Documentation**: http://localhost:8442/redoc

## Docker Deployment

### Prerequisites
- Docker installed on your system
- PostgreSQL database running (can be in a container or host machine)

### Building the Docker Image
```bash
# Build the API Docker image
sudo docker build -t mtg-commander-api .
```

### Running with Docker

#### Option 1: Connect to existing PostgreSQL database
```bash
# Make sure your PostgreSQL database is running first
sudo docker start postgres-db  # if using Docker for database
sudo docker start login-api-container    # if using Docker for the login service
# Run the API container
sudo docker run -d \
  --name mtg-commander-api-container \
  -p 8442:8442 \
  -e DB_HOST=172.17.0.1 \
  -e DB_PORT=8888 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=proj \
  mtg-commander-api
```

#### Option 2: Using host database
```bash
# If database and login service are running on host machine 
sudo docker run -d \
  --name mtg-commander-api-container \
  -p 8442:8442 \
  -e DB_HOST=172.17.0.1 \
  -e DB_PORT=5432 \
  -e DB_USER=postgres \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=proj \
  mtg-commander-api
```

### Docker Management Commands
```bash
# Check running containers
sudo docker ps

# View API logs
sudo docker logs mtg-commander-api-container

# Stop the container
sudo docker stop mtg-commander-api-container

# Start the container
sudo docker start mtg-commander-api-container

# Remove the container
sudo docker rm mtg-commander-api-container

# Remove the image
sudo docker rmi mtg-commander-api
```

### Environment Variables
The Docker container supports these environment variables:
- `DB_HOST` - Database host (default: localhost)
- `DB_PORT` - Database port (default: 8888)  
- `DB_USER` - Database username (default: postgres)
- `DB_PASSWORD` - Database password (default: root)
- `DB_NAME` - Database name (default: proj)

### Docker Network Notes
- Use `172.17.0.1` as DB_HOST to connect to services on the Docker host
- Make sure the PostgreSQL database accepts connections from Docker containers
- Port 8442 will be exposed for API access