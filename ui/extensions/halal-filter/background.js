/**
 * Halal Content Filter - Background Service Worker
 * Handles content filtering and policy enforcement
 */

const AI_SERVICE_URL = 'http://127.0.0.1:5000';
const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours

// Load configuration
let config = {
  activeProfile: 'family',
  aiServiceEnabled: true,
  cacheEnabled: true
};

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  console.log('🌙 Halal Content Filter installed');
  loadConfig();
  setupAlarms();
});

// Load configuration from storage
async function loadConfig() {
  const stored = await chrome.storage.local.get(['config']);
  if (stored.config) {
    config = stored.config;
  }
  console.log('✅ Config loaded:', config);
}

// Save configuration
async function saveConfig() {
  await chrome.storage.local.set({ config });
}

// Setup periodic tasks
function setupAlarms() {
  // Clear old cache every hour
  chrome.alarms.create('clearCache', { periodInMinutes: 60 });
  
  // Check prayer times every 5 minutes
  chrome.alarms.create('prayerCheck', { periodInMinutes: 5 });
}

// Handle alarms
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'clearCache') {
    clearOldCache();
  } else if (alarm.name === 'prayerCheck') {
    checkPrayerTimes();
  }
});

// URL filtering
chrome.webRequest.onBeforeRequest.addListener(
  async (details) => {
    // Skip internal requests
    if (details.url.startsWith('chrome://') || 
        details.url.startsWith('chrome-extension://')) {
      return {};
    }
    
    // Check URL against blocklist
    const urlDecision = await checkURL(details.url);
    
    if (urlDecision.decision === 'BLOCK') {
      console.log('🛑 Blocked URL:', details.url);
      logActivity('URL_BLOCKED', details.url, urlDecision.reason);
      
      // Redirect to blocked page
      return {
        redirectUrl: chrome.runtime.getURL('blocked.html') + 
                    '?url=' + encodeURIComponent(details.url) +
                    '&reason=' + encodeURIComponent(urlDecision.reason)
      };
    }
    
    return {};
  },
  { urls: ['<all_urls>'] },
  ['blocking']
);

// Check URL against filters
async function checkURL(url) {
  try {
    // Check cache first
    if (config.cacheEnabled) {
      const cached = await getCachedDecision(url);
      if (cached) {
        return cached;
      }
    }
    
    // Check with AI service
    const response = await fetch(`${AI_SERVICE_URL}/api/scan/url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    
    if (!response.ok) {
      console.warn('⚠️ AI service unavailable, using local filters only');
      return checkURLLocal(url);
    }
    
    const result = await response.json();
    
    // Cache result
    if (config.cacheEnabled) {
      await cacheDecision(url, result);
    }
    
    return result;
    
  } catch (error) {
    console.error('❌ Error checking URL:', error);
    return checkURLLocal(url);
  }
}

// Local URL checking (fallback)
function checkURLLocal(url) {
  const domain = new URL(url).hostname.toLowerCase();
  
  // Simple blocklist check
  const blockedKeywords = ['porn', 'xxx', 'casino', 'gambling', 'bet'];
  
  for (const keyword of blockedKeywords) {
    if (domain.includes(keyword)) {
      return {
        decision: 'BLOCK',
        reason: `Domain contains blocked keyword: ${keyword}`
      };
    }
  }
  
  return {
    decision: 'ALLOW',
    reason: 'Passed local checks'
  };
}

// Cache management
async function getCachedDecision(url) {
  const key = `cache_${hashString(url)}`;
  const stored = await chrome.storage.local.get([key]);
  
  if (stored[key]) {
    const cached = stored[key];
    const age = Date.now() - cached.timestamp;
    
    if (age < CACHE_DURATION) {
      console.log('📦 Using cached decision for:', url);
      return cached.decision;
    }
  }
  
  return null;
}

async function cacheDecision(url, decision) {
  const key = `cache_${hashString(url)}`;
  await chrome.storage.local.set({
    [key]: {
      decision,
      timestamp: Date.now()
    }
  });
}

async function clearOldCache() {
  const items = await chrome.storage.local.get(null);
  const now = Date.now();
  const keysToRemove = [];
  
  for (const [key, value] of Object.entries(items)) {
    if (key.startsWith('cache_') && value.timestamp) {
      const age = now - value.timestamp;
      if (age > CACHE_DURATION) {
        keysToRemove.push(key);
      }
    }
  }
  
  if (keysToRemove.length > 0) {
    await chrome.storage.local.remove(keysToRemove);
    console.log(`🗑️ Cleared ${keysToRemove.length} old cache entries`);
  }
}

// Activity logging
async function logActivity(action, url, reason) {
  const log = {
    timestamp: new Date().toISOString(),
    action,
    url,
    reason,
    profile: config.activeProfile
  };
  
  // Get existing logs
  const stored = await chrome.storage.local.get(['activityLog']);
  const logs = stored.activityLog || [];
  
  // Add new log
  logs.push(log);
  
  // Keep only last 1000 entries
  if (logs.length > 1000) {
    logs.shift();
  }
  
  // Save logs
  await chrome.storage.local.set({ activityLog: logs });
  
  // Send notification if enabled
  if (config.notificationsEnabled) {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon48.png',
      title: 'Content Blocked',
      message: `Blocked: ${new URL(url).hostname}`
    });
  }
}

// Prayer times check
async function checkPrayerTimes() {
  // TODO: Implement prayer times checking
  // This would integrate with Islamic prayer times API
  console.log('🕌 Checking prayer times...');
}

// Message handling from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scanImage') {
    scanImage(request.url).then(sendResponse);
    return true; // Async response
  } else if (request.action === 'getConfig') {
    sendResponse(config);
  } else if (request.action === 'setProfile') {
    config.activeProfile = request.profile;
    saveConfig();
    sendResponse({ success: true });
  }
});

// Scan image with AI service
async function scanImage(imageUrl) {
  try {
    // Check cache
    if (config.cacheEnabled) {
      const cached = await getCachedDecision(imageUrl);
      if (cached) {
        return cached;
      }
    }
    
    // Scan with AI
    const response = await fetch(`${AI_SERVICE_URL}/api/scan/image`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_url: imageUrl,
        threshold: 0.7
      })
    });
    
    if (!response.ok) {
      return { decision: 'ALLOW', reason: 'AI service unavailable' };
    }
    
    const result = await response.json();
    
    // Cache result
    if (config.cacheEnabled) {
      await cacheDecision(imageUrl, result);
    }
    
    // Log if blocked
    if (result.decision !== 'ALLOW') {
      logActivity('IMAGE_' + result.decision, imageUrl, 
                  `NSFW confidence: ${(result.confidence * 100).toFixed(1)}%`);
    }
    
    return result;
    
  } catch (error) {
    console.error('❌ Error scanning image:', error);
    return { decision: 'ALLOW', reason: 'Error scanning' };
  }
}

// Utility: Hash string for cache keys
function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36);
}

console.log('🌙 Halal Content Filter - Background service worker loaded');
