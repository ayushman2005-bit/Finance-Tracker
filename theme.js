/* theme.js - included inline in each template */
(function(){
  var saved = localStorage.getItem('ft-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  function toggle(){
    var current = document.documentElement.getAttribute('data-theme');
    var next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('ft-theme', next);
    var btn = document.getElementById('theme-btn');
    if(btn){
      btn.querySelector('.toggle-icon').textContent = next === 'dark' ? '☀' : '★';
      btn.querySelector('.toggle-label').textContent = next === 'dark' ? 'Light mode' : 'Dark mode';
    }
  }
  document.addEventListener('DOMContentLoaded', function(){
    var btn = document.getElementById('theme-btn');
    if(btn){
      var theme = document.documentElement.getAttribute('data-theme');
      btn.querySelector('.toggle-icon').textContent = theme === 'dark' ? '☀' : '★';
      btn.querySelector('.toggle-label').textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
      btn.addEventListener('click', toggle);
    }
  });
})();