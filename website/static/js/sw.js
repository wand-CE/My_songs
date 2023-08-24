var CACHE_NAME = "tunecache_cache_v3";
var urlsToCache = [
  "/",
  "/static/img/Tune_Logo_Nome_alternative.png",
  "/static/img/Tune_Logo_Nome.png",
  "/static/img/Tune_logo.png",
  "/static/css/base.css",
  "/static/css/all_songs.css",
  "/static/js/player.js",
  "/static/js/musics_page.js",
  "/static/js/modules/sort_musics.js",
  "/static/js/modules/main_conf.js",
  "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
  "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.4/font/bootstrap-icons.css",
  "//code.jquery.com/jquery-3.6.0.min.js",
  "//code.jquery.com/ui/1.13.0/jquery-ui.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/jqueryui-touch-punch/0.2.2/jquery.ui.touch-punch.min.js",
  "https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js",
  "https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js",
  "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js",
  "https://cdn.jsdelivr.net/npm/howler@2.2.3/dist/howler.min.js",
];

self.addEventListener("install", function (event) {
  self.skipWaiting();
  // install file needed offline
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", function (event) {
  event.respondWith(
    caches.match(event.request).then(function (response) {
      if (response) {
        return response;
      }
      return fetch(event.request);
    })
  );
});
