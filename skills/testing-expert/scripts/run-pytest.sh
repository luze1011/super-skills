#!/bin/bash
# run-pytest.sh - Run pytest with standard configuration
# Usage: ./run-pytest.sh [pytest_options] [test_path]
#
# Examples:
#   ./run-pytest.sh                    # Run all tests
#   ./run-pytest.sh tests/unit         # Run unit tests only
#   ./run-pytest.sh -v --cov=app       # Verbose with coverage
#   ./run-pytest.sh -x -k "test_user"  # Stop on first failure, filter by name

set -e

# Default configuration
TEST_PATH="${1:-tests}"
COVERAGE_THRESHOLD="${COVERAGE_THRESHOLD:-80}"
PARALLEL="${PARALLEL:-auto}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧪 Running pytest tests...${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Install with: pip install pytest pytest-cov pytest-xdist"
    exit 1
fi

# Build pytest command
PYTEST_CMD="pytest ${TEST_PATH}"

# Add common options if not already specified
if [[ "$*" != *"--cov"* ]]; then
    PYTEST_CMD="${PYTEST_CMD} --cov=. --cov-report=term-missing --cov-report=html"
fi

if [[ "$*" != *"-n"* ]] && [[ "$*" != *"-j"* ]]; then
    PYTEST_CMD="${PYTEST_CMD} -n ${PARALLEL}"
fi

# Add verbosity if not specified
if [[ "$*" != *"-v"* ]] && [[ "$*" != *"--verbose"* ]]; then
    PYTEST_CMD="${PYTEST_CMD} -v"
fi

# Run tests
echo "Running: ${PYTEST_CMD}"
echo ""

if eval ${PYTEST_CMD}; then
    echo ""
    echo -e "${GREEN}✅ All tests passed!${NC}"
    
    # Check coverage threshold
    if [[ -f ".coverage" ]]; then
        COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
        if (( $(echo "${COVERAGE} < ${COVERAGE_THRESHOLD}" | bc -l) )); then
            echo -e "${YELLOW}⚠️  Coverage (${COVERAGE}%) is below threshold (${COVERAGE_THRESHOLD}%)${NC}"
        else
            echo -e "${GREEN}📊 Coverage: ${COVERAGE}% (threshold: ${COVERAGE_THRESHOLD}%)${NC}"
        fi
    fi
else
    echo ""
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
fi