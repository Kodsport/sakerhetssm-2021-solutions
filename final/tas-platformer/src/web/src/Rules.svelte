<script>
    const rules = [
        "No inappropriate teamname.",
        "No teaming with other teams.",
    ];
    const stars = [
        `- 🌟🌟🌟🌟 : solution <= 1400 ticks / ${(1400 / 60).toFixed(2)}s`,
        `- 🌟🌟🌟★ : solution <= 1600 ticks / ${(1600 / 60).toFixed(2)}s`,
        `- 🌟🌟★★ : solution <= 2300 ticks / ${(2300 / 60).toFixed(2)}s`,
        `- 🌟★★★ : solution <= 3500 ticks / ${(3500 / 60).toFixed(2)}s`,
        `- ★★★★ : solution <= 10000 tick /  ${(10000 / 60).toFixed(2)}s`,
    ];
</script>

<h2>Rules to follow:</h2>
<ul>
    {#each rules as rule}
        <li>{rule}</li>
    {/each}
</ul>
<h2>Stars:</h2>
<ul>
    {#each stars as star}
        <li>{star}</li>
    {/each}
</ul>
