# 🚀 MageMirror Quick Start

## Step 1: Initialize Default Storage Data

```bash
psql -U magemirror_user -d magemirror_db -h localhost -W -f sql/insert_default_storage.sql
```

**Password**: `MageMirror2026`

---

## Step 2: Start Server (if not running)

```bash
cd /workspace/MageMirror
export PYTHONPATH=$(pwd):$PYTHONPATH
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Step 3: Test

Open browser: **http://localhost:8000**

### Navigation Flow:
1. Click "我" → Goes to `/storage/1`
2. Should see "默认柜子" box
3. Click blue "+" button → Goes to `/upload`
4. Click "默认柜子" → Goes to clothes page

---

## Quick Tests

### Test Storage API:
```bash
curl http://localhost:8000/storage-units/1
```

**Expected**: JSON with storage list

### Test Create Storage:
```bash
curl http://localhost:8000/storage/new/1
```

**Expected**: "storage already exists" or "storage created"

### Test Upload Page:
```bash
curl http://localhost:8000/upload
```

**Expected**: HTML upload page

---

## ✅ All Fixed!

- ✅ Storage page shows units
- ✅ Upload button visible
- ✅ All routes working
- ✅ Complete navigation flow

---

**See**: `FIXES_APPLIED.md` for full details
