<script>
    import Input from "./Input.svelte";
    import Result from "./Result.svelte";
    import Textarea from "./Textarea.svelte";
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

    function run(data) {
        result = {
            status: "loading",
        };
        fetch(__url + "/simulate", {
            body: JSON.stringify(data),
            method: "POST",
        })
            .then((r) => r.json())
            .then((r) => (result = r));
    }
    let result = {};

    const fieldsToObject = (fields) =>
        fields.reduce(
            (p, c) => ({
                ...p,
                [c.name]: c.value,
            }),
            {}
        );

    const handleSubmit = () => run(fieldsToObject(fields));
</script>

<form on:submit|preventDefault={() => handleSubmit(fields)}>
    {#each fields as field}
        {#if field.type === "Input"}
            <Input
                bind:value={field.value}
                label={field.label}
                placeholder={field.placeholder}
            />
        {/if}
        {#if field.type === "Textarea"}
            <Textarea
                bind:value={field.value}
                label={field.label}
                placeholder={field.placeholder}
            />
        {/if}
    {/each}
    <button type="submit">Submit</button>
</form>
<Result {result} />

<style>
    :global(input, select) {
        margin: 5px;
    }
</style>
