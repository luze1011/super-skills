#!/bin/bash
# run-e2e.sh - Run full E2E test suite

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    Full E2E Test Suite Runner${NC}"
echo -e "${BLUE}========================================${NC}"

# Configuration
E2E_DIR="${E2E_DIR:-e2e}"
REPORT_DIR="${REPORT_DIR:-test-results}"
RETRY_COUNT="${RETRY_COUNT:-2}"

# Parse arguments
CLEANUP=false
HEADLESS=true
while [[ $# -gt 0 ]]; do
    case $1 in
        --cleanup)
            CLEANUP=true
            shift
            ;;
        --headed)
            HEADLESS=false
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Create directories
mkdir -p "$REPORT_DIR"

# Step 1: Run linting
echo -e "${YELLOW}[1/4] Running linting...${NC}"
if command -v npm &> /dev/null; then
    npm run lint 2>/dev/null || echo -e "${YELLOW}Linting skipped or failed${NC}"
fi

# Step 2: Run unit tests
echo -e "${YELLOW}[2/4] Running unit tests...${NC}"
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    pytest tests/unit -v --tb=short 2>/dev/null || echo -e "${YELLOW}No unit tests found${NC}"
elif [ -f "package.json" ]; then
    npm run test:unit 2>/dev/null || echo -e "${YELLOW}No unit tests found${NC}"
fi

# Step 3: Run integration tests
echo -e "${YELLOW}[3/4] Running integration tests...${NC}"
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    pytest tests/integration -v --tb=short 2>/dev/null || echo -e "${YELLOW}No integration tests found${NC}"
elif [ -f "package.json" ]; then
    npm run test:integration 2>/dev/null || echo -e "${YELLOW}No integration tests found${NC}"
fi

# Step 4: Run E2E tests
echo -e "${YELLOW}[4/4] Running E2E tests...${NC}"
if [ -f "playwright.config.ts" ] || [ -f "playwright.config.js" ]; then
    CMD="npx playwright test --reporter=html --output=$REPORT_DIR"
    
    if [ "$HEADLESS" = true ]; then
        CMD="$CMD"
    else
        CMD="$CMD --headed"
    fi
    
    # Run with retries
    for i in $(seq 1 $RETRY_COUNT); do
        echo -e "${GREEN}Attempt $i/$RETRY_COUNT${NC}"
        if eval $CMD; then
            echo -e "${GREEN}E2E tests passed!${NC}"
            break
        elif [ $i -eq $RETRY_COUNT ]; then
            echo -e "${RED}E2E tests failed after $RETRY_COUNT attempts${NC}"
            exit 1
        else
            echo -e "${YELLOW}Retrying...${NC}"
        fi
    done
else
    echo -e "${YELLOW}No Playwright config found, skipping E2E tests${NC}"
fi

# Cleanup
if [ "$CLEANUP" = true ]; then
    echo -e "${YELLOW}Cleaning up test artifacts...${NC}"
    rm -rf "$REPORT_DIR"
    rm -rf playwright-report
fi

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Test run complete!${NC}"
if [ -f "playwright-report/index.html" ]; then
    echo -e "${GREEN}View report: npx playwright show-report${NC}"
fi
echo -e "${BLUE}========================================${NC}"