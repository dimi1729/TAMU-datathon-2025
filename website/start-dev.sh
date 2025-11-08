#!/bin/bash

# College Assistant - Development Startup Script
# This script starts both the Flask backend and Next.js frontend

echo "Starting College Assistant Development Environment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}Error: Please run this script from the website/ directory${NC}"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}Warning: Port $port is already in use${NC}"
        return 1
    fi
    return 0
}

# Check ports
echo -e "${BLUE}Checking ports...${NC}"
check_port 5000
backend_port_free=$?
check_port 3000
frontend_port_free=$?

# Start backend
echo -e "\n${BLUE}Starting Flask Backend (Port 5000)...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Start Flask in background
echo -e "${GREEN}✓ Starting Flask server...${NC}"
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo -e "\n${BLUE}Starting Next.js Frontend (Port 3000)...${NC}"
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing npm dependencies...${NC}"
    npm install
fi

# Start Next.js in background
echo -e "${GREEN}✓ Starting Next.js development server...${NC}"
npm run dev &
FRONTEND_PID=$!

# Wait for both services to start
sleep 5

echo -e "\n${GREEN}Development servers started successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo -e "Backend API: ${BLUE}http://localhost:5000${NC}"
echo -e "Frontend UI: ${BLUE}http://localhost:3000${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✓ Servers stopped. Thanks!${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Keep script running
wait
