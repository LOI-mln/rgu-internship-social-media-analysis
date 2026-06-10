#!/bin/bash

# RGU Internship Social Media Analysis - Demo Execution Script
# Author: Milan Loi
# This script launches key modules of the project for demonstration.

# Ensure we are in the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Check if the virtual environment exists and activate it
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Error: Virtual environment '.venv' not found. Please create it and install dependencies."
    exit 1
fi

clear

show_menu() {
    echo "================================================================="
    echo "          RGU INTERNSHIP DEMO EXECUTION CONTROL PANEL            "
    echo "================================================================="
    echo " Please select an execution module to run:"
    echo ""
    echo " 1) Start the Streamlit Visual Dashboard"
    echo "    (Launches the web UI on http://localhost:8501)"
    echo ""
    echo " 2) Run Multimodal Meme Alignment Analysis (CLIP)"
    echo "    (Evaluates text-image semantic similarity on political memes)"
    echo ""
    echo " 3) Compute Discursive Polarization Index (Perspective API)"
    echo "    (Quantifies tribalism based on in-group/out-group vocabulary)"
    echo ""
    echo " 4) Compute Cross-Platform Network Modularity (Louvain)"
    echo "    (Synthesizes YouTube/Instagram/Twitter interaction graphs)"
    echo ""
    echo " 5) Quit"
    echo "================================================================="
}

while true; do
    show_menu
    read -p "Enter choice [1-5]: " choice
    echo ""
    
    case $choice in
        1)
            echo "Starting Streamlit dashboard..."
            echo "Press Ctrl+C in this terminal to stop the server."
            streamlit run app.py
            ;;
        2)
            echo "Running CLIP multimodal analysis evaluation..."
            python src/nlp/evaluate_alignment.py
            ;;
        3)
            echo "Computing Polarization Index..."
            python src/nlp/week6_polarization.py
            ;;
        4)
            echo "Synthesizing cross-platform graph and computing Louvain modularity..."
            python src/network/cross_platform_network.py
            ;;
        5)
            echo "Exiting control panel. Goodbye."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select between 1 and 5."
            ;;
    esac
    
    echo ""
    read -p "Press [Enter] key to return to the menu..." temp
    clear
done
