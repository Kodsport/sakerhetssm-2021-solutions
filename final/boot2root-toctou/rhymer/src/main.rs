use std::io::Write;

const VOKALER: &str = "aoeuiyåäöaoeuiyåäö";

fn last_vowel_group(x: &str) -> &str {
    let mut n = 2;
    for (i, mut ch) in x.char_indices().rev() {
        ch.make_ascii_lowercase();
        if VOKALER.contains(ch) {
            n -= 1;
            if n == 0 {
                return &x[i..];
            }
        }
    }
    x
}

fn main() -> std::io::Result<()> {
    eprintln!("reversa mig inte plz");

    let data_path = std::path::Path::new("/home/guest/edata/words");
    let data = std::fs::read_to_string(data_path)?;
    let words = data.split("\n").collect::<Vec<_>>();

    let mut stdout = std::io::stdout();
    let stdin = std::io::stdin();
    stdout.write(b"Vad vill du rimma? ")?;
    stdout.flush()?;

    let mut inp = String::new();
    stdin.read_line(&mut inp)?;

    let inp = inp.trim_end();
    let group = last_vowel_group(inp);

    println!("Rim:");
    for word in words {
        if word.ends_with(group) {
            println!("> {}", word);
        }
    }
    Ok(())
}
