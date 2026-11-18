import { h } from '../util.js';
import { t } from '../i18n.js';
import { SOCIAL } from '../brand.js';

export async function aboutView() {
  return h('div', { class: 'wrap narrow' },
    h('h1', {}, 'Tentang & Kredit'),
    h('section', { class: 'card about-me' },
      h('div', { class: 'avatar', 'aria-hidden': 'true' }, 'RA'),
      h('div', {}, h('h2', {}, t('siteTitle')), h('p', { class: 'sig' }, t('createdBy')),
        h('p', {}, 'Situs belajar pribadi untuk persiapan TOCFL (Test of Chinese as a Foreign Language) — materi belajar A1–C2 dan latihan listening & reading Band Novice, A, B, dan C.'),
        h('ul', { class: 'social' }, ...SOCIAL.map((s) => h('li', {}, h('a', { href: s.url, target: '_blank', rel: 'noopener noreferrer' }, `${s.name}: ${s.handle}`)))))),
    h('p', { class: 'note' }, t('localOnly')));
}
