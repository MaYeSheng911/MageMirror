# MageMirror Dependencies Analysis

## 📋 Complete Python Import Analysis

### Analysis Date: 2026-04-25
### Python Version Requirement: 3.10+ (Tested: 3.10, 3.11, 3.12)

---

## 1. 📦 Detected Python Files (15 files)

### Core Business Logic:
1. `src/main.py` - FastAPI application entry point
2. `src/clothes.py` - Clothes management API routes
3. `src/recommend.py` - AI outfit recommendation

### AI Module:
4. `src/ai/vision.py` - Gemini AI vision integration
5. `src/ai/image_processor.py` - Image preprocessing & background removal
6. `src/ai/label_normalizer.py` - Label standardization (no external deps)

### Database:
7. `config/database.py` - PostgreSQL connection config
8. `src/config/database.py` - Config duplicate

### Utility Scripts:
9. `src/batch_process_images.py` - Batch image processing
10. `src/fix_category.py` - Fix unknown categories
11. `src/fix_images.py` - Fix image paths

### Init Files:
12-15. `__init__.py` files (no imports)

---

## 2. 🔍 Detected Imports by File

### `src/main.py`
```python
from fastapi import FastAPI, Request
from sqlalchemy import text
from config.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.clothes import router as clothes_router
```

### `src/clothes.py`
```python
from fastapi import APIRouter, UploadFile, File, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal
from src.ai.vision import analyze_clothes
from src.ai.image_processor import process_image
from typing import List
import os
import uuid
from datetime import datetime
```

### `src/recommend.py`
```python
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal
from google import genai
import os
import json
```

### `src/ai/vision.py`
```python
import os
import json
from google import genai
from PIL import Image
```

### `src/ai/image_processor.py`
```python
from rembg import remove
from PIL import Image
import io
import os
```

### `src/ai/label_normalizer.py`
```python
# No external imports - pure Python
```

### `config/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
```

### `src/fix_category.py`
```python
import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal
from ai.vision import analyze_clothes
```

### `src/fix_images.py`
```python
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal
import os
```

### `src/batch_process_images.py`
```python
import os
from ai.image_processor import process_image
```

---

## 3. 📚 Required External Packages

### Web Framework (3 packages):
- **fastapi** - Modern web framework
- **uvicorn** - ASGI server
- **python-multipart** - File upload support

### Template Engine (2 packages):
- **jinja2** - HTML templating
- **markupsafe** - Safe string rendering

### Database (3 packages):
- **sqlalchemy** - ORM framework
- **psycopg2-binary** - PostgreSQL driver
- **greenlet** - Async support for SQLAlchemy

### AI & Vision (3 packages):
- **google-genai** - Gemini AI SDK
- **pillow** - Image manipulation
- **rembg** - Background removal AI

### Image Processing (4 packages):
- **numpy** - Numerical arrays
- **opencv-python-headless** - Computer vision (no GUI)
- **onnxruntime** - AI model inference
- **scikit-image** - Image processing algorithms

### Utilities (1 package):
- **python-dotenv** - Environment variable management

### ASGI Dependencies (4 packages):
- **httptools** - Fast HTTP parsing
- **pyyaml** - YAML support
- **watchfiles** - File change detection
- **websockets** - WebSocket support

### Core Dependencies (5 packages):
- **typing-extensions** - Extended type hints
- **anyio** - Async I/O abstraction
- **starlette** - ASGI framework (FastAPI dependency)
- **pydantic** - Data validation
- **pydantic-core** - Pydantic core functionality

---

## 4. 📊 Package Version Rationale

### FastAPI Ecosystem:
- **fastapi 0.115.0** - Latest stable with Python 3.12 support
- **uvicorn 0.32.0** - Compatible with FastAPI 0.115+
- **starlette 0.41.2** - Required by FastAPI 0.115
- **pydantic 2.9.2** - FastAPI 0.115+ requires Pydantic v2

### Database:
- **sqlalchemy 2.0.35** - Modern async support, type hints
- **psycopg2-binary 2.9.10** - Latest stable PostgreSQL driver
- **greenlet 3.1.1** - Required for SQLAlchemy async operations

### AI Vision:
- **google-genai 1.5.1** - Latest Gemini SDK (2024+)
- **pillow 11.0.0** - Latest with Python 3.12 support
- **rembg 2.0.59** - Latest background removal

### Image Processing:
- **numpy 1.26.4** - Compatible with Python 3.12, rembg, opencv
- **opencv-python-headless 4.10.0.84** - Latest without GUI deps
- **onnxruntime 1.20.1** - Latest with Python 3.12 support
- **scikit-image 0.24.0** - Latest stable

---

## 5. ⚠️ Known Compatibility Constraints

### Python Version Constraints:
- **Minimum**: Python 3.10 (for match/case, improved type hints)
- **Recommended**: Python 3.11+ (better performance)
- **Tested**: Python 3.12.11 (fully compatible)
- **Maximum**: Python 3.13 (may have limited package support)

### PostgreSQL Version:
- **Minimum**: PostgreSQL 12+
- **Recommended**: PostgreSQL 14+ or 15+
- **psycopg2-binary**: Supports PostgreSQL 9.6 - 16

### Critical Version Locks:
1. **FastAPI 0.115.0** requires **Pydantic 2.x** (breaking change from v1)
2. **SQLAlchemy 2.x** has different async syntax than 1.x
3. **rembg 2.0.59** requires specific **numpy** and **onnxruntime** versions
4. **opencv-python-headless** conflicts with **opencv-python** (don't install both)

---

## 6. 🔧 Installation Instructions

### Quick Install:
```bash
pip install -r requirements.txt
```

### Virtual Environment (Recommended):
```bash
# Create virtual environment
python3.10 -m venv venv  # or python3.11, python3.12

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### With Conda:
```bash
conda create -n magemirror python=3.11
conda activate magemirror
pip install -r requirements.txt
```

