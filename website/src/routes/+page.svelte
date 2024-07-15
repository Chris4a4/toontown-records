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
            <b>{`${record.record_name}`}</b>
            {#if record.top3.length != 0}
                <br>
                {#each record.top3 as submission, i}
                  <b>{`${i + 1}.`}</b>
                  {submission.user_ids.map(user_id => user_dict[user_id]).join(", ")}
                  - 
                  <a href={submission.evidence}>asdf</a>
                  <br>
                {/each}
            {:else}
                <br>
                N/A
            {/if}
            <br>
            <br>
        {/each}
    {:else}
      Loading...
    {/if}
  </div>