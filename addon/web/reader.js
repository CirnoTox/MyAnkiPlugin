const paragraphs = [...document.querySelectorAll('main p')];
function report() {
  let index = paragraphs.findIndex(p => p.getBoundingClientRect().bottom > 0);
  index = Math.max(0, index);
  const rect = paragraphs[index].getBoundingClientRect();
  pycmd(JSON.stringify({topic, position: {paragraph: index, fraction: Math.max(0, Math.min(1, -rect.top / Math.max(1, rect.height)))}}));
}
requestAnimationFrame(() => {
  const p = paragraphs[Math.min(saved.paragraph || 0, paragraphs.length - 1)];
  window.scrollTo(0, p.offsetTop + (saved.fraction || 0) * p.offsetHeight);
  window.addEventListener('scroll', report);
});
