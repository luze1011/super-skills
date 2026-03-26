#!/bin/bash
# run-playwright.sh - Run Playwright tests with server management
# Usage: ./run-playwright.sh [options]
#
# Options:
#   --server <cmd>    Server command to run before tests
#   --port <port>     Port to wait for (default: 3000)
#   --headed          # Run in headed mode (visible browser)
#   --debug           # Run in debug mode
#   --ui              # Run with Playwright UI
#   --trace           # Enable tracing
#
# Examples:
#   ./run-playwright.sh                                    # Run all Playwright tests
#   ./run-playwright.sh --headed                           # Run with visible browser
#   ./run-playwright.sh --server "npm run dev" --port 5173 # Start dev server first
#   ./run-playwright.sh tests/e2e/login.spec.ts            # Run specific test file

set -e

# Default configuration
SERVER_CMD=""
PORT=3000
HEADED=false
DEBUG=false
UI_MODE=false
TRACE=false
TEST_PATH="tests/e2e"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --server)
            SERVER_CMD="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --headed)
            HEADED=true
            shift
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        --ui)
            UI_MODE=true
            shift
            ;;
        --trace)
            TRACE=true
            shift
            ;;
        *)
            TEST_PATH="$1"
            shift
            ;;
    esac
done

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}🎭 Running Playwright tests...${NC}"
echo ""

# Check if Playwright is installed
if ! command -v npx &> /dev/null; then
    echo -e "${RED}Error: npx is not installed${NC}"
    echo "Install Node.js: https://nodejs.org/"
    exit 1
fi

# Build Playwright command
PW_CMD="npx playwright test ${TEST_PATH}"

if [ "$HEADED" = true ]; then
    PW_CMD="${PW_CMD} --headed"
fi

if [ "$DEBUG" = true ]; then
    PW_CMD="${PW_CMD} --debug"
fi

if [ "$UI_MODE" = true ]; then
    PW_CMD="npx playwright test --ui"
fi

if [ "$TRACE" = true ]; then
    PW_CMD="${PW_CMD} --trace on"
fi

# Function to wait for server
wait_for_server() {
    local port=$1
    local max_attempts=30
    local attempt=0
    
    echo -e "${BLUE}⏳ Waiting for server on port ${port}...${NC}"
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "http://localhost:${port}" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Server is ready on port ${port}${NC}"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
        echo -n "."
    done
    
    echo ""
    echo -e "${RED}❌ Server failed to start on port ${port}${NC}"
    return 1
}

# Start server if specified
SERVER_PID=""
if [ -n "$SERVER_CMD" ]; then
    echo -e "${BLUE}🚀 Starting server: ${SERVER_CMD}${NC}"
    $SERVER_CMD &
    SERVER_PID=$!
    
    if ! wait_for_server $PORT; then
        kill $SERVER_PID 2>/dev/null || true
        exit 1
    fi
fi

# Run Playwright tests
echo ""
echo "Running: ${PW_CMD}"
echo ""

cleanup() {
    if [ -n "$SERVER_PID" ]; then
        echo ""
        echo -e "${YELLOW}🧹 Cleaning up server process...${NC}"
        kill $SERVER_PID 2>/dev/null || true
    fi
}

trap cleanup EXIT

if eval ${PW_CMD}; then
    echo ""
    echo -e "${GREEN}✅ All Playwright tests passed!${NC}"
    
    # Show report location
    if [ -f "playwright-report/index.html" ]; then
        echo -e "${BLUE}📊 Report available at: playwright-report/index.html${NC}"
        echo "   Open with: npx playwright show-report"
    fi
else
    echo ""
    echo -e "${RED}❌ Playwright tests failed${NC}"
    
    # Show trace location if enabled
    if [ "$TRACE" = true ] && [ -d "test-results" ]; then
        echo -e "${BLUE}🔍 Traces available in: test-results/${NC}"
        echo "   View with: npx playwright show-trace test-results/*/trace.zip"
    fi
    
    exit 1
fi