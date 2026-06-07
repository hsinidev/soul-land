const CACHE_NAME = 'soulland-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/chapters.html',
  '/characters.html',
  '/settings.html',
  '/assets/css/styles.css',
  '/assets/js/app.js',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  // Stale-While-Revalidate for offline capability
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        caches.open(CACHE_NAME).then((cache) => {
          if (event.request.url.startsWith('http')) {
             cache.put(event.request, networkResponse.clone());
          }
        });
        return networkResponse;
      }).catch(() => {
         // Offline fallback if necessary
      });
      return cachedResponse || fetchPromise;
    })
  );
});

// periodic background sync
self.addEventListener('sync', function(event) {
  if (event.tag === 'sync-chapters') {
    console.log('[Service Worker] Syncing new chapters...');
  }
});
