hexo.extend.injector.register('head_end', () => {
  const root = hexo.config.root || '/';
  const base = root.endsWith('/') ? root : `${root}/`;
  const version = Date.now();

  return `<link rel="stylesheet" href="${base}css/custom.css?v=${version}">`;
});
