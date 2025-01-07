#!/bin/bash
pytest --cov=foundry --cov-report=html --cov-report=term-missing "$@" 