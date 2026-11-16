// Accessible audio player with playlist support. Only one player sounds at a time; no autoplay.
import { h, fmtTime, audioUrl } from './util.js';
import { t } from './i18n.js';

const players = new Set();
export function stopAll(except) {
  players.forEach((p) => { if (p !== except && !p.paused) p.pause(); });
}
window.addEventListener('hashchange', () => stopAll());

/**
 * tracks: [{ src (relative audio path), label }]
 * opts: { title, exam (no seek/speed), compact }
 */
export function AudioPlayer(tracks, opts = {}) {
  const audio = new Audio();
  audio.preload = 'none';
  players.add(audio);
  let idx = 0;
  let playAll = !!opts.playAll;
  const titleEl = h('div', { class: 'ap-title' });
  const btn = h('button', { class: 'ap-btn', type: 'button', 'aria-label': t('play') }, '▶');
  const seek = h('input', { type: 'range', min: 0, max: 1000, value: 0, step: 1, class: 'ap-seek', 'aria-label': 'Posisi audio', disabled: opts.exam || null });
  const time = h('span', { class: 'ap-time', 'aria-live': 'off' }, '0:00 / --:--');
  const status = h('div', { class: 'ap-status', role: 'status' });
  const replay = h('button', { class: 'ap-small', type: 'button', 'aria-label': t('replay'), title: t('replay') }, '↺');
  const speed = h('select', { class: 'ap-speed', 'aria-label': t('speed') },
    ...[0.75, 0.9, 1, 1.15, 1.25, 1.5].map((r) => h('option', { value: r, selected: r === 1 || null }, `${r}×`)));
  const list = tracks.length > 1 ? h('ol', { class: 'ap-list' }) : null;

  function load(i, autoplay) {
    idx = i;
    audio.src = audioUrl(tracks[i].src);
    audio.playbackRate = Number(speed.value);
    titleEl.textContent = (opts.title ? opts.title + ' — ' : '') + (tracks[i].label || '');
    status.textContent = '';
    if (list) [...list.children].forEach((li, k) => li.classList.toggle('on', k === i));
    if (autoplay) play();
  }
  function play() {
    stopAll(audio);
    status.textContent = t('loading');
    audio.play().then(() => { status.textContent = ''; }).catch((e) => {
      if (e.name !== 'AbortError') status.textContent = t('audioError');
    });
  }
  btn.addEventListener('click', () => (audio.paused ? play() : audio.pause()));
  replay.addEventListener('click', () => { audio.currentTime = 0; play(); });
  speed.addEventListener('change', () => { audio.playbackRate = Number(speed.value); });
  seek.addEventListener('input', () => { if (isFinite(audio.duration)) audio.currentTime = (seek.value / 1000) * audio.duration; });
  audio.addEventListener('play', () => { btn.textContent = '❚❚'; btn.setAttribute('aria-label', t('pause')); });
  audio.addEventListener('pause', () => { btn.textContent = '▶'; btn.setAttribute('aria-label', t('play')); });
  audio.addEventListener('timeupdate', () => {
    time.textContent = `${fmtTime(audio.currentTime)} / ${fmtTime(audio.duration)}`;
    if (isFinite(audio.duration) && document.activeElement !== seek) seek.value = Math.round((audio.currentTime / audio.duration) * 1000);
  });
  audio.addEventListener('loadedmetadata', () => { time.textContent = `0:00 / ${fmtTime(audio.duration)}`; });
  audio.addEventListener('waiting', () => { status.textContent = t('loading'); });
  audio.addEventListener('playing', () => { status.textContent = ''; });
  audio.addEventListener('error', () => { status.textContent = t('audioError'); });
  audio.addEventListener('ended', () => {
    if (playAll && idx + 1 < tracks.length) load(idx + 1, true);
    opts.onEnded?.(idx);
  });

  if (list) {
    tracks.forEach((tr, i) => list.append(h('li', {}, h('button', { type: 'button', class: 'ap-track', onclick: () => load(i, true) }, tr.label || `Track ${i + 1}`))));
  }
  const allToggle = tracks.length > 1
    ? h('label', { class: 'ap-all' }, h('input', { type: 'checkbox', checked: playAll || null, onchange: (e) => { playAll = e.target.checked; } }), ' Putar berurutan')
    : null;
  load(0, false);
  const el = h('div', { class: 'audio-player' + (opts.compact ? ' compact' : ''), role: 'group', 'aria-label': opts.title || 'Pemutar audio' },
    titleEl,
    h('div', { class: 'ap-row' }, btn, seek, time, opts.exam ? null : replay, opts.exam ? null : speed),
    allToggle, status,
    list ? h('details', { class: 'ap-details' }, h('summary', {}, `Daftar trek (${tracks.length})`), list) : null);
  el.player = { audio, load, play, pause: () => audio.pause() };
  return el;
}
