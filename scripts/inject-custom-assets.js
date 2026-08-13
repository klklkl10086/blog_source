hexo.extend.injector.register('body_end', () => {
  const root = hexo.config.root || '/';
  const base = root.endsWith('/') ? root : `${root}/`;
  const version = Date.now();

  return `<script src="${base}js/code-fold.js?v=${version}"></script>`;
});
