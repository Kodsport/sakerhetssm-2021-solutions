package main

import (
	"database/sql"
	"fmt"

	// Postgresql database driver
	_ "github.com/jackc/pgx/v4/stdlib"
)

const (
	host     = "localhost"
	port     = 5432
	user     = "postgres"
	password = "8Vsrej7NjVWJqjQ2vrMDqhfBci6RJFf7"
	dbname   = "i"
)

func init_database() *sql.DB {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+"password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
	db, err := sql.Open("pgx", psqlInfo)
	if err != nil {
		panic(err)
	}
	//defer db.Close()
	createTables(db)
	return db
}

func createTables(db *sql.DB) {
	if _, err := db.Exec(`CREATE TABLE IF NOT EXISTS posts(
		id integer PRIMARY KEY,
		title varchar(256) NOT NULL,
		text varchar(256) NOT NULL
	);`); err != nil {
		panic(err)
	}
	// test posts
	if _, err := db.Exec(`DELETE FROM posts;`); err != nil {
		panic(err)
	}
	if _, err := db.Exec(`INSERT INTO posts(id, title, text) VALUES (0, 'Första blogposten!', 'Hej nya bloggen!');`); err != nil {
		panic(err)
	}
	if _, err := db.Exec(`INSERT INTO posts(id, title, text) VALUES (1, 'Min katt!', 'Idag gick jag ut med min katt i det fina vädret. Det är vår snart, så kul!');`); err != nil {
		panic(err)
	}
	if _, err := db.Exec(`INSERT INTO posts(id, title, text) VALUES (2, 'Semlor!!!!!', 'Idag bakade jag semlor! Det var jättegott. Det är inte ens Februari men semlor är gott så whatever.');`); err != nil {
		panic(err)
	}
	if _, err := db.Exec(`CREATE TABLE IF NOT EXISTS hemlis_jcndsf(
		hemlis_laqws varchar(256)
	);`); err != nil {
		panic(err)
	}
	if _, err := db.Exec(`DELETE FROM hemlis_jcndsf;`); err != nil {
		panic(err)
	}
	if _, err := db.Exec(`INSERT INTO hemlis_jcndsf(hemlis_laqws) VALUES ('SSM{åh_nej_ni_hittade_min_hemlis}');`); err != nil {
		panic(err)
	}
}

func getAllPosts(db *sql.DB) []string {
	var titleList []string
	rows, err := db.Query("SELECT title FROM posts")
	if err != nil {
		panic(err)
	}
	defer rows.Close()
	for rows.Next() {
		var title string
		err = rows.Scan(&title)
		if err != nil {
			panic(err)
		}
		titleList = append(titleList, title)
	}
	return titleList
}

func getBlogPostUnsafe(db *sql.DB, id string) (string, string) {
	// BAD CODE. Don't do this at home
	var title, text string
	queryStringTitle := "SELECT title, text FROM posts WHERE id=" + id + ";"
	row := db.QueryRow(queryStringTitle)
	row.Scan(&title, &text)
	return title, text
}
