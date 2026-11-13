(function () {
  var STORAGE_KEY = 'rewired-theme';
  var THEMES = ['commodore', 'crt', 'sepia'];
  var META_COLORS = {
    commodore: '#101038',
    crt: '#020402',
    sepia: '#efe3c8',
  };
  var GISCUS_THEMES = {
    commodore: 'dark',
    crt: 'dark_high_contrast',
    sepia: 'light',
  };

  function normalize(theme) {
    return THEMES.indexOf(theme) === -1 ? 'sepia' : theme;
  }

  function updateButtons(theme) {
    document.querySelectorAll('[data-theme-choice]').forEach(function (button) {
      var active = button.getAttribute('data-theme-choice') === theme;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  function updateMeta(theme) {
    var meta = document.querySelector('[data-theme-color]');
    if (meta && META_COLORS[theme]) {
      meta.setAttribute('content', META_COLORS[theme]);
    }
  }

  function updateTwitter(theme) {
    var mode = theme === 'sepia' ? 'light' : 'dark';

    document.querySelectorAll('.twitter-timeline').forEach(function (link) {
      link.dataset.theme = mode;
    });

    if (window.twttr && window.twttr.widgets && window.twttr.widgets.load) {
      document.querySelectorAll('.home-tweets__pane').forEach(function (pane) {
        window.twttr.widgets.load(pane);
      });
    }
  }

  function updateGiscus(theme) {
    var message = {
      giscus: {
        setConfig: {
          theme: GISCUS_THEMES[theme] || 'dark',
        },
      },
    };

    document.querySelectorAll('iframe.giscus-frame').forEach(function (frame) {
      frame.contentWindow.postMessage(message, 'https://giscus.app');
    });
  }

  function apply(theme, persist) {
    var next = normalize(theme);
    document.documentElement.dataset.theme = next;

    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (error) {
        /* localStorage may be unavailable in private modes. */
      }
    }

    updateButtons(next);
    updateMeta(next);
    updateGiscus(next);
    updateTwitter(next);

    document.dispatchEvent(new CustomEvent('rewired:themechange', { detail: { theme: next } }));
  }

  function current() {
    return normalize(document.documentElement.dataset.theme);
  }

  document.querySelectorAll('[data-theme-choice]').forEach(function (button) {
    button.addEventListener('click', function () {
      apply(button.getAttribute('data-theme-choice'), true);
    });
  });

  window.addEventListener('storage', function (event) {
    if (event.key === STORAGE_KEY && event.newValue) {
      apply(event.newValue, false);
    }
  });

  window.addEventListener('message', function (event) {
    if (event.origin !== 'https://giscus.app') return;
    if (!event.data || !event.data.giscus) return;
    updateGiscus(current());
  });

  document.addEventListener('rewired:themechange', function (event) {
    updateGiscus(event.detail.theme);
  });

  apply(current(), false);

  window.addEventListener('load', function () {
    updateGiscus(current());
  });
})();
