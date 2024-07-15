<script>
  import { onMount } from 'svelte';

  let leaderboard_data = null;
  let user_dict = null;

  async function getLeaderboards() {
    const result = await fetch(`${import.meta.env.VITE_API_URL}/api/leaderboards`);
    const { data: leaderboard_data} = await result.json();

    return leaderboard_data;
  }

  async function getUsers() {
    const result = await fetch(`${import.meta.env.VITE_API_URL}/api/users`);
    const { data: user_dict} = await result.json();

    return user_dict;
  }

  onMount(async () => {
  leaderboard_data = await getLeaderboards();

  user_dict = await getUsers();
  user_dict = Object.entries(user_dict).reduce((acc, [key, value]) => (acc[value] = key, acc), {})
  });
</script>

<div class="leaderboard-container">
  {#if leaderboard_data && user_dict}
    <h2>Toontown Rewritten Leaderboard</h2>
    <ol>
      {#each leaderboard_data.leaderboard as user}
        <li>
          {user_dict[user['user_id']]}
        </li>
      {/each}
    </ol>
  {:else}
    <p>Loading...</p>
  {/if}
</div>