# API Reference

## Base URL
```
http://localhost:8000
```

## Health & Status Endpoints

### GET /api/health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-17T10:00:00Z",
  "service": "Solar Predictive Maintenance System"
}
```

### GET /api/status
System status and statistics

**Response:**
```json
{
  "status": "operational",
  "statistics": {
    "total_sensor_readings": 1500,
    "total_predictions": 250,
    "open_maintenance_alerts": 3
  },
  "timestamp": "2025-10-17T10:00:00Z"
}
```

## Sensor Data Endpoints

### POST /api/sensor/upload
Upload sensor reading from IoT device

**Request Body:**
```json
{
  "panel_id": "panel_001",
  "timestamp": "2025-10-17T10:00:00Z",
  "pm10": 120.5,
  "pm25": 65.3,
  "temperature": 32.5,
  "humidity": 45.2,
  "irradiance": 850.0,
  "power_output": 3420.5
}
```

**Response:** 201 Created
```json
{
  "id": 123,
  "panel_id": "panel_001",
  "timestamp": "2025-10-17T10:00:00Z",
  ...
}
```

### GET /api/sensor/readings
Retrieve sensor readings

**Query Parameters:**
- `panel_id` (optional): Filter by panel
- `hours` (default: 24): Get readings from last N hours
- `limit` (default: 100): Maximum records to return

**Response:**
```json
[
  {
    "id": 123,
    "panel_id": "panel_001",
    "timestamp": "2025-10-17T10:00:00Z",
    "pm10": 120.5,
    ...
  }
]
```

### GET /api/sensor/readings/latest/{panel_id}
Get most recent reading for a panel

## Analytics Endpoints

### GET /api/analytics/summary/{panel_id}
Get analytics summary

**Query Parameters:**
- `hours` (default: 24): Analysis window

**Response:**
```json
{
  "panel_id": "panel_001",
  "total_readings": 144,
  "avg_power_output": 3250.5,
  "avg_degradation_score": 12.5,
  "active_alerts": 1,
  "last_reading_time": "2025-10-17T10:00:00Z"
}
```

### POST /api/analytics/predict/{panel_id}
Generate performance prediction

**Response:**
```json
{
  "id": 45,
  "panel_id": "panel_001",
  "predicted_output": 3500.0,
  "actual_output": 3250.0,
  "degradation_score": 7.1,
  "cleaning_alert": false,
  "maintenance_priority": "normal"
}
```

### GET /api/analytics/predictions
Get prediction history

**Query Parameters:**
- `panel_id` (optional): Filter by panel
- `limit` (default: 100): Maximum records

### GET /api/analytics/trend/{panel_id}
Get performance trend data

**Query Parameters:**
- `hours` (default: 168): Time window (7 days)

## Alerts Endpoints

### POST /api/alerts/
Create maintenance alert

**Request Body:**
```json
{
  "panel_id": "panel_001",
  "alert_type": "cleaning",
  "priority": "high",
  "message": "Dust accumulation affecting performance",
  "estimated_days_until_critical": 3
}
```

### GET /api/alerts/
Get maintenance alerts

**Query Parameters:**
- `panel_id` (optional): Filter by panel
- `status` (default: "open"): Filter by status (open, acknowledged, resolved)
- `limit` (default: 100): Maximum records

### PATCH /api/alerts/{alert_id}/status
Update alert status

**Query Parameters:**
- `new_status`: New status (acknowledged, resolved)

## Error Responses

All endpoints may return standard HTTP error codes:

- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Format:**
```json
{
  "detail": "Error message description"
}
```
