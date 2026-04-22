/**
 * MindVault AI Assessment - A/B Test Script
 * Routes 50/50 between Variant A (deposit messaging) and Variant B (no deposit)
 * Tracks impressions and conversions
 */

// A/B Test Configuration
const AB_TEST_CONFIG = {
  testName: 'assessment_deposit_messaging_v1',
  variants: ['a', 'b'], // a = with deposit, b = without
  splitRatio: 0.5, // 50/50
  cookieName: 'mv_ab_test_variant',
  cookieDuration: 30 // days
};

/**
 * Assign or retrieve variant for this user
 */
function getVariant() {
  // Check for existing assignment
  let variant = getCookie(AB_TEST_CONFIG.cookieName);
  
  if (!variant) {
    // New visitor - assign variant
    variant = Math.random() < AB_TEST_CONFIG.splitRatio ? 'a' : 'b';
    setCookie(AB_TEST_CONFIG.cookieName, variant, AB_TEST_CONFIG.cookieDuration);
    
    // Log impression
    logEvent('impression', { variant, test: AB_TEST_CONFIG.testName });
  }
  
  return variant;
}

/**
 * Apply variant to page
 */
function applyVariant(variant) {
  const body = document.body;
  body.classList.add(`ab-variant-${variant}`);
  
  if (variant === 'b') {
    // Hide deposit messaging
    hideDepositElements();
  } else {
    // Variant A - add conversion tracking
    trackConversions();
  }
  
  // Track conversions for both variants
  trackConversions();
}

/**
 * Hide deposit-related elements for Variant B
 */
function hideDepositElements() {
  // Hide price note under $997
  const priceNote = document.querySelector('.price-note');
  if (priceNote) priceNote.style.display = 'none';
  
  // Hide deposit callout in FAQ
  const depositCallout = document.querySelector('.deposit-callout');
  if (depositCallout) depositCallout.style.display = 'none';
  
  // Hide implementation credit section in report (if viewing report)
  const creditSection = document.querySelector('.implementation-credit');
  if (creditSection) creditSection.style.display = 'none';
}

/**
 * Track clicks on CTA buttons
 */
function trackConversions() {
  const ctaButtons = document.querySelectorAll('.cta-btn, [data-track="conversion"]');
  
  ctaButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const variant = getCookie(AB_TEST_CONFIG.cookieName);
      logEvent('conversion', { 
        variant, 
        test: AB_TEST_CONFIG.testName,
        element: e.target.textContent.trim()
      });
    });
  });
}

/**
 * Log event to backend
 */
async function logEvent(eventType, data) {
  try {
    await fetch('https://analytics.mindvaultstudio.net/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event: eventType,
        timestamp: new Date().toISOString(),
        sessionId: getSessionId(),
        ...data
      })
    });
  } catch (e) {
    // Silent fail - don't break user experience
    console.debug('Analytics error:', e);
  }
}

/**
 * Cookie helpers
 */
function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Strict`;
}

function getCookie(name) {
  return document.cookie.split('; ').reduce((r, v) => {
    const parts = v.split('=');
    return parts[0] === name ? decodeURIComponent(parts[1]) : r;
  }, '');
}

/**
 * Session ID for tracking unique sessions
 */
function getSessionId() {
  let sessionId = sessionStorage.getItem('mv_session_id');
  if (!sessionId) {
    sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
    sessionStorage.setItem('mv_session_id', sessionId);
  }
  return sessionId;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  const variant = getVariant();
  applyVariant(variant);
  console.log(`A/B Test: Showing variant ${variant.toUpperCase()}`);
});
