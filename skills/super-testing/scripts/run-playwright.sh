#!/bin/bash
# run-playwright.sh - Run Playwright E2E tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Running Playwright tests...${NC}"

# Default options
BROWSER="chromium"
HEADED=false
DEBUG=false
UI=false
PROJECT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --browser|-b)
            BROWSER="$2"
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
            UI=true
            shift
            ;;
        --project|-p)
            PROJECT="--project=$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Build command
CMD="npx playwright test"

if [ -n "$PROJECT" ]; then
    CMD="$CMD $PROJECT"
fi

if [ "$HEADED" = true ]; then
    CMD="$CMD --headed"
fi

if [ "$DEBUG" = true ]; then
    CMD="$CMD --debug"
fi

if [ "$UI" = true ]; then
    CMD="npx playwright test --ui"
fi

# Run tests
echo -e "${GREEN}Executing: $CMD${NC}"
eval $CMD

# Check for report
if [ -f "playwright-report/index.html" ]; then
    echo -e "${GREEN}Report available at: playwright-report/index.html${NC}"
    echo -e "${GREEN}Open with: npx playwright show-report${NC}"
fi