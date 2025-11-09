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

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    local pids=$(lsof -ti :$port)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}Killing processes on port $port...${NC}"
        kill -9 $pids 2>/dev/null || true
        sleep 2
    fi
}

# Check ports and kill if necessary
echo -e "${BLUE}Checking ports...${NC}"
if ! check_port 5000; then
    kill_port 5000
fi
if ! check_port 3000; then
    kill_port 3000
fi

# Start backend
echo -e "\n${BLUE}Starting Flask Backend (Port 5000)...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo -e "${YELLOW}Activating Python virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1

# Start Flask in background
echo -e "${GREEN}✓ Starting Flask server...${NC}"
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

# Start frontend
echo -e "\n${BLUE}Starting Next.js Frontend (Port 3000)...${NC}"
cd ../frontend

# Check if node_modules exists and if Next.js is available
if [ ! -d "node_modules" ] || ! command -v ./node_modules/.bin/next &> /dev/null; then
    echo -e "${YELLOW}Installing/updating npm dependencies...${NC}"

    # Clean install to avoid version conflicts
    rm -rf node_modules package-lock.json 2>/dev/null || true
    npm cache clean --force 2>/dev/null || true

    echo -e "${YELLOW}Running fresh npm install...${NC}"
    npm install

    # Fix any audit issues
    echo -e "${YELLOW}Fixing security vulnerabilities...${NC}"
    npm audit fix --force 2>/dev/null || true
fi

# Verify Next.js is working
if ! ./node_modules/.bin/next --version >/dev/null 2>&1; then
    echo -e "${YELLOW}Next.js not found, reinstalling dependencies...${NC}"
    rm -rf node_modules package-lock.json
    npm install
fi

# Start Next.js in background
echo -e "${GREEN}✓ Starting Next.js development server...${NC}"
npm run dev &
FRONTEND_PID=$!

# Wait for both services to start
sleep 5

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Frontend failed to start${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo -e "\n${GREEN}Development servers started successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo -e "Backend API: ${BLUE}http://localhost:5000${NC}"
echo -e "Backend Health: ${BLUE}http://localhost:5000/api/health${NC}"
echo -e "Frontend UI: ${BLUE}http://localhost:3000${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo -e "${YELLOW}Logs will appear below:${NC}"
echo -e "${YELLOW}========================${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"

    # Kill the background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi

    # Extra cleanup - kill any remaining processes on these ports
    kill_port 5000
    kill_port 3000

    echo -e "${GREEN}✓ Servers stopped. Thanks!${NC}"
    exit 0
}

# Trap Ctrl+C and other signals
trap cleanup INT TERM

# Keep script running and show logs
wait
