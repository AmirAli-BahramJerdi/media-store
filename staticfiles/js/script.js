// Theme toggle
(function () {
  const app = document.querySelector('#app');
  const themeToggle = document.querySelector('#themeToggle');
  if (!app || !themeToggle) return;

  let isDark = localStorage.getItem('theme') !== 'light';

  function applyTheme(dark) {
    app.classList.toggle('is-dark', dark);
    app.classList.toggle('is-light', !dark);
    themeToggle.textContent = dark ? '\u263E' : '\u263C';
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  }
  applyTheme(isDark);

  themeToggle.addEventListener('click', () => {
    isDark = !isDark;
    applyTheme(isDark);
  });
})();

// Mobile menu
(function () {
  const nav = document.querySelector('#nav');
  const toggle = document.querySelector('#menuToggle');
  if (!nav || !toggle) return;
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
  nav.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => nav.classList.remove('open'))
  );
})();

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href && href !== '#') {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });
});
