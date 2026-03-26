#!/bin/bash
# run-pytest.sh - Run Python tests with pytest and coverage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running pytest with coverage...${NC}"

# Default options
COVERAGE=true
VERBOSE=false
PARALLEL=false
TEST_PATH="tests/"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cov)
            COVERAGE=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        *)
            TEST_PATH="$1"
            shift
            ;;
    esac
done

# Build pytest command
CMD="pytest"

if [ "$VERBOSE" = true ]; then
    CMD="$CMD -v"
fi

if [ "$PARALLEL" = true ]; then
    CMD="$CMD -n auto"
fi

if [ "$COVERAGE" = true ]; then
    CMD="$CMD --cov=src --cov-report=term-missing --cov-report=html:htmlcov"
fi

CMD="$CMD $TEST_PATH"

# Run tests
echo -e "${GREEN}Executing: $CMD${NC}"
eval $CMD

# Print coverage report location
if [ "$COVERAGE" = true ] && [ -d "htmlcov" ]; then
    echo -e "${GREEN}Coverage report: htmlcov/index.html${NC}"
fi