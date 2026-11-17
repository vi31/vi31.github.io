/* Studio site script: theme toggle, project/blog filters, contact form. */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ---- Theme toggle ---- */
  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t === 'light' || t === 'dark') return t;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function syncToggle(btn) {
    btn.setAttribute('aria-label', currentTheme() === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }

  /* ---- Filter buttons (Projects by category, Blog by topic) ---- */
  document.querySelectorAll('[data-filters]').forEach(function (group) {
    var items = document.querySelectorAll('[data-filter-list] [data-category]');
    group.hidden = false; /* shown only when JS is available */
    group.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-filter]');
      if (!btn) return;
      var wanted = btn.getAttribute('data-filter');
      group.querySelectorAll('[data-filter]').forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      items.forEach(function (item) {
        item.hidden = wanted !== 'all' && item.getAttribute('data-category') !== wanted;
      });
    });
  });

  /* A link like /blog/#topic-slug opens the list already filtered. */
  if (location.hash) {
    var wantedHash = decodeURIComponent(location.hash.slice(1));
    document.querySelectorAll('[data-filters] [data-filter]').forEach(function (b) {
      if (b.getAttribute('data-filter') === wantedHash) b.click();
    });
  }

  /* ---- Contact form: posts to the form service, shows a plain success/error message ---- */
  var form = document.querySelector('[data-contact-form]');
  if (form && window.fetch && window.FormData) {
    var status = form.querySelector('[data-form-status]');
    var submit = form.querySelector('[type="submit"]');

    var say = function (state, text) {
      status.setAttribute('data-state', state);
      status.textContent = text;
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var action = form.getAttribute('action') || '';
      if (/[\[\]]/.test(action)) {
        say('error', 'Error: this form is not connected yet (set form_endpoint in _config.yml).');
        return;
      }
      submit.disabled = true;
      say('pending', 'Sending…');
      fetch(action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        form.reset();
        say('success', 'Thanks, your message was sent.');
      }).catch(function () {
        say('error', 'Error: your message was not sent. Please try again in a moment.');
      }).then(function () {
        submit.disabled = false;
      });
    });
  }

  var toggle = document.querySelector('[data-theme-toggle]');
  if (toggle) {
    syncToggle(toggle);
    toggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      syncToggle(toggle);
    });
    /* Follow OS changes while the visitor has not chosen a theme. */
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', function () {
        syncToggle(toggle);
      });
    }
  }
})();
