#!/bin/bash

# Quick Start Script for Campus Compass
# This script quickly fixes common issues and starts the development servers

echo "Campus Compass Quick Start"
echo "=============================="

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

# Kill any processes that might be running on our ports
echo -e "${BLUE}Cleaning up any existing processes...${NC}"
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "next dev" 2>/dev/null || true
pkill -f "node.*next" 2>/dev/null || true
sleep 2

# Setup backend
echo -e "\n${BLUE}Setting up Backend...${NC}"
cd backend

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate and install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
source venv/bin/activate
pip install -r requirements.txt --quiet

# Start backend in background
echo -e "${GREEN}Starting Flask backend on port 5000...${NC}"
python app.py &
BACKEND_PID=$!
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is running successfully${NC}"
else
    echo -e "${YELLOW}⚠ Backend may still be starting up...${NC}"
fi

# Setup frontend
echo -e "\n${BLUE}Setting up Frontend...${NC}"
cd ../frontend

# Force clean install to avoid dependency issues
echo -e "${YELLOW}Cleaning npm cache and node_modules...${NC}"
rm -rf node_modules package-lock.json .next 2>/dev/null || true
npm cache clean --force --silent 2>/dev/null || true

echo -e "${YELLOW}Installing npm dependencies (this may take a moment)...${NC}"
npm install --silent

# Fix any security vulnerabilities
npm audit fix --force --silent 2>/dev/null || true

# Start frontend
echo -e "${GREEN}Starting Next.js frontend on port 3000...${NC}"
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 8

echo -e "\n${GREEN}Campus Compass is starting up!${NC}"
echo -e "${GREEN}=================================${NC}"
echo -e "Backend API: ${BLUE}http://localhost:5000${NC}"
echo -e "Frontend UI: ${BLUE}http://localhost:3000${NC}"
echo -e "Health Check: ${BLUE}http://localhost:5000/api/health${NC}"
echo -e "\n${YELLOW}Wait about 10-15 seconds for Next.js to fully compile...${NC}"
echo -e "${YELLOW}Then open http://localhost:3000 in your browser!${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"

    # Kill background processes
    [ ! -z "$BACKEND_PID" ] && kill $BACKEND_PID 2>/dev/null || true
    [ ! -z "$FRONTEND_PID" ] && kill $FRONTEND_PID 2>/dev/null || true

    # Kill any remaining processes
    pkill -f "python.*app.py" 2>/dev/null || true
    pkill -f "next dev" 2>/dev/null || true
    pkill -f "node.*next" 2>/dev/null || true

    echo -e "${GREEN}✓ All servers stopped. Goodbye!${NC}"
    exit 0
}

# Trap exit signals
trap cleanup INT TERM

# Keep script running
echo -e "\n${BLUE}Monitoring servers... (Ctrl+C to stop)${NC}"
while true; do
    sleep 5

    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}Backend process died unexpectedly${NC}"
        break
    fi

    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}Frontend process died unexpectedly${NC}"
        break
    fi
done

cleanup
