<script>
  import { onMount } from 'svelte';
  import { discordToken } from '$lib/stores.js';
  import { goto } from '$app/navigation';
  
  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
  
    if (code) {
      const result = await fetch(`${import.meta.env.VITE_API_URL}/api/register/${code}`);
      const { data: data} = await result.json();

      if (data) {
        discordToken.set(data);
      }
    }

    goto('/');
  });
</script>
