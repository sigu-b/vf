# System Design Document

## Solar Predictive Maintenance System (SPMS)

### 1. Overview

The Solar Predictive Maintenance System is an AI-driven platform that predicts solar panel performance degradation due to dust accumulation and environmental conditions.

### 2. Architecture

```
┌─────────────────┐
│   IoT Devices   │
│   (Simulated)   │
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────────────────────────────┐
│          FastAPI Backend                │
│  ┌──────────────────────────────────┐  │
│  │  Sensor Data Ingestion           │  │
│  │  - Validation (Pydantic)         │  │
│  │  - Storage (PostgreSQL)          │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  ML Analytics Engine             │  │
│  │  - Feature Engineering           │  │
│  │  - Random Forest Prediction      │  │
│  │  - Degradation Scoring           │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  Alert Generation                │  │
│  │  - Threshold Monitoring          │  │
│  │  - Maintenance Recommendations   │  │
│  └──────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │ REST API
                  ▼
         ┌────────────────┐
         │  React Frontend │
         │  - Dashboard    │
         │  - Charts       │
         │  - Alerts       │
         └────────────────┘
```

### 3. Data Flow

#### 3.1 Sensor Data Ingestion
1. Simulator generates realistic sensor data
2. Data posted to `/api/sensor/upload`
3. Pydantic validates data structure
4. SQLAlchemy stores in PostgreSQL
5. Acknowledgment returned

#### 3.2 Prediction Pipeline
1. User/System triggers prediction
2. Latest sensor data retrieved
3. Features engineered (12 features from 5 base sensors)
4. ML model predicts expected power output
5. Degradation score calculated (actual vs predicted)
6. Alert generated if threshold exceeded
7. Results stored and returned

#### 3.3 Dashboard Visualization
1. Frontend polls API every 10 seconds
2. Retrieves sensor readings and analytics
3. Renders charts using Recharts
4. Displays alerts and recommendations

### 4. Database Schema

#### sensor_readings
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| panel_id | String | Panel identifier |
| timestamp | DateTime | Reading timestamp |
| pm10 | Float | PM10 concentration (μg/m³) |
| pm25 | Float | PM2.5 concentration (μg/m³) |
| temperature | Float | Temperature (°C) |
| humidity | Float | Humidity (%) |
| irradiance | Float | Solar irradiance (W/m²) |
| power_output | Float | Power output (W) |
| created_at | DateTime | Record creation time |

#### predictions
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| panel_id | String | Panel identifier |
| timestamp | DateTime | Prediction timestamp |
| predicted_output | Float | Predicted power (W) |
| actual_output | Float | Actual power (W) |
| degradation_score | Float | Performance loss (%) |
| cleaning_alert | Boolean | Cleaning required flag |
| maintenance_priority | String | Priority level |
| created_at | DateTime | Record creation time |

#### maintenance_alerts
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| panel_id | String | Panel identifier |
| timestamp | DateTime | Alert timestamp |
| alert_type | String | Type (cleaning, inspection, repair) |
| priority | String | Priority level |
| message | String | Alert description |
| estimated_days_until_critical | Integer | Days until critical |
| status | String | Status (open, acknowledged, resolved) |
| resolved_at | DateTime | Resolution timestamp |
| created_at | DateTime | Record creation time |

### 5. ML Model

#### Features (12 engineered features)
1. Base features: pm10, pm25, temperature, humidity, irradiance
2. Interaction features:
   - dust_total = pm10 + pm25
   - dust_ratio = pm25 / (pm10 + 1)
   - temp_irradiance = temperature × irradiance
   - humidity_temp = humidity × temperature
3. Polynomial features:
   - pm10_squared
   - temperature_squared
4. Derived features:
   - temp_deviation = |temperature - 25|

#### Model: Random Forest Regressor
- n_estimators: 100
- max_depth: 15
- Target: power_output (W)
- Performance: R² > 0.95, RMSE < 100W

#### Physics-Based Fallback
When ML model unavailable:
```python
base_power = irradiance × 4.0
dust_loss = (pm10 × 0.0015 + pm25 × 0.002) %
temp_loss = max(0, (temperature - 25) × 0.004) %
power = base_power × (1 - total_loss)
```

### 6. Environmental Simulation

The simulator generates realistic data based on:

#### Diurnal Patterns
- Solar irradiance: Sinusoidal curve (sunrise 6:30 AM, sunset 6:30 PM)
- Temperature: Peak at 2 PM (~30°C), minimum at 6 AM (~15°C)
- Humidity: Inverse of temperature (higher at night)

#### Dust Accumulation
- Gradual accumulation: 2 μg/m³ per day
- Rain events: 10% probability, removes 70% of dust
- Wind variation: ±30% dust levels

#### Regional Calibration (Nairobi, Kenya)
- PM10 baseline: 80 μg/m³ (dry season)
- Temperature range: 15-35°C
- Humidity range: 30-70%
- Irradiance max: 1000 W/m²

### 7. Scaling Considerations

#### Current Capacity
- 3 panels simulated
- ~100 readings/hour/panel
- ~7,200 readings/day total

#### Scaling to 100 Panels
- Database indexing on panel_id, timestamp
- Implement caching (Redis)
- Batch predictions (Celery workers)
- Time-series database (TimescaleDB)

#### Scaling to 1,000+ Panels
- Microservices architecture
- Message queue (RabbitMQ/Kafka)
- Distributed ML inference
- CDN for frontend
- Cloud deployment (AWS/GCP)

### 8. Security (Future)

- JWT authentication
- API rate limiting
- HTTPS only
- Database encryption
- Role-based access control (RBAC)

### 9. Deployment

#### Development
```bash
docker-compose up
```

#### Production
- Backend: Render/Fly.io/AWS ECS
- Database: Managed PostgreSQL (RDS/Supabase)
- Frontend: Vercel/Netlify
- CI/CD: GitHub Actions
