/// <reference types="@sveltejs/kit" />
import { build, files, version } from '$service-worker';

const CACHE = `cache-${version}`;

const ASSETS = [
    ...build,
    ...files
];

self.addEventListener('install', (event) => {
    async function addFilesToCache() {
        const cache = await caches.open(CACHE);
        await cache.addAll(ASSETS);
    }
    event.waitUntil(addFilesToCache());
});

self.addEventListener('activate', (event) => {
    async function deleteOldCaches() {
        for (const key of await caches.keys()) {
            if (key !== CACHE) await caches.delete(key);
        }
    }
    event.waitUntil(deleteOldCaches());
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;
    
    async function respond() {
        const url = new URL(event.request.url);
        const cache = await caches.open(CACHE);

        // Serve build/static files from cache
        if (ASSETS.includes(url.pathname)) {
            return cache.match(event.request);
        }

        // For images (manga pages), try cache first, then network
        if (url.pathname.includes('/manga/')) {
            const cachedResponse = await cache.match(event.request);
            if (cachedResponse) return cachedResponse;
            
            const response = await fetch(event.request);
            if (response.status === 200) {
                cache.put(event.request, response.clone());
            }
            return response;
        }

        // For other requests, try network, fallback to cache
        try {
            const response = await fetch(event.request);
            if (!(response instanceof Response)) {
                throw new Error('invalid response from fetch');
            }
            return response;
        } catch (err) {
            const response = await cache.match(event.request);
            if (response) return response;
            throw err;
        }
    }

    event.respondWith(respond());
});
