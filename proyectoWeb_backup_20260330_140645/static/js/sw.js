self.addEventListener('fetch', function(event) {
    // Este código permite que la app funcione online
    event.respondWith(fetch(event.request));
});
