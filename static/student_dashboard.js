
setInterval(function() {
    fetch('/get_news_count')
      .then(response => response.json())
      .then(data => {
        document.getElementById('newsCount').textContent = data.news_count || '0';
      })
      .catch(error => {
        console.error('Error:', error);
      });
}, 10000);