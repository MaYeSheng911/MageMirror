# Storage Units Database Fix - Manual Execution Guide

## 📋 Problem Description

**Error**: `relation "storage_units" does not exist`

**Root Cause**: The `storage_units` table was never created in the database, but the code was trying to query it.

---

## 🔧 What This Fix Does

1. ✅ Creates the `storage_units` table with proper schema
2. ✅ Inserts default storage data for 3 persons (我, 妈, 爸)
3. ✅ Updates all API endpoints to use `storage_units` table
4. ✅ Updates database configuration to use `mage_mirror` database
5. ✅ Restarts the FastAPI server with new changes

---

## 🚀 Option 1: Automated Fix (Recommended)

Run the automated script:

```bash
cd /workspace/MageMirror
./apply_storage_fix.sh
```

This will execute all steps automatically.

---

## 🔨 Option 2: Manual Execution

### Step 1: Create storage_units table

```bash
psql -U magemirror_user -d mage_mirror -h localhost -W \
  -f sql/create_storage_tables.sql
```

**Password**: `MageMirror2026`

**Expected Output**:
```
DROP TABLE
CREATE TABLE
CREATE INDEX
 status
--------
 storage_units table created successfully
```

### Step 2: Insert default storage data

```bash
psql -U magemirror_user -d mage_mirror -h localhost -W \
  -f sql/insert_default_storage.sql
```

**Expected Output**:
```
INSERT 0 1
INSERT 0 1
INSERT 0 1
 id | person_id |    name    | location |       created_at
----+-----------+------------+----------+------------------------
  1 |         1 | 默认柜子   | 卧室     | 2026-04-25 10:30:00
  2 |         2 | 默认柜子   | 卧室     | 2026-04-25 10:30:01
  3 |         3 | 默认柜子   | 卧室     | 2026-04-25 10:30:02
```

### Step 3: Verify data

```bash
psql -U magemirror_user -d mage_mirror -h localhost -W \
  -c "SELECT * FROM storage_units;"
```

### Step 4: Stop existing FastAPI server (if running)

```bash
# Find the process ID
ps aux | grep "uvicorn src.main:app" | grep -v grep

# Kill the process (replace <PID> with actual process ID)
kill <PID>
```

### Step 5: Start FastAPI server

```bash
cd /workspace/MageMirror
export PYTHONPATH=$(pwd):$PYTHONPATH
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Or run in background:**

```bash
cd /workspace/MageMirror
export PYTHONPATH=$(pwd):$PYTHONPATH
nohup uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 > server.log 2>&1 &
echo "Server PID: $!"
```

---

## 🧪 Testing the Fix

### Test 1: Check API endpoint

```bash
curl http://localhost:8000/storage-units/1
```

**Expected Response**:
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "默认柜子",
      "location": "卧室",
      "created_at": "2026-04-25 10:30:00"
    }
  ]
}
```

### Test 2: Check storage page

Open in browser: `http://localhost:8000/storage/1`

**Expected**: Page loads with storage list (not empty)

### Test 3: Check auto-creation endpoint

```bash
curl http://localhost:8000/storage/new/4
```

**Expected**: Creates default storage for person_id=4

---

## 📁 Files Changed

### New Files Created (2):
1. **sql/create_storage_tables.sql** - Creates `storage_units` table
2. **apply_storage_fix.sh** - Automated execution script

### Files Modified (4):
1. **sql/insert_default_storage.sql** - Changed `storage` → `storage_units`
2. **src/storage.py** - All 3 endpoints updated to use `storage_units`
3. **config/database.py** - Database name updated to `mage_mirror`
4. **src/config/database.py** - Database credentials updated

---

## 📊 Database Schema

### storage_units table structure:

```sql
CREATE TABLE storage_units (
    id SERIAL PRIMARY KEY,              -- Auto-increment ID
    person_id INTEGER NOT NULL,         -- Owner's person ID
    name TEXT NOT NULL,                 -- Storage unit name (e.g., "默认柜子")
    location TEXT DEFAULT '',           -- Location (e.g., "卧室")
    description TEXT DEFAULT '',        -- Optional description
    created_at TIMESTAMP DEFAULT NOW()  -- Creation timestamp
);

CREATE INDEX idx_storage_units_person_id ON storage_units(person_id);
```

---

## 🐛 Troubleshooting

### Issue 1: "psql: command not found"

**Solution**: Install PostgreSQL client
```bash
apt-get update && apt-get install -y postgresql-client
```

### Issue 2: "connection refused"

**Solution**: Start PostgreSQL server
```bash
sudo service postgresql start
# or
pg_ctl -D /path/to/data start
```

### Issue 3: "FATAL: password authentication failed"

**Solution**: Check credentials in config files
- Username: `magemirror_user`
- Password: `MageMirror2026`
- Database: `mage_mirror`

### Issue 4: "duplicate key value violates unique constraint"

**Solution**: Data already exists, safe to ignore. Or drop and recreate:
```sql
TRUNCATE storage_units RESTART IDENTITY CASCADE;
```
Then re-run `insert_default_storage.sql`

### Issue 5: Server won't start

**Check logs**:
```bash
tail -f server.log
```

**Common fixes**:
- Port 8000 already in use: `lsof -ti:8000 | xargs kill`
- Import errors: `pip install -r requirements.txt`
- Database connection: Check `config/database.py`

---

## ✅ Success Criteria

After completing the fix, verify:

- ✅ No database errors in server logs
- ✅ `/storage-units/{person_id}` returns data (not empty)
- ✅ `/storage/new/{person_id}` works without errors
- ✅ Storage page displays storage list
- ✅ Upload button navigates correctly

---

## 📞 Support

If you encounter issues:

1. Check server logs: `tail -f server.log`
2. Check database connectivity: `psql -U magemirror_user -d mage_mirror -h localhost`
3. Verify table exists: `\dt storage_units`
4. Check data: `SELECT * FROM storage_units;`

---

## 📝 Summary

**Problem**: Table `storage_units` didn't exist  
**Solution**: Created table + inserted default data + updated code  
**Result**: Storage functionality now works end-to-end  

**Estimated Time**: 2-3 minutes  
**Complexity**: Low (just SQL execution + server restart)
