# A/B Testing Infrastructure

Batches of 200 visitors, 50/50 split between variants.

## Quick Start

```bash
# 1. Deploy analytics worker
cd /root/projects/mindvault-assess
bash deploy_analytics.sh

# 2. Set up KV namespace
wrangler kv:namespace create AB_TEST_KV

# 3. Update wrangler.toml with your KV ID, then deploy
wrangler deploy
```

## Variants

| Variant | Description |
|---------|-------------|
| **A** | WITH deposit messaging ("$997 applies to implementation") |
| **B** | WITHOUT deposit messaging |

## Viewing Results

Live stats endpoint:
```bash
curl https://analytics.mindvaultstudio.net/stats
```

Returns:
```json
{
  "test": "assessment_deposit_v1",
  "summary": {
    "totalImpressions": 200,
    "targetSampleSize": 200,
    "progress": "100%",
    "sufficientData": true,
    "recommendation": "Variant A winning with 23% lift in conversions"
  },
  "variants": {
    "a": { "conversions": 12, "impressions": 100, "rate": "12.0%" },
    "b": { "conversions": 8, "impressions": 100, "rate": "8.0%" }
  }
}
```

## Test Conclusion Criteria

Stop test when:
- ✅ 200 total visitors reached (100 per variant)
- ✅ Statistical significance at 95% confidence
- ✅ Minimum 20 conversions combined

Winner is variant with higher conversion rate on "Book Assessment" CTA.

## Files

- `ab-test.js` — Client-side variant assignment & tracking
- `analytics_worker.js` — Cloudflare Worker for stats
- `deploy_analytics.sh` — Deployment script

## Tracking Events

| Event | Trigger |
|-------|---------|
| `impression` | Page load with variant assigned |
| `conversion` | Click on any CTA button |

## Privacy

- No PII collected
- Session ID rotated per session
- 30-day cookie for variant consistency
