# 🚀 MageMirror Deployment Quick Start

## ⚠️ CRITICAL: Project Cannot Run Without Fixes

This project has **5 critical issues** that prevent it from running. This document provides quick fixes.

---

## 📋 Issue Summary

| # | Issue | Severity | Fix Time |
|---|-------|----------|----------|
| 1 | Missing database columns/tables | 🔴 Critical | 5 min |
| 2 | No environment variables | 🔴 Critical | 5 min |
| 3 | Hardcoded file paths | 🔴 Critical | 10 min |
| 4 | Database credentials in code | 🔴 Critical | 5 min |
| 5 | Missing required directories | ⚠️ Warning | 2 min |

**Total Fix Time**: ~30 minutes

---

## 🎯 Quick Fix (Automated)

### Option 1: Use Fix Script (Recommended)

```bash
# 1. Run automated fix script
./fix_hardcoded_paths.sh

# 2. Edit .env and add your Gemini API key
nano .env
# Add: GEMINI_API_KEY=your_actual_key_here

# 3. Initialize database with FIXED schema
psql -U magemirror_user -d magemirror_db -h localhost -W -f sql/init_tables_fixed.sql

# 4. Load environment and start server
export $(cat .env | xargs)
export PYTHONPATH=$(pwd):$PYTHONPATH
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Done! Server should be running on http://localhost:8000**

---

## 📚 Full Documentation

For detailed instructions, see:

- **`STARTUP_GUIDE_FROM_ZERO.md`** - Complete step-by-step guide (45-60 min)
- **`STARTUP_VERIFICATION_REPORT.md`** - Detailed issue analysis
- **`DEPENDENCIES_ANALYSIS.md`** - Full dependency documentation

---

## 🔍 What Each Fix Does

### 1. Database Schema Fix
**File**: `sql/init_tables_fixed.sql`  
**Changes**:
- Adds missing `storage` table
- Adds `storage_id` column to `clothes` table
- Adds proper foreign key constraints
- Creates performance indexes

### 2. Environment Variables
**File**: `.env` (created from `.env.example`)  
**Required variables**:
```bash
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
UPLOAD_DIR=/path/to/uploads
TEMPLATES_DIR=/path/to/templates
```

### 3. Path Fixes
**Modified files**:
- `config/database.py` - Use environment variables
- `src/main.py` - Dynamic paths for uploads/templates
- `src/clothes.py` - Dynamic upload directory
- `src/ai/vision.py` - Load dotenv

### 4. Security Improvements
- Remove hardcoded database credentials
- Load passwords from environment
- Don't commit `.env` to Git

### 5. Directory Creation
```bash
uploads/      # For uploaded images
src/static/   # For static assets
```

---

## 📦 Installation Requirements

### System Dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install python3.11 postgresql-14 libpq-dev

# macOS
brew install python@3.11 postgresql@14
```

### Python Dependencies:
```bash
pip install -r requirements.txt
```

**28 packages**, ~360MB total

---

## 🔐 Get Gemini API Key

1. Go to: https://ai.google.dev/
2. Sign in with Google
3. Click "Get API Key"
4. Copy key (format: `AIza...`)
5. Add to `.env`: `GEMINI_API_KEY=AIza...`

---

## ✅ Verification Checklist

Before running, verify:

- [ ] PostgreSQL is installed and running
- [ ] Database `magemirror_db` exists
- [ ] User `magemirror_user` exists with correct password
- [ ] Python 3.10+ is installed
- [ ] Virtual environment is activated
- [ ] All packages installed: `pip install -r requirements.txt`
- [ ] `.env` file exists with GEMINI_API_KEY
- [ ] Database initialized with `init_tables_fixed.sql`
- [ ] `uploads/` directory exists
- [ ] PYTHONPATH is set

---

## 🧪 Testing

### Test 1: Database Connection
```bash
curl http://localhost:8000/test-db

# Expected: {"status":"success","database":"connected"}
```

### Test 2: Web Interface
```bash
# Open in browser
http://localhost:8000/

# Expected: Persons page loads
```

### Test 3: API Documentation
```bash
# Open in browser
http://localhost:8000/docs

# Expected: Swagger UI with all endpoints
```

### Test 4: File Upload
```bash
curl -X POST http://localhost:8000/upload-clothes \
  -F "files=@test.jpg" \
  -F "storage_id=1"

# Expected: {"message":"Upload successful","uploaded":1}
```

---

## 🐛 Common Errors

### Error: "GEMINI_API_KEY not set"
**Fix**: Add key to `.env` and export:
```bash
echo "GEMINI_API_KEY=your_key" >> .env
export $(cat .env | xargs)
```

### Error: "column storage_id does not exist"
**Fix**: Use fixed schema:
```bash
psql -U magemirror_user -d magemirror_db -h localhost -W -f sql/init_tables_fixed.sql
```

### Error: "ModuleNotFoundError: No module named 'src'"
**Fix**: Set PYTHONPATH:
```bash
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### Error: "FileNotFoundError: uploads"
**Fix**: Create directory:
```bash
mkdir -p uploads && chmod 755 uploads
```

---

## 📞 Support

- **Full Guide**: See `STARTUP_GUIDE_FROM_ZERO.md`
- **Issue Report**: See `STARTUP_VERIFICATION_REPORT.md`
- **Dependencies**: See `DEPENDENCIES_ANALYSIS.md`
- **GitHub**: https://github.com/MaYeSheng911/MageMirror/issues

---

## 🎉 Success Indicators

When running correctly, you should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

And tests should pass:
- ✅ Database test returns "connected"
- ✅ Homepage loads at http://localhost:8000
- ✅ API docs available at http://localhost:8000/docs
- ✅ File upload works without errors

---

**Ready to Start?**

```bash
# Quick start command:
./fix_hardcoded_paths.sh && \
nano .env && \
psql -U magemirror_user -d magemirror_db -h localhost -W -f sql/init_tables_fixed.sql && \
export $(cat .env | xargs) && \
export PYTHONPATH=$(pwd):$PYTHONPATH && \
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Good luck! 🚀**
