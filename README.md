# 🌞 Solar Predictive Maintenance System (SPMS)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![React](https://img.shields.io/badge/React-18.2-blue.svg)

An AI-driven predictive maintenance platform for solar panels that predicts performance degradation due to dust accumulation and environmental conditions.

## 🚀 Features

- **Real-time IoT Data Ingestion**: Collect sensor data from solar panels (PM10, PM2.5, temperature, humidity, irradiance)
- **AI-Powered Predictions**: Machine learning models predict panel efficiency loss and degradation
- **Predictive Maintenance Alerts**: Automated alerts when cleaning or maintenance is needed
- **Interactive Dashboard**: Real-time visualization of panel performance, environmental conditions, and alerts
- **Physics-Based Simulation**: Realistic solar panel data simulator for testing and development

## 🏗️ Architecture

```
solar-predictive-maintenance-system/
├── backend/              # FastAPI backend
│   ├── main.py          # API entry point
│   ├── models.py        # Database models
│   ├── routers/         # API endpoints
│   ├── ml/              # Machine learning models
│   └── core/            # Configuration
├── frontend/            # React dashboard
│   ├── src/
│   │   ├── pages/       # Dashboard pages
│   │   ├── components/  # React components
│   │   └── services/    # API client
├── simulator/           # IoT data simulator
│   ├── solar_simulator.py
│   ├── physics_model.py
│   └── weather_patterns.py
├── docs/                # Documentation
└── docker-compose.yml   # Docker orchestration
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or use Docker)
- Git

## 🔧 Installation

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd solar-predictive-maintenance-system
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start services:
```bash
docker-compose up -d
```

4. Access the application:
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Frontend: http://localhost:5173

### Option 2: Local Development

#### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Set up PostgreSQL database:
```bash
createdb solar_maintenance
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Train ML model (first time only):
```bash
python -m backend.ml.model_training
```

6. Start backend:
```bash
uvicorn backend.main:app --reload
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

#### Simulator Setup

1. Install dependencies:
```bash
pip install -r simulator/requirements.txt
```

2. Start simulator:
```bash
python -m simulator.solar_simulator
```

## 🎯 Usage

### Starting the System

1. **Start Backend**: The API server handles data ingestion and predictions
2. **Start Frontend**: Access the dashboard at http://localhost:5173
3. **Start Simulator**: Generates realistic sensor data for 3 panels

### Dashboard Features

- **Overview Dashboard**: View all panels, total power output, and system metrics
- **Panel Details**: Deep dive into individual panel performance
- **Environmental Charts**: Monitor PM10, temperature, humidity, and irradiance
- **Alerts Panel**: Track maintenance alerts and recommendations
- **Prediction Engine**: Run AI predictions on demand

### API Documentation

Access interactive API docs at http://localhost:8000/docs

Key endpoints:
- `POST /api/sensor/upload` - Upload sensor data
- `GET /api/analytics/summary/{panel_id}` - Get analytics
- `POST /api/analytics/predict/{panel_id}` - Generate prediction
- `GET /api/alerts/` - Get maintenance alerts

## 🧠 Machine Learning Model

The system uses a **Random Forest Regressor** trained on:

**Input Features (12 engineered features):**
- Environmental: PM10, PM2.5, temperature, humidity, irradiance
- Derived: dust_total, dust_ratio, temp×irradiance, etc.

**Output:**
- Predicted power output (W)
- Degradation score (0-100%)
- Maintenance priority (low, normal, high, critical)

**Performance:**
- R² Score: >0.95
- RMSE: <100W
- MAE: <75W

### Training Custom Model

```bash
python -m backend.ml.model_training
```

The model will be saved to `backend/ml/models/solar_prediction_model.joblib`

## 📊 Simulation Details

The simulator generates realistic data based on:

- **Diurnal patterns**: Sunrise/sunset cycles, temperature variations
- **Dust accumulation**: Gradual buildup with rain cleaning events
- **Weather patterns**: Cloud cover, humidity, wind effects
- **Regional calibration**: Based on Nairobi, Kenya climate

## 🧪 Testing

Run backend tests:
```bash
pytest backend/tests/
```

## 📚 Documentation

- [API Reference](docs/api_reference.md)
- [System Design](docs/system_design.md)
- Architecture Diagram: `docs/architecture_diagram.png` (to be created)

## 🚢 Deployment

### Backend Deployment (Render/Fly.io)

1. Push to GitHub
2. Connect to hosting platform
3. Set environment variables
4. Deploy!

### Frontend Deployment (Vercel/Netlify)

```bash
cd frontend
npm run build
# Deploy dist/ folder
```

## 🔮 Future Enhancements

- [ ] Real IoT device integration (ESP32 + sensors)
- [ ] Multi-site management with map view
- [ ] WhatsApp/SMS alert notifications
- [ ] Historical trend analysis and reporting
- [ ] Mobile app (React Native)
- [ ] Advanced ML models (LSTM for time series)
- [ ] Integration with solar monitoring APIs
- [ ] Authentication and user management

## 🌍 Real-World Applications

This system has potential for:

- **Solar Companies**: M-KOPA, Powerhive, d.light (maintenance optimization)
- **Off-Grid Sites**: Remote monitoring and maintenance scheduling
- **Research**: Solar panel degradation studies in African climates
- **Government**: Monitoring public solar installations

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your university project, startup, or research!

## 👥 Authors

**Your Name** - University Project / Startup MVP

## 🙏 Acknowledgments

- Solar panel physics models based on research literature
- Weather patterns calibrated for Nairobi, Kenya
- Inspired by real-world solar maintenance challenges in East Africa

## 📞 Contact

For questions, partnerships, or demo requests:
- Email: your.email@example.com
- GitHub: @yourusername

---

**Built with ❤️ for sustainable energy in Africa**
