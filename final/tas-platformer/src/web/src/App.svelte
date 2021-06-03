<script lang="ts">
    import Form from "./Form.svelte";
    import Scoreboard from "./Scoreboard.svelte";
    import Rules from "./Rules.svelte";
    let data = fetch(__url + "/scoreboard").then((r) => r.json());
    let update_scoreboard = () =>
        (data = fetch(__url + "/scoreboard").then((r) => r.json()));
    let value = "";
    let fields = [
        {
            name: "team_name",
            type: "Input",
            value: "",
            placeholder: "Enter team name...",
            label: "Team name",
        },
        {
            name: "code",
            type: "Textarea",
            value: "",
            placeholder: "Paste saved data...",
            label: "Saved speedrun",
        },
    ];
    let selected = "Scoreboard";
</script>

<main>
    <h1>Hello Gamer!</h1>
    <p>
        Submit your speedruns for a chance to be on the scoreboard and win some
        flags.
    </p>
    <ul id="select">
        <li>
            <a
                href="/"
                on:click|preventDefault={() => {
                    selected = "Scoreboard";
                    update_scoreboard();
                }}>Scoreboard</a
            >
        </li>
        |
        <li>
            <a href="/" on:click|preventDefault={() => (selected = "Submit")}
                >Submit</a
            >
        </li>
        |
        <li>
            <a href="/" on:click|preventDefault={() => (selected = "Rules")}
                >Rules</a
            >
        </li>
    </ul>
    {#if selected == "Scoreboard"}
        <Scoreboard {data} />
    {:else if selected == "Submit"}
        <Form />
    {:else if selected == "Rules"}
        <Rules />
    {:else}
        <p>404</p>
    {/if}
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }
    ul#select li {
        display: inline;
    }
    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
        font: bold;
        text-align: center;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>
