# BankSync

Aplicación web full-stack con Vue.js 3 + FastAPI + PostgreSQL (Supabase)

## 🚀 Características

- Backend FastAPI con PostgreSQL (Supabase)
- CRUD con SQLAlchemy y soporte async
- Autenticación OAuth2 con JWT tokens
- Frontend Vue 3 con Composition API
- Tailwind CSS para estilos modernos
- Pinia para manejo de estado
- Refresh token en cookies httpOnly, access token en memoria

## Demo
`localhost` for frontend <br>
`localhost:5001/docs` for backend swagger docs

<a href="https://www.youtube.com/watch?v=EOnzjuOir7o&ab_channel=ZhuDev" target="_blank">
 <img src="https://raw.githubusercontent.com/jason810496/FastAPI-Vue-OAuth2/main/docs/demo.png" alt="demo" height="300" />
</a>

Click image to watch demo video on YouTube ☝️


## Features
- FastAPI backend with PostgreSQL database
- SQLAlchemy CRUD with async support
- Simple User CRUD
- OAuth2 authentication with JWT tokens
- Store refresh token in `httpOnly` cookie, access token in memory ( Pinia store )
- Vue3 frontend with Pinia store
- Docker Compose for development and production

## Project Structure & Details
### Backend
- `app.py`  FastAPI application files
- `/api`  API endpoints
- `/auth`
    - OAuth2 authentication 
    - `get_current_user` dependency
- `/crud`
    - user related CRUD utilities
    - database session dependency
- `/database`  Database configuration files 
- `/models`  SQLAlchemy models using `declarative_base`
- `/schemas`  Pydantic schemas

### Database
- `PostgreSQL 15.1` image from Docker Hub
- exposed on port `5432`
- volume `postgres_data` for persistent data

### Frontend
- `Vite`  Frontend build tool
-  `/views`  Frontend page views
    - use `RefreshView.vue` as middleware to refresh JWT tokens
-  `/store`  Pinia store ( using `Data Provider Patten` )
-  `/router`  Vue router
- `/api`  API endpoints
    - `req.js` 
        - `axios` request wrapper , handle `401` unauthorized error to refresh JWT tokens
        - use `import.meta.env.VITE_APP_API_URL` to load API url from `.env` file

## Environment Variables
- `.env`  for postgres database
    - `POSTGRES_USER`
    - `POSTGRES_PASSWORD`
    - `POSTGRES_DB`
- `backend/.env`  for backend
    - `PORT`
    - `RELOAD`
    - `DATABASE_URL`  **Should be same as above setting dot file**
    - `JWT_ALGORITHM`
    - `ACCESS_TOKEN_SECRET`
    - `REFRESH_TOKEN_SECRET`
    - `ACCESS_TOKEN_EXPIRE_MINUTES`
    - `REFRESH_TOKEN_EXPIRE_MINUTES`

- `nginx/nginx.conf`  for nginx server
    - **Note :** backend hostname should be same as `docker-compose.yml` service name
- `frontend/.env`  for development API url
- `frontend/.env.production`  for production API url
    

## Deployment

### Containerization
- `docker-compose.yml`  Docker Compose configuration file
- `Dockerfile`  Dockerfile for frontend nginx server with production build
- `backend/Dockerfile`  Dockerfile for backend with hot reload

### Production
- `docker-compose up -d --build`

## 📦 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <tu-repo-url>
cd BankSync
```

### 2. Configurar Base de Datos (Supabase)

1. Crea una cuenta en [Supabase](https://supabase.com)
2. Crea un nuevo proyecto
3. Ve a **Settings > Database** y copia la **Connection String** (Direct connection)
4. Actualiza el archivo `backend/.env` con tu URL de Supabase:

```env
DATABASE_URL=postgresql+asyncpg://postgres:[TU_PASSWORD]@db.[TU_PROJECT_ID].supabase.co:5432/postgres
```

### 3. Backend (FastAPI)

#### Opción 1: Con Virtual Environment (Windows)
```bash
cd BankSync
.Venv\Scripts\Activate
cd backend
pip install -r requirements.txt
python run.py --dev
```

#### Opción 2: Sin Virtual Environment
```bash
cd backend
pip install -r requirements.txt
python run.py --dev
```

El backend estará disponible en: `http://localhost:5001`
Documentación API: `http://localhost:5001/docs`

### 4. Frontend (Vue 3 + Vite)

En una nueva terminal:

```bash
cd BankSync
.Venv\Scripts\Activate  # Si usas el virtual environment
cd frontend
npm install
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 🎯 Uso

1. **Registro**: Navega a `/register` o haz clic en "Regístrate" en la página de login
2. **Login**: Usa tus credenciales en la página principal (`/`)
3. **Dashboard**: Después del login, serás redirigido a `/home` donde verás la lista de usuarios
4. **Perfil**: Accede a `/profile` para ver tu perfil de usuario

## 🔧 Configuración de Variables de Entorno

### Backend (`backend/.env`)
```env
PORT=5001
RELOAD=True
DATABASE_URL=postgresql+asyncpg://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres
ACCESS_TOKEN_SECRET=tu_secret_key_aqui
REFRESH_TOKEN_SECRET=tu_refresh_secret_key_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
```

### Frontend (`frontend/.env`)
```env
VITE_APP_API_URL=http://localhost:5001/api
```

### Advanced : Kubernetes

```
Still working on it on features/k8s branch !
```

## Issues & PR
Feel free to open an issue !

Pull requests are welcome. <br>
Any contributions you make are **greatly appreciated**.

