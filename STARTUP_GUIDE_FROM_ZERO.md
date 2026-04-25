# 🚀 MageMirror Complete Startup Guide from Zero

**Target Audience**: New developers with zero environment setup  
**Time Required**: 45-60 minutes  
**Difficulty**: Medium  
**Last Updated**: 2026-04-25

---

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] Operating System: Ubuntu 20.04+ / macOS 11+ / Windows 10+ with WSL2
- [ ] Python 3.10, 3.11, or 3.12 installed
- [ ] PostgreSQL 12+ installed and running
- [ ] Git installed
- [ ] Internet connection (for downloading packages and AI models)
- [ ] Gemini API key from Google AI Studio

---

## 🎯 Overview

This guide will walk you through:
1. Installing system dependencies
2. Setting up PostgreSQL database
3. Configuring Python environment
4. Fixing code issues
5. Running the application
6. Testing functionality

**⚠️ IMPORTANT**: This project has critical issues that must be fixed before it can run. This guide includes all necessary fixes.

---

## Step 1: Install System Dependencies

### Ubuntu/Debian:
```bash
# Update package list
sudo apt-get update

# Install Python 3.11 (recommended)
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib libpq-dev

# Install build tools
sudo apt-get install -y gcc make

# Verify installations
python3.11 --version  # Should show: Python 3.11.x
psql --version        # Should show: psql (PostgreSQL) 14.x or higher
```

### macOS:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Verify installations
python3.11 --version
psql --version
```

### Windows (WSL2):
```bash
# Open Ubuntu WSL2 terminal
# Follow Ubuntu/Debian instructions above

# Or use Docker (alternative):
docker pull postgres:14
docker run --name magemirror-db -e POSTGRES_PASSWORD=MageMirror2026 -p 5432:5432 -d postgres:14
```

---

## Step 2: Set Up PostgreSQL Database

### 2.1 Start PostgreSQL Service

```bash
# Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql  # Auto-start on boot

# macOS
brew services start postgresql@14

# Check status
sudo systemctl status postgresql  # Ubuntu
brew services list                # macOS
```

### 2.2 Create Database User and Database

```bash
# Switch to postgres user (Ubuntu/Debian)
sudo -u postgres psql

# Or directly connect (macOS)
psql postgres
```

Inside PostgreSQL shell:
```sql
-- Create user
CREATE USER magemirror_user WITH PASSWORD 'MageMirror2026';

-- Create database
CREATE DATABASE magemirror_db OWNER magemirror_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE magemirror_db TO magemirror_user;

-- Exit
\q
```

### 2.3 Test Connection

```bash
# Test database connection
psql -U magemirror_user -d magemirror_db -h localhost -W
# Enter password: MageMirror2026

# If successful, you'll see:
# magemirror_db=>

# Exit
\q
```

**✅ Checkpoint**: Database is ready if connection succeeds.

---

## Step 3: Clone and Configure Project

### 3.1 Clone Repository

```bash
# Navigate to your workspace
cd /workspace  # Or your preferred directory

# Clone repository (if not already cloned)
git clone https://github.com/MaYeSheng911/MageMirror.git
cd MageMirror

# Verify structure
ls -la
```

### 3.2 Create Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Verify activation (prompt should show (venv))
which python  # Should point to venv/bin/python
```

### 3.3 Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# This will take 5-10 minutes and download ~360MB
# Wait for completion...

# Verify key packages
python -c "import fastapi; import sqlalchemy; from google import genai; from PIL import Image; from rembg import remove; print('✅ All imports successful')"
```

**⚠️ Common Issues**:

**Issue**: `psycopg2` compilation error  
**Fix**: Install PostgreSQL development headers
```bash
# Ubuntu
sudo apt-get install libpq-dev python3-dev

# macOS
brew install postgresql
```

**Issue**: `rembg` model download hangs  
**Fix**: This is normal on first run, wait 5 minutes

---

## Step 4: Get Gemini API Key

### 4.1 Obtain API Key

1. Go to: https://ai.google.dev/
2. Click "Get API Key" or "Get Started"
3. Sign in with your Google account
4. Create a new API key
5. Copy the key (format: `AIza...`)

### 4.2 Create `.env` File

```bash
# Create .env file from template
cp .env.example .env

# Edit .env file
nano .env  # Or use your preferred editor
```

Update the `.env` file:
```bash
# ===== REQUIRED =====
GEMINI_API_KEY=AIzaSyC_YOUR_ACTUAL_API_KEY_HERE

# ===== DATABASE (update if needed) =====
DATABASE_URL=postgresql://magemirror_user:MageMirror2026@localhost:5432/magemirror_db

# ===== PATHS (update to your actual paths) =====
UPLOAD_DIR=/workspace/MageMirror/uploads
TEMPLATES_DIR=/workspace/MageMirror/templates

# ===== SERVER =====
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=INFO
```

**Save and exit** (Ctrl+O, Enter, Ctrl+X in nano)

### 4.3 Load Environment Variables

```bash
# Export environment variables
export $(cat .env | xargs)

