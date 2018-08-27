var CACHE_NAME = 'Zapp App';
var urlsToCache = [
  '/register',
  '/loginpage',
  '/static/css/main.css',
  '/static/css/12345.css',
  '/static/css/homeuserexists.css',
  '/static/css/profile.css',
  '/static/css/sendfxxkit.css',
  '/static/css/trans.css',
  '/static/script.js',
  '/static/Javascript/12345.js',
  '/static/Javascript/homeuserexists.js',
  '/static/Javascript/profile.js',
  '/static/Javascript/sendfxxkit.js',
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