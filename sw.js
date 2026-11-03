// Zeigt nur Hinweise an und speichert nichts: ohne fetch-Handler läuft die Seite unverändert.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
    const open = list.find(c => !c.url.includes('hinweis-test'));
    return open ? open.focus() : self.clients.openWindow('./');
  }));
});
