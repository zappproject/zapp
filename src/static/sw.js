var CACHE_NAME = 'Zapp App';
var urlsToCache = [
  '/',
  '/register',
  '/static/css/main.css',
  '/static/script.js',
  'https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,500,600,700,900',
  'https://use.fontawesome.com/releases/v5.0.13/css/all.css',
  'https://code.jquery.com/jquery-3.2.1.slim.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
  'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
  '/static/manifest.json',
]
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