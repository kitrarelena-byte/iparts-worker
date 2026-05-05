#!/bin/bash

playwright install chromium
uvicorn worker:app --host 0.0.0.0 --port $PORT
