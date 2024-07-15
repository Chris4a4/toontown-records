<script>
    import { onMount } from 'svelte';
    import { valueString } from '$lib/recordMetadata.js';

    let record_data = null;
    let user_dict = null;

    async function getRecords() {
      const result = await fetch(`${import.meta.env.VITE_API_URL}/api/records`);
      const { data: record_data} = await result.json();

      return record_data;
    }

    async function getUsers() {
      const result = await fetch(`${import.meta.env.VITE_API_URL}/api/users`);
      const { data: user_dict} = await result.json();
    
      return user_dict;
    }
  
    onMount(async () => {
      record_data = await getRecords();

      user_dict = await getUsers();
      user_dict = Object.entries(user_dict).reduce((acc, [key, value]) => (acc[value] = key, acc), {})
    });
</script>

<div>
  {#if record_data && user_dict}
    {#each record_data as record}
      <article class="record">
        <h2>{record.record_name}</h2>
        {#if record.top3.length}
          <ol>
            {#each record.top3 as submission}
              <li>
                <span class="users">{submission.user_ids.map(id => user_dict[id]).join(", ")}</span>
                - 
                <a href={submission.evidence}>{valueString(submission, record.tags)}</a>
              </li>
            {/each}
          </ol>
        {:else}
          <p>N/A</p>
        {/if}
      </article>
    {/each}
  {:else}
    <p>Loading...</p>
  {/if}
</div>