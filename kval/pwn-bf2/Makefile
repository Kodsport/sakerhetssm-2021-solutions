

bf2: bf2.c
	gcc $< -o container/$@

docker: container/bf2
	docker build -t bf2 container
