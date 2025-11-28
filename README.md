# BankSync

Aplicación web full-stack con Vue.js 3 + FastAPI + PostgreSQL (Supabase)

## Características

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

Click image to watch demo video on YouTube 


## Features
- FastAPI backend with PostgreSQL database
- SQLAlchemy CRUD with async support
- Simple User CRUD
- OAuth2 authentication with JWT tokens
- Store refresh token in `httpOnly` cookie, access token in memory ( Pinia store )
- Vue3 frontend with Pinia store
- Conciliaciones bancarias con IA (OpenAI)

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
- PostgreSQL en Supabase
- Conexión remota segura
- Gestión de usuarios y autenticación

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
- `backend/.env`  for backend
    - `DATABASE_URL`  Supabase connection string
    - `ACCESS_TOKEN_SECRET`
    - `REFRESH_TOKEN_SECRET`
    - `ACCESS_TOKEN_EXPIRE_MINUTES`
    - `REFRESH_TOKEN_EXPIRE_MINUTES`
    - `OPENAI_API_KEY`  for conciliaciones bancarias
- `frontend/.env`  for development API url
- `frontend/.env.production`  for production API url
    

## Deployment

### Production
- Backend: Deploy FastAPI to services like Railway, Render, or Heroku
- Frontend: Deploy to Vercel, Netlify, or similar
- Database: Supabase (already cloud-hosted)

## Instalación y Configuración

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

##  Uso

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


## Issues & PR
Feel free to open an issue !

Pull requests are welcome. <br>
Any contributions you make are **greatly appreciated**.

