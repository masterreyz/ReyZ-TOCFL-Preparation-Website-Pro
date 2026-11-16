// Runtime configuration (edit after deployment without rebuilding).
// mediaBase: page images and question crops (deployed with the site).
// audioBase: original MP3 recordings. They are NOT deployed to GitHub Pages (≈3 GB).
//   originalAudio: 'auto' checks once whether audioProbe exists under audioBase:
//     found  -> original recordings are used (local use after `npm run sync-media`, or external hosting)
//     absent -> Mandarin speech synthesis (Web Speech API) reads the official scripts / lesson text instead.
//   Set true/false to force either mode.
window.REYZ_CONFIG = {
  mediaBase: './media/',
  audioBase: './media/audio/',
  originalAudio: 'auto',
  audioProbe: 'ex/a-l1/t003-1-01.mp3',
};
