#!/bin/bash

# Solar Predictive Maintenance System - Installation Verification Script

echo "=========================================="
echo "SPMS Installation Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check counters
CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to check file/directory
check_exists() {
    if [ -e "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} $1 (MISSING)"
        ((CHECKS_FAILED++))
    fi
}

echo "Checking Backend Structure..."
check_exists "backend/main.py"
check_exists "backend/database.py"
check_exists "backend/models.py"
check_exists "backend/schemas.py"
check_exists "backend/crud.py"
check_exists "backend/requirements.txt"

echo ""
echo "Checking Backend Modules..."
check_exists "backend/core/config.py"
check_exists "backend/core/utils.py"
check_exists "backend/core/constants.py"

echo ""
echo "Checking Routers..."
check_exists "backend/routers/sensor.py"
check_exists "backend/routers/analytics.py"
check_exists "backend/routers/alert.py"
check_exists "backend/routers/health.py"

echo ""
echo "Checking ML Module..."
check_exists "backend/ml/model_training.py"
check_exists "backend/ml/model_predict.py"
check_exists "backend/ml/feature_engineering.py"

echo ""
echo "Checking Simulator..."
check_exists "simulator/solar_simulator.py"
check_exists "simulator/physics_model.py"
check_exists "simulator/weather_patterns.py"
check_exists "simulator/config.py"
check_exists "simulator/data_logger.py"

echo ""
echo "Checking Frontend..."
check_exists "frontend/package.json"
check_exists "frontend/vite.config.js"
check_exists "frontend/tailwind.config.js"
check_exists "frontend/src/App.jsx"
check_exists "frontend/src/main.jsx"

echo ""
echo "Checking Frontend Pages..."
check_exists "frontend/src/pages/Dashboard.jsx"
check_exists "frontend/src/pages/PanelDetails.jsx"
check_exists "frontend/src/pages/Settings.jsx"

echo ""
echo "Checking Frontend Components..."
check_exists "frontend/src/components/NavBar.jsx"
check_exists "frontend/src/components/DashboardCard.jsx"
check_exists "frontend/src/components/AlertsPanel.jsx"
check_exists "frontend/src/components/Charts/PowerOutputChart.jsx"
check_exists "frontend/src/components/Charts/EnvironmentalChart.jsx"

echo ""
echo "Checking Configuration..."
check_exists "docker-compose.yml"
check_exists "Dockerfile"
check_exists ".env.example"
check_exists ".gitignore"
check_exists "requirements.txt"

echo ""
echo "Checking Documentation..."
check_exists "README.md"
check_exists "QUICKSTART.md"
check_exists "PROJECT_SUMMARY.md"
check_exists "docs/api_reference.md"
check_exists "docs/system_design.md"
check_exists "docs/PITCH_DECK_OUTLINE.md"

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"
echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All files present! Installation verified.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Read QUICKSTART.md for setup instructions"
    echo "2. Run 'docker-compose up' or follow manual setup"
    echo "3. Train ML model: python -m backend.ml.model_training"
    echo "4. Start simulator: python -m simulator.solar_simulator"
    echo ""
else
    echo -e "${RED}✗ Some files are missing. Please check installation.${NC}"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Python 3 not found in PATH"
fi

# Check Node version
echo "Checking Node.js version..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node $NODE_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Node.js not found in PATH"
fi

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}✓${NC} $DOCKER_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Docker not found (optional)"
fi

echo ""
echo "=========================================="
echo "Ready to build! 🚀"
echo "=========================================="
