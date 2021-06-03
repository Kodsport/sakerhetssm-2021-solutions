<script>
    export let row;
    const onestar = 3500;
    const twostars = 2300;
    const threestars = 1600;
    const fourstars = 1400;
    let stars = (time) => {
        if (time < fourstars) return "🌟🌟🌟🌟";
        if (time < threestars) return "🌟🌟🌟★";
        if (time < twostars) return "🌟🌟★★";
        if (time < onestar) return "🌟★★★";
        return "★★★★";
    };
</script>

<tr>
    <th>{row[0]}</th>
    <th>{(row[1] / 60).toFixed(2)}</th>
    <th>{row[1]}</th>
    <th>{stars(row[1])}</th>
</tr>
