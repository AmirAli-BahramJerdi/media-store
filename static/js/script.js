// ===== Theme toggle =====
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

// ===== Mobile menu =====
(function () {
  const nav = document.querySelector('#nav');
  const toggle = document.querySelector('#menuToggle');
  if (!nav || !toggle) return;
  toggle.addEventListener('click', () => nav.classList.toggle('open'));
  nav.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => nav.classList.remove('open'))
  );
})();

// ===== Smooth scroll =====
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

// ===== Product filters =====
(function () {
  const buttons = document.querySelectorAll('.filter-button');
  if (!buttons.length) return;
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      button.classList.add('active');
      const filter = button.dataset.filter;
      document.querySelectorAll('.product-card').forEach(card => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.style.display = show ? '' : 'none';
        if (show) {
          card.style.animation = 'none';
          void card.offsetHeight;
          card.style.animation = '';
        }
      });
    });
  });
})();

// ===== Track order (AJAX) + Steps rendering =====
(function () {
  const form = document.querySelector('#trackForm');
  if (!form) return;

  const resultEl = document.querySelector('#trackingResult');
  const errorEl = document.querySelector('#trackError');
  const phoneInput = document.querySelector('#trackPhone');
  const statusEl = document.querySelector('#trackStatus');
  const idEl = document.querySelector('#trackId');
  const progressEl = document.querySelector('#trackProgress');
  const deviceEl = document.querySelector('#trackDevice');
  const etaEl = document.querySelector('#trackETA');
  const stepsEl = document.querySelector('#trackSteps');

  const STEPS = [
    { icon: '▣', title: 'دریافت دستگاه', desc: 'تحویل به تکنسین' },
    { icon: '⌕', title: 'بررسی اولیه',    desc: 'تشخیص دقیق مشکل' },
    { icon: '⚒', title: 'در حال تعمیر',   desc: 'توسط متخصص' },
    { icon: '✓', title: 'آماده تحویل',    desc: 'تست نهایی کیفیت' },
  ];
  const PERSIAN_INDEX = ['۰۱', '۰۲', '۰۳', '۰۴'];

  function renderSteps(currentStep) {
    if (!stepsEl) return;
    stepsEl.innerHTML = STEPS.map((s, i) => {
      let state = '';
      if (currentStep >= 4 || i < currentStep) state = 'done';
      else if (i === currentStep) state = 'current';

      return `
        <div class="track-step ${state}">
          <b class="track-step-index">${PERSIAN_INDEX[i]}</b>
          <strong class="track-step-icon">${s.icon}</strong>
          <h4>${s.title}</h4>
          <p>${s.desc}</p>
          ${state === 'current' ? '<span class="track-step-badge">مرحله فعلی</span>' : ''}
          ${state === 'done' ? '<span class="track-step-check">✓</span>' : ''}
        </div>
      `;
    }).join('');
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const phone = (phoneInput.value || '').trim();
    if (!phone) return;

    resultEl.hidden = true;
    errorEl.hidden = true;

    try {
      const res = await fetch(`/repairs/api/track/?phone=${encodeURIComponent(phone)}`);
      const data = await res.json();

      if (!data.found) {
        errorEl.hidden = false;
        errorEl.textContent = data.message || 'سفارشی با این شماره یافت نشد.';
        return;
      }

      const o = data.order;
      statusEl.textContent = o.status;
      idEl.textContent = `سفارش #${o.id}`;
      progressEl.style.width = `${o.progress}%`;
      deviceEl.textContent = `مدل: ${o.device}`;
      etaEl.textContent = o.estimated_delivery
        ? `تحویل تقریبی: ${o.estimated_delivery}`
        : '';

      renderSteps(o.current_step);

      resultEl.hidden = false;
      resultEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (err) {
      errorEl.hidden = false;
      errorEl.textContent = 'خطا در ارتباط با سرور. دوباره تلاش کن.';
    }
  });
})();