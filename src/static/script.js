if ('serviceWorker' in navigator) {
   // we are checking here to see if the browser supports the  service worker api
window.addEventListener('load', function() {
    navigator.serviceWorker.register('../sw.js').then(function(registration) {
      // Registration was successful
      console.log('Service Worker registration was successful with scope: ', registration.scope);
    }, function(err) {
      // registration failed :(
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}


window.addEventListener("beforeinstallprompt", ev => {
  // Stop Chrome from asking _now_
  ev.preventDefault();

  // Create your custom "add to home screen" button here if needed.
  // Keep in mind that this event may be called multiple times,
  // so avoid creating multiple buttons!
  btnAdd.onclick = () => ev.prompt();
});