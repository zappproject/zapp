importScripts('/static/cache-polyfill.js');

self.addEventListener('install', function(e) {
 e.waitUntil(
   caches.open('Zapp').then(function(cache) {
     return cache.addAll([
       '/static/icon.png',
       '/templates/home.html',
       '/templates/profile.html'
     ]);
   })
 );
});
self.addEventListener('fetch', function(event) {
 console.log(event.request.url);

 event.respondWith(
   caches.match(event.request).then(function(response) {
     return response || fetch(event.request);
   })
 );
});