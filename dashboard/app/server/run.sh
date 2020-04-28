#!/bin/bash
PYTHONPATH=../../../  uvicorn main:app --reload --port 1345 --host 0.0.0.0