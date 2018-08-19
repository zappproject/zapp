var CACHE_NAME = 'Zapp App';
var urlsToCache = [
  '/register',
  '/send',
  'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
  'https://code.jquery.com/jquery-3.2.1.slim.min.js',
  '/static/css/main.css',
  '/static/script.js'
];
self.addEventListener('install', function(event) {
  // install files needed offline
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});
self.addEventListener('fetch', function(event) {
  // every request from our site, passes through the fetch handler
  // I have proof
  console.log('I am a request with url:', event.request.clone().url)
  event.respondWith(
    // check all the caches in the browser and find
    // out whether our request is in any of them
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          // if we are here, that means there's a match
          //return the response stored in browser
          return response;
        }
        // no match in cache, use the network instead
        return fetch(event.request);
      }
    )
  );
});