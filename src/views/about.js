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
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Sumber materi'),
      h('ul', {},
        h('li', {}, h('strong', {}, 'TOCFL Study: '), '當代中文課程 / A Course in Contemporary Chinese, jilid 1–6 (Textbook & Workbook) beserta audionya. Pemimpin redaksi 鄧守信 (Shou-Hsin Teng); disusun oleh 國立臺灣師範大學國語教學中心 (Mandarin Training Center, NTNU); diterbitkan oleh 聯經出版 (Linking Publishing).'),
        h('li', {}, h('strong', {}, 'TOCFL Exercise: '), 'Mock test (模擬試題) TOCFL listening & reading beserta kunci jawaban, naskah dengar, dan audio, dari 國家華語測驗推動工作委員會 (SC-TOP).')),
      h('p', {}, 'Hak cipta seluruh materi di atas tetap milik pemegang hak masing-masing. Branding “ReyZ” dan nama Reynard Agahari hanya menandai pembuat situs ini — bukan penulis buku atau soal, dan situs ini tidak berafiliasi resmi dengan TOCFL/SC-TOP, NTNU, maupun Linking Publishing.')),
    h('section', { class: 'card' }, h('h2', { class: 'h3' }, 'Catatan akurasi'),
      h('ul', { class: 'small' },
        h('li', {}, 'Penilaian memakai kunci jawaban resmi yang disertakan. Soal yang kuncinya tidak dapat diverifikasi ditandai “tidak dapat dinilai” dan tidak dihitung.'),
        h('li', {}, 'Skor yang ditampilkan adalah skor mentah dan persentase — bukan skor skala resmi TOCFL atau hasil sertifikasi.'),
        h('li', {}, 'Teks soal diekstrak otomatis dari PDF; tampilan asli setiap soal selalu tersedia untuk pembanding.'),
        h('li', {}, 'Transkrip berasal dari naskah dengar resmi. Penempatan transkrip per soal dilakukan otomatis; transkrip lengkap resmi tersedia di halaman hasil.'))),
    h('p', { class: 'note' }, t('localOnly')));
}
