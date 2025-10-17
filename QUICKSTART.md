# 🚀 Quick Start Guide

Get your Solar Predictive Maintenance System running in under 5 minutes!

## Prerequisites Check

```bash
python --version  # Should be 3.11+
node --version    # Should be 18+
docker --version  # Optional but recommended
```

## Option A: Docker (Easiest)

### 1. Start Everything

```bash
# Clone and navigate
git clone <repo-url>
cd solar-predictive-maintenance-system

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d
```

### 2. Train the ML Model (First Time Only)

```bash
# Enter the backend container
docker exec -it solar_maintenance_backend bash

# Train model
python -m backend.ml.model_training

# Exit container
exit
```

### 3. Access the Application

- 🌐 Frontend Dashboard: http://localhost:5173
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs
- 💾 Database: localhost:5432

## Option B: Local Development

### 1. Backend Setup (Terminal 1)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set up database (if you have PostgreSQL installed)
createdb solar_maintenance

# Or update .env to use SQLite
# DATABASE_URL=sqlite:///./solar_maintenance.db

# Copy and edit environment file
cp .env.example .env

# Train ML model
python -m backend.ml.model_training

# Start backend
uvicorn backend.main:app --reload
```

### 2. Frontend Setup (Terminal 2)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Start Simulator (Terminal 3)

```bash
# Activate virtual environment (same as backend)
source venv/bin/activate

# Install simulator dependencies
pip install -r simulator/requirements.txt

# Start simulator
python -m simulator.solar_simulator
```

## What You Should See

### Terminal 1 (Backend)
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 (Frontend)
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Terminal 3 (Simulator)
```
======================================================================
Solar Panel IoT Simulator Started
======================================================================
API Endpoint: http://localhost:8000/api/sensor/upload
Panels: panel_001, panel_002, panel_003
Interval: 5 seconds

[Iteration 1] 2025-10-17 10:00:00
✓ panel_001: 3420W (Irr: 850W/m², PM10: 120μg/m³)
✓ panel_002: 3380W (Irr: 845W/m², PM10: 118μg/m³)
✓ panel_003: 3450W (Irr: 855W/m², PM10: 115μg/m³)
```

## First Steps

### 1. View the Dashboard
Open http://localhost:5173 in your browser

You should see:
- 3 active solar panels
- Real-time power output
- System statistics

### 2. Explore a Panel
Click on any panel card to see:
- Detailed performance metrics
- Environmental condition charts
- Power output trends

### 3. Generate Predictions
On a panel detail page:
1. Click "Run Prediction"
2. View the AI-generated degradation score
3. Check for maintenance alerts

### 4. Check the API
Visit http://localhost:8000/docs for interactive API documentation

Try these endpoints:
- GET `/api/health` - Health check
- GET `/api/sensor/readings` - View recent data
- GET `/api/status` - System statistics

## Common Issues & Solutions

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn backend.main:app --port 8001
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Simulator can't connect
```bash
# Make sure backend is running on port 8000
curl http://localhost:8000/api/health

# If using different port, update simulator/config.py
# API_BASE_URL = "http://localhost:8001"
```

### Database connection error
```bash
# Option 1: Use SQLite (simpler for dev)
# In .env file:
DATABASE_URL=sqlite:///./solar_maintenance.db

# Option 2: Start PostgreSQL with Docker
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=solar_maintenance \
  postgres:15-alpine
```

### ML model not found
```bash
# Train the model first
python -m backend.ml.model_training

# Verify model file exists
ls backend/ml/models/solar_prediction_model.joblib
```

## Verify Everything Works

Run this checklist:

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] Simulator sending data every 5 seconds
- [ ] Dashboard showing 3 panels
- [ ] Can view panel details
- [ ] Can generate predictions
- [ ] Alerts appearing when degradation > 15%

## Next Steps

1. **Customize the simulator**: Edit `simulator/config.py` to add more panels
2. **Adjust thresholds**: Modify `backend/core/constants.py` for different alert levels
3. **Train with real data**: Replace synthetic data in `backend/ml/model_training.py`
4. **Deploy to cloud**: See deployment guides in `docs/`

## Getting Help

- Check `README.md` for detailed documentation
- Review API reference in `docs/api_reference.md`
- View system design in `docs/system_design.md`

## Stop Everything

```bash
# Docker
docker-compose down

# Local (press Ctrl+C in each terminal)
# Then deactivate virtual environment
deactivate
```

---

**You're all set! Start building the future of solar energy maintenance! ⚡**
