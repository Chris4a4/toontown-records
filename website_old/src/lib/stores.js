import { writable } from 'svelte/store';
import { browser } from "$app/environment"

let persistedToken = browser && localStorage.getItem('discordToken')
export let discordToken = writable(persistedToken)

if (browser) {
    discordToken.subscribe(u => localStorage.discordToken = u)
}

export let discordId = writable(null)
export let discordAvatar = writable(null)