# Verify
echo $GEMINI_API_KEY  # Should show your API key
```

**✅ Checkpoint**: API key is set if `echo` shows your key.

---

## Step 5: Fix Critical Code Issues

### 🔴 Issue 1: Database Schema Missing Columns

**Problem**: `clothes` table missing `storage_id` column, `storage` table missing entirely.

**Fix**: Use the fixed schema file

```bash
# Initialize database with FIXED schema
psql -U magemirror_user -d magemirror_db -h localhost -W -f sql/init_tables_fixed.sql

# Enter password: MageMirror2026

# Expected output:
# CREATE TABLE (x9)
# INSERT (x2)
# CREATE INDEX (x6)
# ✅ 数据库初始化完成
```

**Verify tables**:
```bash
psql -U magemirror_user -d magemirror_db -h localhost -W -c "\dt"

# Expected tables:
# users, storage, clothes, images, tags, clothes_tags, outfits, outfit_items, recommendations
```

---

### 🔴 Issue 2: Hardcoded Paths in Code

**Problem**: 6 files have hardcoded `/home/ubuntu/MageMirror/*` paths.

**Fix**: Update files to use environment variables or relative paths.

#### Fix `config/database.py`:
```bash
nano config/database.py
```

**Change**:
```python
# OLD (line 8):
DATABASE_URL = "postgresql://magemirror_user:MageMirror2026@localhost:5432/magemirror_db"

# NEW:
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://magemirror_user:MageMirror2026@localhost:5432/magemirror_db"
)
```

#### Fix `src/main.py`:
```bash
nano src/main.py
```

**Add at top** (after imports):
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))
TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", os.path.join(BASE_DIR, "templates"))
```

**Change line 49**:
```python
# OLD:
directory="/home/ubuntu/MageMirror/uploads"

# NEW:
directory=UPLOAD_DIR
```

**Change line 60**:
```python
# OLD:
directory="/home/ubuntu/MageMirror/templates"

# NEW:
directory=TEMPLATES_DIR
```

#### Fix `src/clothes.py`:
```bash
nano src/clothes.py
```

**Add after imports**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))
```

**Remove old line 18**:
```python
# DELETE:
# UPLOAD_DIR = "/home/ubuntu/MageMirror/uploads"
```

#### Fix utility scripts (optional - only if you plan to use them):

```bash
# Update batch_process_images.py
sed -i 's|/home/ubuntu/MageMirror/uploads|os.getenv("UPLOAD_DIR", "./uploads")|g' src/batch_process_images.py

# Update fix_category.py
sed -i 's|/home/ubuntu/MageMirror/uploads|os.getenv("UPLOAD_DIR", "./uploads")|g' src/fix_category.py

# Update fix_images.py
sed -i 's|/home/ubuntu/MageMirror/uploads|os.getenv("UPLOAD_DIR", "./uploads")|g' src/fix_images.py
```

**✅ Checkpoint**: All hardcoded paths are now using environment variables.

---

### 🔴 Issue 3: Load dotenv in vision.py

**Fix**: Ensure environment variables are loaded

```bash
nano src/ai/vision.py
```

**Add at top** (line 2):
```python
import os
import json
from dotenv import load_dotenv  # ADD THIS

load_dotenv()  # ADD THIS

from google import genai
from PIL import Image
```

---

## Step 6: Create Required Directories

```bash
# Create uploads directory
mkdir -p uploads

# Create static directory (if needed)
mkdir -p src/static

# Set permissions
chmod 755 uploads
chmod 755 src/static

# Verify
ls -ld uploads src/static
```

**✅ Checkpoint**: Directories exist and are writable.

---

## Step 7: Start the Application

### 7.1 Set PYTHONPATH

```bash
# Set Python path to include project root
export PYTHONPATH=/workspace/MageMirror:$PYTHONPATH

# Or use absolute path to your project
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### 7.2 Start FastAPI Server

```bash
# Start server (development mode)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [xxxxx] using StatFiles
# INFO:     Started server process [xxxxx]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**🎉 SUCCESS**: If you see "Application startup complete", the server is running!

---

## Step 8: Test the Application

### 8.1 Test Database Connection

Open a new terminal:
```bash
# Test database endpoint
curl http://localhost:8000/test-db

# Expected output:
# {"status":"success","database":"connected"}
```

**✅ Success**: Database is connected!

---

### 8.2 Test Web Interface

Open your browser:
```
http://localhost:8000/
```

**Expected**: You should see the persons page (用户列表).

---

### 8.3 Test API Endpoints

```bash
# Get API documentation
curl http://localhost:8000/docs

# Or open in browser:
# http://localhost:8000/docs
```

**Expected**: Swagger UI showing all API endpoints.

---

### 8.4 Test File Upload (with curl)

```bash
# Create a test image
convert -size 100x100 xc:red test.jpg  # Requires ImageMagick

# Or download a sample image
wget https://via.placeholder.com/500 -O test.jpg

# Upload image
curl -X POST http://localhost:8000/upload-clothes \
  -F "files=@test.jpg" \
  -F "storage_id=1"

# Expected output:
# {"message":"Upload successful","uploaded":1}
```

---

## Step 9: Verify AI Functionality

### 9.1 Test Gemini Vision

```bash
# Upload an actual clothing image
curl -X POST http://localhost:8000/upload-clothes \
  -F "files=@path/to/real_clothing_image.jpg" \
  -F "storage_id=1"

# Check logs in server terminal
# You should see:
# 🔥 调用 Gemini: /path/to/image
# 🔥 Gemini返回: {"name":"...","category":"..."}
```

### 9.2 Test Background Removal

**Note**: On first run, rembg will download ~180MB AI model. This is normal.

```bash
# Watch server logs when uploading
# You should see model download progress:
# Downloading: u2net.onnx [180MB]
```

---

## Step 10: Production Deployment (Optional)

### 10.1 Update Settings for Production

Edit `.env`:
```bash
DEBUG=False
LOG_LEVEL=WARNING
```

### 10.2 Start with Multiple Workers

```bash
# Stop development server (Ctrl+C)

# Start production server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 10.3 Use Process Manager (Recommended)

Install supervisor or systemd service:

**Systemd service** (`/etc/systemd/system/magemirror.service`):
```ini
[Unit]
Description=MageMirror AI Wardrobe Management
After=network.target postgresql.service

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/workspace/MageMirror
Environment="PATH=/workspace/MageMirror/venv/bin"
Environment="PYTHONPATH=/workspace/MageMirror"
EnvironmentFile=/workspace/MageMirror/.env
ExecStart=/workspace/MageMirror/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable magemirror
sudo systemctl start magemirror
sudo systemctl status magemirror
```

---

## 🎉 Congratulations!

Your MageMirror application is now running!

### Quick Reference Commands:

```bash
# Start server (development)
cd /workspace/MageMirror
source venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH
export $(cat .env | xargs)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Stop server
# Press Ctrl+C

# View logs
# Check terminal output

# Access application
# http://localhost:8000/

# Access API docs
# http://localhost:8000/docs
```

---

## 📚 Common Commands

### Database Management:
```bash
# Connect to database
psql -U magemirror_user -d magemirror_db -h localhost -W

# List tables
\dt

# View clothes
SELECT * FROM clothes;

# View images
SELECT * FROM images;

# Exit
\q
```

### Troubleshooting:
```bash
# Check logs
tail -f /var/log/magemirror.log  # If using systemd

# Test imports
python -c "import fastapi; import sqlalchemy; print('OK')"

# Test environment variables
echo $GEMINI_API_KEY
echo $DATABASE_URL

# Test database connection
psql -U magemirror_user -d magemirror_db -h localhost -W -c "SELECT 1"

# Restart server
# Ctrl+C then re-run uvicorn command
```

---

## 🐛 Known Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution**: Set PYTHONPATH
```bash
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### Issue: "GEMINI_API_KEY not set"
**Solution**: Load .env file
```bash
export $(cat .env | xargs)
```

### Issue: "column 'storage_id' does not exist"
**Solution**: Re-run fixed schema
```bash
psql -U magemirror_user -d magemirror_db -h localhost -W -f sql/init_tables_fixed.sql
```

### Issue: "FileNotFoundError: uploads directory"
**Solution**: Create directory
```bash
mkdir -p uploads
chmod 755 uploads
```

### Issue: "rembg download stuck"
**Solution**: Wait 5-10 minutes or download manually
```bash
python -c "from rembg import remove; import io; remove(b'')"
```

---

## 📊 Performance Optimization

### PostgreSQL Tuning:
```sql
-- Increase shared buffers
ALTER SYSTEM SET shared_buffers = '256MB';

-- Increase work memory
ALTER SYSTEM SET work_mem = '16MB';

-- Reload configuration
SELECT pg_reload_conf();
```

### Python Optimization:
```bash
# Install uvloop for faster async
pip install uvloop

# Use in main.py:
# import uvloop
# uvloop.install()
```

---

## 📝 Next Steps

1. **Customize Configuration**: Edit `.env` for your environment
2. **Add Real Users**: Insert users into database
3. **Upload Clothes**: Use web interface to upload images
4. **Test AI Recognition**: Verify Gemini API responses
5. **Create Outfits**: Use recommendation features
6. **Deploy to Production**: Follow production deployment section
7. **Set Up Monitoring**: Add logging and error tracking
8. **Secure Application**: Add authentication and HTTPS

---

## 📞 Support

- **GitHub Issues**: https://github.com/MaYeSheng911/MageMirror/issues
- **Documentation**: See `DEPENDENCIES_ANALYSIS.md`
- **API Reference**: http://localhost:8000/docs (when running)

---

**✅ Startup Guide Complete**  
**Time Spent**: ~45-60 minutes  
**Status**: Application fully functional  
**Version**: 1.1 (Fixed)

**Happy Coding! 🎉**
