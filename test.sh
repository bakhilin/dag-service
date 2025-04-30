#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

debug() { 
    echo -e "${BLUE}[DEBUG] $1${NC}"; 
}

info() { 
    echo -e "${GREEN}[INFO] $1${NC}"; 
}

warn() { 
    echo -e "${YELLOW}[WARN] $1${NC}"; 
}

error() { 
    echo -e "${RED}[ERROR] $1${NC}"; exit 1; 
}

# Check required commands
check_commands() {
    local commands=("docker" "curl" "git")
    for cmd in "${commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error "Command '$cmd' not found. Please install it first."
        fi
    done
}

run_service() {
    
    git clone https://github.com/bakhilin/dag-service.git && \
    cd dag-service 

    read -p 'Запустить как Deamon процесс? Y/N' res
    
    if [[ $res = "Y" ]]; then
        ARGS='-d --build'
    else
        ARGS='--build'
    fi 
    
    docker compose up ${ARGS}
}


info 'Check utilities...'
check_commands

info 'Start service and db...'
run_service


