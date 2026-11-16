// Removes the previous build output (assets/) so old hashed bundles don't pile up in the repo.
import { rmSync } from 'node:fs';
rmSync('assets', { recursive: true, force: true });
