document.addEventListener('DOMContentLoaded', () => {
  // Service Worker Registration
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then(registration => {
          console.log('[App] Service Worker registered with scope:', registration.scope);
        })
        .catch(err => {
          console.error('[App] Service Worker registration failed:', err);
        });
    });
  }

  // Request Notification Permission
  const notifyBtn = document.getElementById('btn-notify');
  if (notifyBtn && 'Notification' in window) {
    notifyBtn.addEventListener('click', () => {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
           new Notification('Spirit Awakening Successful!', {
             body: 'You will now receive notifications for new Soul Land chapters.',
             icon: '/assets/icons/icon-192x192.png'
           });
        }
      });
    });
  }
});
