/**
 * Cloudflare Worker for A/B Testing & Analytics
 * 
 * Routes traffic 50/50 between variants
 * Tracks impressions + conversions
 * Provides real-time stats endpoint
 * 
 * Deploy to: analytics.mindvaultstudio.net
 */

// A/B Test State (stored in Cloudflare Analytics Engine or KV)
const TEST_CONFIG = {
  testId: 'assessment_deposit_v1',
  variants: ['a', 'b'],
  targetSampleSize: 200 // Total visitors before evaluation
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    // Route: /log - Track events
    if (url.pathname === '/log' && request.method === 'POST') {
      return await handleLog(request, env, corsHeaders);
    }
    
    // Route: /stats - View test statistics
    if (url.pathname === '/stats' && request.method === 'GET') {
      return await handleStats(request, env, corsHeaders);
    }
    
    // Route: /assign - Get variant assignment
    if (url.pathname === '/assign' && request.method === 'GET') {
      return await handleAssign(request, env, corsHeaders);
    }
    
    return new Response('Not Found', { status: 404, headers: corsHeaders });
  }
};

/**
 * Log event (impression or conversion)
 */
async function handleLog(request, env, corsHeaders) {
  try {
    const data = await request.json();
    const { event, variant, test, sessionId, timestamp } = data;
    
    // Validate
    if (!event || !variant || !test) {
      return jsonResponse({ error: 'Missing required fields' }, 400, corsHeaders);
    }
    
    // Write to Analytics Engine (if configured)
    if (env.ANALYTICS) {
      await env.ANALYTICS.writeDataPoint({
        blobs: [test, variant, event, sessionId],
        doubles: [event === 'conversion' ? 1 : 0, 1],
        indexes: [test]
      });
    }
    
    // Also track in KV for quick queries
    const date = new Date().toISOString().split('T')[0];
    const key = `${test}:${variant}:${event}:${date}`;
    
    if (env.AB_TEST_KV) {
      const current = parseInt(await env.AB_TEST_KV.get(key) || '0');
      await env.AB_TEST_KV.put(key, (current + 1).toString());
    }
    
    return jsonResponse({ success: true }, 200, corsHeaders);
    
  } catch (e) {
    return jsonResponse({ error: e.message }, 500, corsHeaders);
  }
}

/**
 * Get test statistics
 */
async function handleStats(request, env, corsHeaders) {
  try {
    const url = new URL(request.url);
    const test = url.searchParams.get('test') || TEST_CONFIG.testId;
    
    // Get stats from KV
    const stats = {
      test,
      timestamp: new Date().toISOString(),
      variants: {}
    };
    
    if (env.AB_TEST_KV) {
      for (const variant of TEST_CONFIG.variants) {
        // Get today's stats
        const date = new Date().toISOString().split('T')[0];
        const impressions = parseInt(
          await env.AB_TEST_KV.get(`${test}:${variant}:impression:${date}`) || '0'
        );
        const conversions = parseInt(
          await env.AB_TEST_KV.get(`${test}:${variant}:conversion:${date}`) || '0'
        );
        
        // Get all-time stats
        const allTimeImpressions = await getAllTimeCount(env, test, variant, 'impression');
        const allTimeConversions = await getAllTimeCount(env, test, variant, 'conversion');
        
        stats.variants[variant] = {
          today: { impressions, conversions, rate: impressions > 0 ? (conversions/impressions * 100).toFixed(2) + '%' : '0%' },
          allTime: { 
            impressions: allTimeImpressions, 
            conversions: allTimeConversions,
            rate: allTimeImpressions > 0 ? (allTimeConversions/allTimeImpressions * 100).toFixed(2) + '%' : '0%'
          }
        };
      }
    }
    
    // Calculate significance (simplified)
    const variantA = stats.variants.a?.allTime || { conversions: 0, impressions: 0 };
    const variantB = stats.variants.b?.allTime || { conversions: 0, impressions: 0 };
    const totalImpressions = variantA.impressions + variantB.impressions;
    
    stats.summary = {
      totalImpressions,
      targetSampleSize: TEST_CONFIG.targetSampleSize,
      progress: Math.min(100, Math.round((totalImpressions / TEST_CONFIG.targetSampleSize) * 100)) + '%',
      sufficientData: totalImpressions >= TEST_CONFIG.targetSampleSize,
      recommendation: totalImpressions >= TEST_CONFIG.targetSampleSize 
        ? getRecommendation(variantA, variantB)
        : 'Collecting data...'
    };
    
    return jsonResponse(stats, 200, corsHeaders);
    
  } catch (e) {
    return jsonResponse({ error: e.message }, 500, corsHeaders);
  }
}

/**
 * Assign variant to new visitor
 */
async function handleAssign(request, env, corsHeaders) {
  // Simple 50/50 assignment
  const variant = Math.random() < 0.5 ? 'a' : 'b';
  
  return jsonResponse({
    variant,
    test: TEST_CONFIG.testId,
    description: variant === 'a' 
      ? 'Deposit messaging (applicable credit)'
      : 'No deposit messaging'
  }, 200, corsHeaders);
}

/**
 * Get all-time count from KV
 */
async function getAllTimeCount(env, test, variant, event) {
  if (!env.AB_TEST_KV) return 0;
  
  // List all keys for this test/variant/event
  const prefix = `${test}:${variant}:${event}:`;
  const keys = await env.AB_TEST_KV.list({ prefix });
  
  let total = 0;
  for (const key of keys.keys) {
    const count = parseInt(await env.AB_TEST_KV.get(key.name) || '0');
    total += count;
  }
  
  return total;
}

/**
 * Get recommendation based on conversion rates
 */
function getRecommendation(variantA, variantB) {
  const rateA = variantA.impressions > 0 ? variantA.conversions / variantA.impressions : 0;
  const rateB = variantB.impressions > 0 ? variantB.conversions / variantB.impressions : 0;
  
  const diff = Math.abs(rateA - rateB);
  const lift = Math.max(rateA, rateB) / Math.min(rateA, rateB) - 1;
  
  if (diff < 0.01) {
    return 'No significant difference. Either variant is fine.';
  }
  
  const winner = rateA > rateB ? 'Variant A (deposit messaging)' : 'Variant B (no deposit)';
  return `${winner} is winning with ${(lift * 100).toFixed(1)}% lift in conversions`;
}

/**
 * JSON response helper
 */
function jsonResponse(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    }
  });
}
