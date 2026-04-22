#!/bin/bash
# Deploy Cloudflare Worker for A/B Testing
# Requires: wrangler CLI authenticated

echo "Deploying MindVault A/B Test Analytics Worker..."

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "Installing wrangler..."
    npm install -g wrangler
fi

# Create wrangler.toml config
cat > wrangler.toml << 'EOF'
name = "mindvault-analytics"
main = "analytics_worker.js"
compatibility_date = "2024-01-01"

# Add your subdomain here
routes = [
  { pattern = "analytics.mindvaultstudio.net/*", zone_name = "mindvaultstudio.net" }
]

[env.production]
kv_namespaces = [
  { binding = "AB_TEST_KV", id = "your_kv_namespace_id_here" }
]
EOF

echo ""
echo "⚠️  IMPORTANT: Before deploying:"
echo "1. Update wrangler.toml with your actual KV namespace ID"
echo "2. Run: wrangler kv:namespace create AB_TEST_KV"
echo "3. Then run: wrangler deploy"
echo ""
echo "To view stats after deployment:"
echo "  curl https://analytics.mindvaultstudio.net/stats"
echo ""
