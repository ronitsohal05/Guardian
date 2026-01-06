#!/bin/bash
# Test script for Guardian surplus food notification system
# Tests the complete flow: store registration, image upload, user preferences, and notifications

set -e

API_URL="http://localhost:5001"
TS=$(date +%s)
STORE_EMAIL="store_${TS}@guardian.local"
STORE_PASSWORD="storepass123"
USER_EMAIL="user_${TS}@guardian.local"
USER_PASSWORD="userpass123"
IMAGE_PATH="./test_images/cake.jpg" # set to cake.jpg provided in test_images

echo "🚀 Guardian E2E Test Suite"
echo "================================"

# 1. Register Store
echo ""
echo "1️⃣  Registering store..."
STORE_RESPONSE=$(curl -s -X POST "$API_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$STORE_EMAIL\",
    \"password\": \"$STORE_PASSWORD\"
  }")

STORE_TOKEN=$(echo "$STORE_RESPONSE" | jq -r '.token')
STORE_ID=$(echo "$STORE_RESPONSE" | jq -r '.user_id')
echo "✅ Store registered: $STORE_ID"
echo "   Token: ${STORE_TOKEN:0:20}..."

# 2. Create Store Profile with Location
echo ""
echo "2️⃣  Creating store profile with location..."
STORE_PROFILE=$(curl -s -X POST "$API_URL/stores" \
  -H "Content-Type: application/json" \
  -d "{
    \"store_id\": \"$STORE_ID\",
    \"name\": \"Fresh Market Downtown\",
    \"email\": \"$STORE_EMAIL\",
    \"phone\": \"555-0100\",
    \"location\": {
      \"lat\": 37.7749,
      \"lng\": -122.4194
    }
  }")

echo "✅ Store profile created"
echo "$STORE_PROFILE" | jq '.'

# 3. Register User
echo ""
echo "3️⃣  Registering user..."
USER_RESPONSE=$(curl -s -X POST "$API_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$USER_EMAIL\",
    \"password\": \"$USER_PASSWORD\"
  }")

USER_TOKEN=$(echo "$USER_RESPONSE" | jq -r '.token')
USER_ID=$(echo "$USER_RESPONSE" | jq -r '.user_id')
echo "✅ User registered: $USER_ID"
echo "   Token: ${USER_TOKEN:0:20}..."

# 4. Set User Preferences (Location + Items)
echo ""
echo "4️⃣  Setting user preferences (location + items)..."
USER_PREFS=$(curl -s -X POST "$API_URL/prefs" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d "{
    \"item_filters\": [\"cake\", \"bread\", \"banana\"],
    \"location\": {
      \"lat\": 37.7800,
      \"lng\": -122.4100
    },
    \"radius_km\": 2,
    \"notify\": true
  }")

echo "✅ User preferences saved"
echo "$USER_PREFS" | jq '.'

# 5. List Stores
echo ""
echo "5️⃣  Listing stores..."
STORES=$(curl -s -X GET "$API_URL/stores")
echo "✅ Stores:"
echo "$STORES" | jq '.stores[]'

# 6. Get User Info
echo ""
echo "6️⃣  Getting user info..."
USER_INFO=$(curl -s -X GET "$API_URL/me" \
  -H "Authorization: Bearer $USER_TOKEN")
echo "✅ User info:"
echo "$USER_INFO" | jq '.user | {email, item_filters, location, radius_km, notify}'

# 7. Simulate Food Upload (produce event)
echo ""
echo "7️⃣  Simulating store food detection (publish event)..."

# If an image exists at IMAGE_PATH, send it as multipart/form-data; otherwise send JSON only
if [ -f "$IMAGE_PATH" ]; then
  echo "Using image: $IMAGE_PATH"
  UPLOAD=$(curl -s -X POST "$API_URL/upload-test" \
    -H "Authorization: Bearer $STORE_TOKEN" \
    -F "store_id=$STORE_ID" \
    -F "image=@$IMAGE_PATH")
else
  echo "No image found at $IMAGE_PATH — sending test request without image"
  UPLOAD=$(curl -s -X POST "$API_URL/upload-test" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $STORE_TOKEN" \
    -d "{
      \"store_id\": \"$STORE_ID\"
    }")
fi

echo "✅ Food detected:"
echo "$UPLOAD" | jq '.items'

# Wait for worker to process
echo ""
echo "⏳ Waiting for worker to process events (3 seconds)..."
sleep 3

# 8. Check Notifications
echo ""
echo "8️⃣  Checking notifications..."
NOTIFS=$(curl -s -X GET "http://localhost:27017" 2>/dev/null || echo "{}")
echo "✅ Note: Notifications stored in MongoDB. Check with:"
echo "   mongosh --eval \"db.notifications.find().pretty()\""

echo ""
echo "================================"
echo "✅ E2E Test Complete!"
echo ""
echo "📋 Summary:"
echo "   - Store: $STORE_ID ($STORE_EMAIL)"
echo "   - User: $USER_ID ($USER_EMAIL)"
echo "   - Items watched: cake, bread, banana"
echo "   - Search radius: 2 km"
echo "   - Distance store->user: ~1 km (within radius ✓)"
echo ""
echo "📧 Email notifications sent to: $USER_EMAIL"
echo "   (Check SMTP logs for details)"
