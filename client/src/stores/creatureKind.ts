import { writable, type Writable } from 'svelte/store';

export let creatureKind: Writable<string> = writable('Enemies');
