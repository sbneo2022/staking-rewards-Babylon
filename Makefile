# Makefile for running the Streamlit app and additional commands

# Default target
.PHONY: run  help

run:
	streamlit run cryptometric_dashboard.py

help:
	@echo "Makefile Commands:"
	@echo "  make run   - Run the Streamlit app"
	@echo "  make help  - Display this help message"