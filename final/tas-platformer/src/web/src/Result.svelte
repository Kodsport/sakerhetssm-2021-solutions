<script>
    export let result;
</script>

{#if result.status != undefined}
    {#if result.status == "success"}
        <p>Success, time: {result.ticks / 60}</p>
        {#if result.flags.lenght != 0}
            <p>Here are some flags for you:</p>
            <ul>
                {#each result.flags as flag}
                    <li>{flag}</li>
                {/each}
            </ul>
        {/if}
    {:else if result.status == "loading"}
        <p>Loading</p>
    {:else}
        <p>Failed</p>
    {/if}
{/if}
