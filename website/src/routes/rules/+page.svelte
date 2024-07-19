<script>
  export let data;
</script>

{#if data}
  {data.leaderboardData.num_records}
{:else}
  LOADING
{/if}