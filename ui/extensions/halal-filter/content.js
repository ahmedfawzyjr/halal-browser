/**
 * Halal Content Filter - Content Script
 * Scans and filters content on web pages
 */

console.log('🌙 Halal Content Filter - Content script loaded');

// Configuration
let config = null;

// Load config from background
chrome.runtime.sendMessage({ action: 'getConfig' }, (response) => {
  config = response;
  console.log('✅ Config loaded in content script:', config);
  
  // Start scanning page
  scanPage();
});

// Scan all images on page
async function scanPage() {
  console.log('🔍 Scanning page for content...');
  
  // Scan existing images
  const images = document.querySelectorAll('img');
  console.log(`   Found ${images.length} images`);
  
  for (const img of images) {
    await scanImage(img);
  }
  
  // Watch for new images
  observeNewImages();
}

// Scan individual image
async function scanImage(img) {
  // Skip if already scanned
  if (img.dataset.halalScanned) {
    return;
  }
  
  // Mark as scanned
  img.dataset.halalScanned = 'true';
  
  // Skip small images (likely icons)
  if (img.width < 50 || img.height < 50) {
    return;
  }
  
  // Skip if no src
  if (!img.src || img.src.startsWith('data:')) {
    return;
  }
  
  try {
    // Ask background to scan image
    const result = await chrome.runtime.sendMessage({
      action: 'scanImage',
      url: img.src
    });
    
    // Handle result
    if (result.decision === 'BLOCK') {
      blockImage(img);
    } else if (result.decision === 'BLUR') {
      blurImage(img);
    }
    
  } catch (error) {
    console.error('❌ Error scanning image:', error);
  }
}

// Block image completely
function blockImage(img) {
  console.log('🛑 Blocking image:', img.src);
  
  // Create blocked placeholder
  const placeholder = document.createElement('div');
  placeholder.className = 'halal-blocked-image';
  placeholder.innerHTML = `
    <div class="halal-blocked-content">
      <span class="halal-icon">🛑</span>
      <span class="halal-text">Content Blocked</span>
      <span class="halal-subtext">This image was blocked by Halal Filter</span>
    </div>
  `;
  
  // Set size to match image
  placeholder.style.width = img.width ? `${img.width}px` : '100%';
  placeholder.style.height = img.height ? `${img.height}px` : 'auto';
  
  // Replace image
  img.parentNode.replaceChild(placeholder, img);
}

// Blur image with warning
function blurImage(img) {
  console.log('⚠️ Blurring image:', img.src);
  
  // Add blur class
  img.classList.add('halal-blurred-image');
  
  // Create warning overlay
  const overlay = document.createElement('div');
  overlay.className = 'halal-blur-overlay';
  overlay.innerHTML = `
    <div class="halal-blur-warning">
      <span class="halal-icon">⚠️</span>
      <span class="halal-text">Content Hidden</span>
      <button class="halal-reveal-btn">Click to Reveal</button>
    </div>
  `;
  
  // Wrap image
  const wrapper = document.createElement('div');
  wrapper.className = 'halal-blur-wrapper';
  wrapper.style.position = 'relative';
  wrapper.style.display = 'inline-block';
  
  img.parentNode.insertBefore(wrapper, img);
  wrapper.appendChild(img);
  wrapper.appendChild(overlay);
  
  // Add click to reveal
  const revealBtn = overlay.querySelector('.halal-reveal-btn');
  revealBtn.addEventListener('click', () => {
    if (confirm('This content may be inappropriate. Show anyway?')) {
      img.classList.remove('halal-blurred-image');
      overlay.remove();
    }
  });
}

// Observe new images added to page
function observeNewImages() {
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (node.tagName === 'IMG') {
          scanImage(node);
        } else if (node.querySelectorAll) {
          const images = node.querySelectorAll('img');
          images.forEach(img => scanImage(img));
        }
      }
    }
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  console.log('👀 Watching for new images...');
}

// Scan videos (optional - can be expensive)
function scanVideos() {
  const videos = document.querySelectorAll('video');
  console.log(`   Found ${videos.length} videos`);
  
  // For now, just log videos
  // Full video scanning would require frame extraction
  videos.forEach(video => {
    console.log('🎥 Video found:', video.src);
  });
}

// Listen for messages from background
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'rescanPage') {
    scanPage();
    sendResponse({ success: true });
  }
});

console.log('✅ Halal Content Filter - Ready');
