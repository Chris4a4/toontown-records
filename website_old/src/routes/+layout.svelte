<script>
  import "../app.css";
  import Nav from '$lib/components/Nav.svelte';
  import { onMount } from 'svelte';
  import { discordToken, discordId, discordAvatar } from '$lib/stores.js';

  onMount(async () => {
    discordToken.subscribe(async (value) => {
      const result = await fetch(`${import.meta.env.VITE_API_URL}/api/get_info/${value}`);
      const { data: data} = await result.json();

      if (data) {
        discordId.set(data.id);
        discordAvatar.set(`https://cdn.discordapp.com/avatars/${data.id}/${data.avatar}.png`)
      }
    });
  });
</script>

<main>
  <!-- Content for large screens and above -->
  <div class="hidden xl:block">
    <Nav />
    <slot />
  </div>

  <!-- Message for smaller screens -->
  <div class="block xl:hidden">
    Mobile currently not supported
  </div>
</main>