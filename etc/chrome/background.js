chrome.app.runtime.onLaunched.addListener(function() {
  chrome.app.window.create('http://localhost:1621/admin/journal/latest', {
    'bounds': {
      'width': 750,
      'height': 600
    }
  });
});
