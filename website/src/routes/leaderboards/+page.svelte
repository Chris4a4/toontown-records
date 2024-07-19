<script>
  export let data;
</script>

<div class="leaderboard-container">
  <h2>Toontown Rewritten Leaderboard</h2>
  <ol>
    {#each data.leaderboardData.leaderboard as user}
      <li>
        {data.usersData[user['user_id']]}
      </li>
    {/each}
  </ol>
</div>