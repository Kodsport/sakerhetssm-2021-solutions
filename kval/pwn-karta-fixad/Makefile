
flags := -no-pie

karta-fixad: karta-fixad.c
	gcc -Wall -Wpedantic $< $(flags) -o container/$@

docker: container/karta-fixad
	docker build -t karta-fixad container
