<script>
  import { valueString } from '$lib/recordMetadata.js';

  export let data;
</script>

<div>
  {#each data.recordData as record}
    <article class="record">
      <h2>{record.record_name}</h2>
      {#if record.top3.length}
        <ol>
          {#each record.top3 as submission}
            <li>
              <span class="users">{submission.user_ids.map(id => data.usersData[id]).join(", ")}</span>
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
</div>