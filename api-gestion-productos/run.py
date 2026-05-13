#!/usr/bin/env python3
"""Script to run the Food Inventory API."""

import sys
from pathlib import Path

# Add src to path
BASE_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Food Inventory API...")
    print("📚 API: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
