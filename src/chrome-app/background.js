chrome.app.runtime.onLaunched.addListener(function() {
  chrome.app.window.create('http://localhost:1620/day/live', {
    'bounds': {
      'width': 750,
      'height': 600
    }
  });
});
