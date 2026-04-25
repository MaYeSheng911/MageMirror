#!/bin/bash

# =========================================================
# Apply Storage Units Database Fix
# =========================================================
# This script:
# 1. Creates the storage_units table
# 2. Inserts default storage data
# 3. Restarts the FastAPI server
# =========================================================

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         MageMirror Storage Units - Database Fix               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
DB_NAME="mage_mirror"
DB_USER="magemirror_user"
DB_HOST="localhost"
DB_PORT="5432"
export PGPASSWORD="MageMirror2026"

echo "📋 Configuration:"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo "   Host: $DB_HOST:$DB_PORT"
echo ""

# Step 1: Create storage_units table
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Creating storage_units table"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -f sql/create_storage_tables.sql; then
    echo "✅ storage_units table created successfully"
else
    echo "❌ Failed to create storage_units table"
    exit 1
fi

echo ""

# Step 2: Insert default storage data
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Inserting default storage data"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -f sql/insert_default_storage.sql; then
    echo "✅ Default storage data inserted successfully"
else
    echo "❌ Failed to insert default storage data"
    exit 1
fi

echo ""

# Step 3: Verify data
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Verifying data"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -c "SELECT COUNT(*) as total_storage_units FROM storage_units;"

echo ""

# Step 4: Show storage units
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Storage units created:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -c "SELECT id, person_id, name, location FROM storage_units ORDER BY person_id;"

echo ""

# Step 5: Check for running FastAPI server
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Checking FastAPI server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

UVICORN_PID=$(ps aux | grep "uvicorn src.main:app" | grep -v grep | awk '{print $2}')

if [ -n "$UVICORN_PID" ]; then
    echo "⚠️  FastAPI server is running (PID: $UVICORN_PID)"
    echo "   Stopping server..."
    kill $UVICORN_PID
    sleep 2
    echo "✅ Server stopped"
else
    echo "ℹ️  No FastAPI server running"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Starting FastAPI server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd /workspace/MageMirror
export PYTHONPATH=$(pwd):$PYTHONPATH

# Start server in background
nohup uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 > server.log 2>&1 &
SERVER_PID=$!

echo "⏳ Starting server (PID: $SERVER_PID)..."
sleep 3

# Check if server started successfully
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ FastAPI server started successfully"
    echo "   - URL: http://localhost:8000"
    echo "   - API docs: http://localhost:8000/docs"
    echo "   - Log file: server.log"
    echo "   - PID: $SERVER_PID"
else
    echo "❌ Failed to start server. Check server.log for details."
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║                    ✅ Database Fix Complete!                   ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "   ✅ storage_units table created"
echo "   ✅ Default storage data inserted"
echo "   ✅ FastAPI server restarted"
echo ""
echo "🧪 Test the fix:"
echo "   curl http://localhost:8000/storage-units/1"
echo ""
echo "📄 View server logs:"
echo "   tail -f server.log"
echo ""
echo "🛑 Stop server:"
echo "   kill $SERVER_PID"
echo ""
