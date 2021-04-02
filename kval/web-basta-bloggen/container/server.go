package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
)

var db *sql.DB

type post struct {
	title string
	text  string
}

var layout = `<!DOCTYPE html>
<html>
	<head>
		<style>
			body {
				background-image: url("yellow_flowers.jpg");
				color: brown;
			}

			a:link, a:visited {
				color: brown;
			}
		</style>
	</head>
	<body>
		<h1>Min Blogg!!!!!!</h1>
		<a href="/">Klicka på mig för att komma till förstasidan</a>
		<br>
		<br>
		<!--Replace with content-->
		<img src="cat_lick.gif" alt="slick slick">
		<p>Lev livet!</p>
	</body>
</html>`

func main() {
	db = init_database()
	// mux := http.NewServeMux()
	http.HandleFunc("/", displayAllPosts)
	http.HandleFunc("/posts", displayOnePost)
	http.HandleFunc("/cat_lick.gif", cat)
	http.HandleFunc("/yellow_flowers.jpg", flowers)
	http.ListenAndServe(":8080", nil)
	db.Close()
}

func flowers(w http.ResponseWriter, r *http.Request) {
	image, err := ioutil.ReadFile("yellow_flowers.jpg")
	if err != nil {
		panic(err)
	}
	w.Write(image)
}

func cat(w http.ResponseWriter, r *http.Request) {
	image, err := ioutil.ReadFile("cat_lick.gif")
	if err != nil {
		panic(err)
	}
	w.Write(image)
}

func displayAllPosts(w http.ResponseWriter, r *http.Request) {
	titleList := getAllPosts(db)
	var s string
	for i, t := range titleList {
		s = s + "<a href=\"/posts?id=" + strconv.Itoa(i) + "\">" + t + "</a><br><br>"
	}
	s = strings.ReplaceAll(layout, "<!--Replace with content-->", s)
	fmt.Fprint(w, s)
}

func displayOnePost(w http.ResponseWriter, r *http.Request) {
	id := r.FormValue("id")
	title, text := getBlogPostUnsafe(db, id)
	var s string
	s = strings.ReplaceAll(layout, "<!--Replace with content-->", "<h1>"+title+"</h1><p>"+text+"</p>")
	fmt.Fprint(w, s)
}
