<script>
    export let data;
    import Row from "./Row.svelte";
</script>

<h1>Scoreboard</h1>
<table style="width:100%">
    <tr>
        <th>Team Name</th><th>Time</th><th>Ticks</th><th>Stars</th>
    </tr>
    {#await data}
        <th>Loading</th><th>Loading</th><th>Loading</th><th>Loading</th>
    {:then res}
        {#each res.scoreboard as row}
            <Row {row} />
        {/each}
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}
</table>
