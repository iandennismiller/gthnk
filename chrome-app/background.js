chrome.app.runtime.onLaunched.addListener(function() {
  chrome.app.window.create('http://localhost:1620/admin/journal/latest.html', {
    'bounds': {
      'width': 750,
      'height': 600
    }
  });
});