### Docker Installation:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 7. 🧪 Testing Installation

### Basic Test:
```bash
python3 -c "import fastapi; import sqlalchemy; import PIL; from google import genai; from rembg import remove; print('✅ All imports successful')"
```

### Detailed Test:
```python
import sys
print(f"Python: {sys.version}")

import fastapi
print(f"FastAPI: {fastapi.__version__}")

import sqlalchemy
print(f"SQLAlchemy: {sqlalchemy.__version__}")

import PIL
print(f"Pillow: {PIL.__version__}")

from google import genai
print(f"Google GenAI: OK")

from rembg import remove
print(f"Rembg: OK")
```

---

## 8. 🚨 Common Installation Issues

### Issue 1: psycopg2 compilation error
**Solution**: Use `psycopg2-binary` instead of `psycopg2`
```bash
pip install psycopg2-binary==2.9.10
```

### Issue 2: rembg download models on first run
**Note**: rembg will download ~180MB AI model on first use
```bash
# Pre-download models
python3 -c "from rembg import remove; print('Models downloaded')"
```

### Issue 3: OpenCV conflicts
**Solution**: Only install opencv-python-headless
```bash
pip uninstall opencv-python  # Remove GUI version
pip install opencv-python-headless==4.10.0.84
```

### Issue 4: numpy version conflicts
**Solution**: Install numpy first
```bash
pip install numpy==1.26.4
pip install -r requirements.txt
```

### Issue 5: Gemini API authentication
**Solution**: Set environment variable
```bash
export GEMINI_API_KEY="your_api_key_here"
```

---

## 9. 📝 Environment Variables Required

### Required:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Database (if not using default):
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Optional:
```bash
UPLOAD_DIR=/path/to/uploads
DEBUG=True
LOG_LEVEL=INFO
```

---

## 10. 🔄 Updating Dependencies

### Check for updates:
```bash
pip list --outdated
```

### Update specific package:
```bash
pip install --upgrade package_name
```

### Update all (careful):
```bash
pip install --upgrade -r requirements.txt
```

### Freeze current versions:
```bash
pip freeze > requirements.lock
```

---

## 11. 📦 Package Size Estimates

| Package Category | Size | Download Time (10 Mbps) |
|-----------------|------|-------------------------|
| FastAPI + Uvicorn | ~15 MB | ~12 seconds |
| SQLAlchemy + psycopg2 | ~8 MB | ~6 seconds |
| Google GenAI | ~5 MB | ~4 seconds |
| Pillow | ~3 MB | ~2 seconds |
| rembg + models | ~200 MB | ~160 seconds |
| numpy + opencv | ~50 MB | ~40 seconds |
| onnxruntime | ~30 MB | ~24 seconds |
| **Total** | **~310 MB** | **~4-5 minutes** |

---

## 12. 🎯 Production Recommendations

### Security:
1. Pin all dependency versions (already done in requirements.txt)
2. Run `pip audit` to check for vulnerabilities
3. Use virtual environments
4. Don't commit `.env` files

### Performance:
1. Use `uvicorn` with `--workers` for production
2. Enable PostgreSQL connection pooling
3. Cache Gemini API responses when possible
4. Optimize image sizes before upload

### Monitoring:
```bash
# Add these for production:
pip install prometheus-client==0.21.0
pip install sentry-sdk==2.17.0
```

---

## 13. 🔍 Dependency Tree (Simplified)

```
MageMirror
├── FastAPI (Web Framework)
│   ├── Starlette (ASGI)
│   ├── Pydantic (Validation)
│   └── Uvicorn (Server)
├── SQLAlchemy (ORM)
│   ├── psycopg2-binary (PostgreSQL)
│   └── greenlet (Async)
├── Gemini AI
│   └── google-genai (SDK)
├── Image Processing
│   ├── Pillow (Manipulation)
│   ├── rembg (Background Removal)
│   │   ├── onnxruntime (AI Models)
│   │   ├── opencv-python-headless (CV)
│   │   ├── numpy (Arrays)
│   │   └── scikit-image (Processing)
└── Utilities
    ├── python-dotenv (Env Vars)
    └── python-multipart (File Uploads)
```

---

## 14. ✅ Verification Checklist

After installation, verify:

- [ ] Python version is 3.10+
- [ ] All packages install without errors
- [ ] PostgreSQL is installed and accessible
- [ ] Gemini API key is set in environment
- [ ] Upload directory exists and is writable
- [ ] Test imports work: `python3 -c "import fastapi, sqlalchemy, PIL, rembg"`
- [ ] Database connection works: Test `/test-db` endpoint
- [ ] Rembg models are downloaded (first run)
- [ ] FastAPI server starts: `uvicorn src.main:app --reload`

---

## 15. 📞 Support & References

### Official Documentation:
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Gemini API: https://ai.google.dev/docs
- Pillow: https://pillow.readthedocs.io/
- rembg: https://github.com/danielgatis/rembg

### Package Registries:
- PyPI: https://pypi.org/
- Conda: https://anaconda.org/

---

**Generated**: 2026-04-25  
**Python Version**: 3.10+ | 3.11 | 3.12  
**Compatibility**: Production-ready ✅
