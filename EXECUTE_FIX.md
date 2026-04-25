# 🚀 Storage Units Fix - Quick Execution Guide

## ⚡ Quick Start (One Command)

```bash
cd /workspace/MageMirror && ./apply_storage_fix.sh
```

This script will:
1. ✅ Create `storage_units` table
2. ✅ Insert default data for 3 persons
3. ✅ Verify database state
4. ✅ Restart FastAPI server

---

## 📋 Prerequisites

- PostgreSQL server running
- Database `mage_mirror` exists
- User `magemirror_user` with password `MageMirror2026`

---

## 🔨 Manual Execution (If Automated Script Fails)

### Step 1: Create Table
```bash
export PGPASSWORD='MageMirror2026'
psql -U magemirror_user -d mage_mirror -h localhost \
  -f sql/create_storage_tables.sql
```

### Step 2: Insert Data
```bash
export PGPASSWORD='MageMirror2026'
psql -U magemirror_user -d mage_mirror -h localhost \
  -f sql/insert_default_storage.sql
```

### Step 3: Start Server
```bash
cd /workspace/MageMirror
export PYTHONPATH=$(pwd):$PYTHONPATH
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Verify Success

Test the API:
```bash
curl http://localhost:8000/storage-units/1
```

Expected response:
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "默认柜子",
      "location": "卧室",
      "created_at": "..."
    }
  ]
}
```

---

## 📖 More Information

- Full manual: `STORAGE_FIX_MANUAL.md`
- Complete log: `STORAGE_FIX_LOG.md`
- Automated script: `apply_storage_fix.sh`

---

## ⏱️ Estimated Time: 2 minutes
