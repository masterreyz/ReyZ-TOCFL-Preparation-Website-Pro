// Interface strings. Indonesian is the default UI language; add another locale object to translate.
const id = {
  siteTitle: 'ReyZ TOCFL Preparation Website',
  createdBy: 'Created by Reynard Agahari',
  navHome: 'Beranda', navStudy: 'TOCFL Study', navExercise: 'TOCFL Exercise', navReview: 'Ulas Kesalahan',
  navBookmarks: 'Penanda', navHistory: 'Riwayat', navSearch: 'Cari', navAbout: 'Tentang', navSettings: 'Pengaturan',
  continue: 'Lanjutkan belajar', start: 'Mulai', submit: 'Kumpulkan jawaban', next: 'Berikutnya', prev: 'Sebelumnya',
  correct: 'Benar', incorrect: 'Salah', unanswered: 'Tidak dijawab', ungradable: 'Tidak dapat dinilai',
  yourAnswer: 'Jawaban Anda', correctAnswer: 'Jawaban benar', transcript: 'Transkrip', fullScript: 'Transkrip lengkap (resmi)',
  practice: 'Mode Latihan', exam: 'Mode Simulasi Tes', listening: 'Listening (Mendengar)', reading: 'Reading (Membaca)',
  markComplete: 'Tandai selesai', completed: 'Selesai', bookmark: 'Tandai', bookmarked: 'Ditandai',
  play: 'Putar', pause: 'Jeda', replay: 'Ulangi', speed: 'Kecepatan', loading: 'Memuat…',
  audioError: 'Audio tidak dapat dimuat. Pastikan file audio sudah disalin (npm run sync-media) atau periksa mediaBase di config.js.',
  localOnly: 'Progres disimpan di browser dan perangkat ini saja (localStorage). Progres tidak tersinkron antarperangkat — gunakan Ekspor/Impor untuk memindahkannya.',
};
export const t = (k) => id[k] ?? k;
export const BAND_LABEL = { novice: 'Band Novice', a: 'Band A', b: 'Band B', c: 'Band C' };
export const BAND_DESC = {
  novice: 'Tingkat persiapan (準備級)', a: 'Tingkat 1–2 (入門級・基礎級)', b: 'Tingkat 3–4 (進階級・高階級)', c: 'Tingkat 5–6 (流利級・精通級)',
};
