import './styles.css';
import { h, parseHash, $ } from './util.js';
import { t } from './i18n.js';
import { store } from './store.js';
import { homeView } from './views/home.js';
import { studyHome, levelView, bookView, lessonView, pageView } from './views/study.js';
import { exerciseHome, bandView, sectionView, testIntro, testRun, resultView } from './views/exercise.js';
import { mistakesView, bookmarksView, historyView, settingsView } from './views/personal.js';
import { searchView } from './views/search.js';
import { aboutView } from './views/about.js';
import { SOCIAL } from './brand.js';


const routes = [
  [[], homeView],
  [['study'], studyHome], [['study', ':level'], levelView], [['book', ':book'], bookView],
  [['lesson', ':lesson'], lessonView], [['page', ':book', ':page'], pageView],
  [['exercise'], exerciseHome], [['exercise', ':band'], bandView], [['section', ':band', ':sec'], sectionView],
  [['test', ':test'], testIntro], [['test', ':test', 'run'], testRun], [['result', ':attempt'], resultView],
  [['mistakes'], mistakesView], [['bookmarks'], bookmarksView], [['history'], historyView],
  [['settings'], settingsView], [['search'], searchView], [['about'], aboutView],
];

function match(parts) {
  for (const [pat, view] of routes) {
    if (pat.length !== parts.length) continue;
    const params = {};
    if (pat.every((p, i) => (p.startsWith(':') ? ((params[p.slice(1)] = parts[i]), true) : p === parts[i]))) return { view, params };
  }
  return null;
}

function applyPrefs() {
  const p = store.get().prefs;
  const dark = p.theme === 'dark' || (p.theme === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  document.documentElement.style.setProperty('--reading-scale', p.fontScale);
}

const NAV = [
  ['#/', 'navHome'], ['#/study', 'navStudy'], ['#/exercise', 'navExercise'], ['#/mistakes', 'navReview'],
  ['#/bookmarks', 'navBookmarks'], ['#/history', 'navHistory'], ['#/search', 'navSearch'], ['#/about', 'navAbout'],
];

function shell() {
  const themeBtn = h('button', {
    class: 'icon-btn', type: 'button', 'aria-label': 'Ganti tema terang/gelap', title: 'Tema',
    onclick: () => {
      const cur = document.documentElement.dataset.theme;
      store.setPref('theme', cur === 'dark' ? 'light' : 'dark'); applyPrefs();
    },
  }, '◐');
  const menuBtn = h('button', { class: 'icon-btn menu-btn', type: 'button', 'aria-label': 'Buka menu', 'aria-expanded': 'false',
    onclick: (e) => { const nav = $('#nav'); const open = nav.classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', String(open)); } }, '☰');
  const nav = h('nav', { id: 'nav', 'aria-label': 'Navigasi utama' },
    ...NAV.map(([href, k]) => h('a', { href, 'data-nav': href }, t(k))),
    h('a', { href: '#/settings', 'data-nav': '#/settings' }, t('navSettings')));
  const header = h('header', { class: 'site-header' },
    h('div', { class: 'wrap header-inner' },
      h('a', { class: 'brand', href: '#/' }, h('span', { class: 'brand-mark', 'aria-hidden': 'true' }, 'R'),
        h('span', { class: 'brand-text' }, h('strong', {}, 'ReyZ TOCFL'), h('small', {}, 'Preparation Website'))),
      nav, h('div', { class: 'header-tools' }, themeBtn, menuBtn)));
  const footer = h('footer', { class: 'site-footer' },
    h('div', { class: 'wrap footer-inner' },
      h('div', {}, h('strong', {}, t('siteTitle')), h('div', { class: 'sig' }, t('createdBy')),
        h('p', { class: 'muted small' }, 'Materi belajar: 當代中文課程 (A Course in Contemporary Chinese), NTNU Mandarin Training Center. Soal latihan: TOCFL mock tests, SC-TOP. Situs ini dibuat secara independen dan tidak berafiliasi dengan TOCFL/SC-TOP, NTNU, maupun penerbitnya.')),
      h('ul', { class: 'social', 'aria-label': 'Media sosial Reynard Agahari' },
        ...SOCIAL.map((s) => h('li', {}, h('a', { href: s.url, target: '_blank', rel: 'noopener noreferrer' }, `${s.name} ${s.handle}`))))));
  const main = h('main', { id: 'main', tabindex: '-1' });
  $('#app').append(header, main, footer);
}

async function render() {
  const { parts, query } = parseHash();
  const main = $('#main');
  const m = match(parts);
  document.querySelectorAll('[data-nav]').forEach((a) => {
    const href = a.getAttribute('data-nav');
    const cur = '#/' + (parts[0] || '');
    a.toggleAttribute('aria-current', href === cur || (href === '#/study' && ['book', 'lesson', 'page'].includes(parts[0])) || (href === '#/exercise' && ['test', 'result', 'section'].includes(parts[0])));
  });
  $('#nav').classList.remove('open');
  main.replaceChildren(h('div', { class: 'wrap loading' }, t('loading')));
  try {
    const node = m ? await m.view(m.params, query) : notFound();
    main.replaceChildren(node);
  } catch (e) {
    console.error(e);
    main.replaceChildren(h('div', { class: 'wrap' }, h('div', { class: 'card error' }, h('h1', {}, 'Konten tidak dapat dimuat'), h('p', {}, String(e.message || e)), h('a', { href: '#/' }, 'Kembali ke beranda'))));
  }
  if (!query.has('keep')) window.scrollTo(0, 0);
  const h1 = main.querySelector('h1');
  document.title = (h1 ? h1.textContent + ' · ' : '') + t('siteTitle');
  main.focus({ preventScroll: true });
}

function notFound() {
  return h('div', { class: 'wrap' }, h('h1', {}, 'Halaman tidak ditemukan'), h('a', { href: '#/' }, 'Kembali ke beranda'));
}

applyPrefs();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyPrefs);
shell();
window.addEventListener('hashchange', render);
render();
