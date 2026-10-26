/* Documentation demonstrations only. The Tide CSS package ships no runtime. */
(() => {
  'use strict';
  const form = document.querySelector('[data-validation-demo]');
  if (form) {
    const fields = [...form.querySelectorAll('input[required]')];
    const summary = form.querySelector('.tide-error-summary');
    const list = summary.querySelector('[data-error-list]');
    const result = form.querySelector('[data-form-result]');
    const hints = new Map(fields.map(field => [field, field.getAttribute('aria-describedby') || '']));
    let reviewed = false;
    function reveal(field) {
      for (let parent = field.parentElement; parent; parent = parent.parentElement) {
        if (parent.tagName === 'DETAILS') parent.open = true;
      }
    }
    function renderErrors() {
      list.replaceChildren();
      const invalid = fields.filter(field => !field.validity.valid);
      fields.forEach(field => {
        const error = document.getElementById(field.id + '-error');
        const failed = invalid.includes(field);
        error.hidden = !failed;
        field.toggleAttribute('aria-invalid', failed);
        if (failed) field.setAttribute('aria-invalid', 'true');
        field.setAttribute('aria-describedby', [hints.get(field), failed ? error.id : ''].filter(Boolean).join(' '));
        if (failed) {
          reveal(field);
          const link = document.createElement('a');
          link.className = 'tide-link';
          link.href = '#' + field.id;
          link.textContent = error.textContent;
          link.addEventListener('click', event => {
            if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault(); reveal(field); field.focus();
          });
          const item = document.createElement('li'); item.append(link); list.append(item);
        }
      });
      summary.hidden = !invalid.length;
      return invalid;
    }
    form.noValidate = true;
    form.addEventListener('submit', event => {
      event.preventDefault(); reviewed = true; result.textContent = '';
      if (renderErrors().length) summary.focus();
      else result.textContent = 'The sample details are valid. Nothing was submitted.';
    });
    fields.forEach(field => field.addEventListener('input', () => {
      result.textContent = '';
      if (reviewed) renderErrors();
    }));
    form.addEventListener('reset', () => {
      reviewed = false; summary.hidden = true; list.replaceChildren(); result.textContent = '';
      fields.forEach(field => {
        field.removeAttribute('aria-invalid'); field.setAttribute('aria-describedby', hints.get(field));
        document.getElementById(field.id + '-error').hidden = true;
      });
    });
  }
  const save = document.querySelector('[data-save-demo]');
  if (save) save.addEventListener('click', () => {
    const pressed = save.getAttribute('aria-pressed') !== 'true';
    save.setAttribute('aria-pressed', String(pressed));
    document.querySelector('[data-save-result]').textContent = pressed ? 'Sample is saved for this page visit.' : 'Sample is not saved.';
  });
  document.querySelectorAll('[data-file-demo]').forEach(example => {
    const input = example.querySelector('input');
    const error = example.querySelector('.tide-field__error');
    const result = example.querySelector('[data-file-result]');
    const clear = example.querySelector('[data-clear-file]');
    const hint = input.getAttribute('aria-describedby');
    function update() {
      const file = input.files[0];
      const message = !file ? '' : !['image/jpeg', 'image/png', 'image/webp'].includes(file.type)
        ? 'Choose a JPEG, PNG or WebP image.' : file.size > 10 * 1024 * 1024 ? 'Choose an image of 10 MB or smaller.' : '';
      error.textContent = message; error.hidden = !message;
      if (message) input.setAttribute('aria-invalid', 'true'); else input.removeAttribute('aria-invalid');
      input.setAttribute('aria-describedby', message ? hint + ' ' + error.id : hint);
      result.textContent = !file ? 'No file selected.' : message ? 'The selected file is not accepted. Choose a replacement or remove it.' : file.name + ' · ' + Math.ceil(file.size / 1024) + ' KB · selected locally';
      clear.hidden = !file;
    }
    input.addEventListener('change', update);
    clear.addEventListener('click', () => { input.value = ''; update(); input.focus(); });
  });
})();
