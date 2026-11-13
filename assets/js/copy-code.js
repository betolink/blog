(function () {
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }

    return new Promise(function (resolve, reject) {
      var area = document.createElement('textarea');
      area.value = text;
      area.setAttribute('readonly', '');
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();

      try {
        document.execCommand('copy');
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        document.body.removeChild(area);
      }
    });
  }

  function addButton(pre) {
    if (pre.querySelector('.copy-code')) return;

    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-code';
    button.textContent = 'copy';
    button.setAttribute('aria-label', 'Copy code to clipboard');

    button.addEventListener('click', function () {
      var code = pre.querySelector('code');
      var text = code ? code.innerText : pre.innerText;

      copyText(text)
        .then(function () {
          button.textContent = 'copied';
          button.classList.add('is-copied');
          window.setTimeout(function () {
            button.textContent = 'copy';
            button.classList.remove('is-copied');
          }, 1600);
        })
        .catch(function () {
          button.textContent = 'error';
          window.setTimeout(function () {
            button.textContent = 'copy';
          }, 1600);
        });
    });

    pre.appendChild(button);
  }

  function init() {
    document.querySelectorAll('.page__content pre').forEach(addButton);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
