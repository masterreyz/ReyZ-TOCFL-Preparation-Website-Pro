// Local progress storage (browser localStorage). Versioned, failure-tolerant, exportable.
const KEY = 'reyz-tocfl-v1';
const empty = () => ({
  version: 1,
  prefs: { theme: 'auto', fontScale: 1, showPinyin: true, ttsVoice: null, speechRate: 0.85 },
  lessons: {},        // lessonId -> { completed: bool, lastVisited: ts }
  lastLesson: null,   // { id, title, href, ts }
  bookmarks: {},      // key -> { type, title, href, ts }
  inProgress: {},     // testId -> { mode, answers:{n:letter}, startedAt, elapsed }
  attempts: [],       // [{ id, testId, title, mode, answers, score:{...}, submittedAt, durationSec }]
  pagesSeen: {},      // bookId -> last page
});

let state = load();
let storageOk = true;
const listeners = new Set();

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return empty();
    const s = JSON.parse(raw);
    return { ...empty(), ...s, prefs: { ...empty().prefs, ...(s.prefs || {}) } };
  } catch {
    storageOk = false;
    return empty();
  }
}

function persist() {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
    storageOk = true;
  } catch (e) {
    storageOk = false;
    console.warn('Progress could not be saved', e);
  }
  listeners.forEach((fn) => fn(state));
}

export const store = {
  get: () => state,
  ok: () => storageOk,
  onChange: (fn) => listeners.add(fn),
  update(fn) { fn(state); persist(); },
  setPref(k, v) { state.prefs[k] = v; persist(); },
  // lessons
  visitLesson(id, title, href) {
    state.lessons[id] = { ...(state.lessons[id] || {}), lastVisited: Date.now() };
    state.lastLesson = { id, title, href, ts: Date.now() };
    persist();
  },
  setCompleted(id, v) { state.lessons[id] = { ...(state.lessons[id] || {}), completed: v }; persist(); },
  isCompleted: (id) => !!state.lessons[id]?.completed,
  // bookmarks
  toggleBookmark(key, data) {
    if (state.bookmarks[key]) delete state.bookmarks[key];
    else state.bookmarks[key] = { ...data, ts: Date.now() };
    persist();
    return !!state.bookmarks[key];
  },
  isBookmarked: (key) => !!state.bookmarks[key],
  // tests
  getProgress: (testId) => state.inProgress[testId],
  saveProgress(testId, p) { state.inProgress[testId] = p; persist(); },
  clearProgress(testId) { delete state.inProgress[testId]; persist(); },
  addAttempt(a) { state.attempts.push(a); persist(); return a; },
  attempt: (id) => state.attempts.find((a) => a.id === id),
  attemptsFor: (testId) => state.attempts.filter((a) => a.testId === testId),
  // export / import / reset
  exportJson: () => JSON.stringify({ app: 'reyz-tocfl', exportedAt: new Date().toISOString(), data: state }, null, 1),
  importJson(text) {
    const obj = JSON.parse(text);
    const data = obj.data || obj;
    if (typeof data !== 'object' || !('attempts' in data)) throw new Error('File bukan ekspor progres ReyZ TOCFL.');
    // merge: keep attempts from both, prefer imported prefs/lessons
    const ids = new Set(state.attempts.map((a) => a.id));
    state = {
      ...empty(), ...state, ...data,
      attempts: [...state.attempts, ...(data.attempts || []).filter((a) => !ids.has(a.id))],
      lessons: { ...state.lessons, ...(data.lessons || {}) },
      bookmarks: { ...state.bookmarks, ...(data.bookmarks || {}) },
    };
    persist();
  },
  reset() { state = empty(); persist(); },
};
