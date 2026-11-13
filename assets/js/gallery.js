(function () {
  var galleries = document.querySelectorAll('[data-photo-gallery]');
  if (!galleries.length) return;

  var dialog = document.createElement('dialog');
  dialog.className = 'photo-lightbox';
  dialog.setAttribute('aria-label', 'Photo gallery');
  dialog.innerHTML =
    '<div class="photo-lightbox__frame">' +
      '<button class="photo-lightbox__close" type="button" aria-label="Close gallery">×</button>' +
      '<img class="photo-lightbox__image" alt="">' +
      '<div class="photo-lightbox__bar">' +
        '<button class="photo-lightbox__nav" type="button" data-gallery-prev aria-label="Previous photo">←</button>' +
        '<span class="photo-lightbox__counter" aria-live="polite"></span>' +
        '<button class="photo-lightbox__nav" type="button" data-gallery-next aria-label="Next photo">→</button>' +
      '</div>' +
      '<p class="photo-lightbox__caption"></p>' +
    '</div>';
  document.body.appendChild(dialog);

  var image = dialog.querySelector('.photo-lightbox__image');
  var caption = dialog.querySelector('.photo-lightbox__caption');
  var counter = dialog.querySelector('.photo-lightbox__counter');
  var previous = dialog.querySelector('[data-gallery-prev]');
  var next = dialog.querySelector('[data-gallery-next]');
  var close = dialog.querySelector('.photo-lightbox__close');
  var items = [];
  var index = 0;

  function render() {
    var item = items[index];
    if (!item) return;
    image.src = item.href;
    image.alt = item.alt;
    caption.textContent = item.caption;

    if (item.link) {
      caption.append(' ');
      var link = document.createElement('a');
      link.href = item.link;
      link.textContent = item.linkText || item.link;
      link.target = '_blank';
      link.rel = 'noopener';
      caption.append(link);
    }

    counter.textContent = (index + 1) + ' / ' + items.length;
    previous.disabled = index === 0;
    next.disabled = index === items.length - 1;
  }

  function step(offset) {
    index = Math.min(items.length - 1, Math.max(0, index + offset));
    render();
  }

  function open(list, start) {
    items = list;
    index = start;
    render();
    dialog.showModal();
  }

  galleries.forEach(function (gallery) {
    var links = Array.prototype.slice.call(gallery.querySelectorAll('[data-gallery-item]'));

    links.forEach(function (link, position) {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        open(
          links.map(function (item) {
            return {
              href: item.href,
              alt: item.getAttribute('data-alt') || '',
              caption: item.getAttribute('data-caption') || '',
              link: item.getAttribute('data-caption-link') || '',
              linkText: item.getAttribute('data-caption-link-text') || '',
            };
          }),
          position
        );
      });
    });
  });

  previous.addEventListener('click', function () { step(-1); });
  next.addEventListener('click', function () { step(1); });
  close.addEventListener('click', function () { dialog.close(); });

  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowLeft') { event.preventDefault(); step(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); step(1); }
  });
})();
