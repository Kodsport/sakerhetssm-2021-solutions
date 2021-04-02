
flags := -no-pie -Wl,-z,norelro

printf-i-en-loop: printf-i-en-loop.c
	gcc $< $(flags) -o container/$@

docker: container/printf-i-en-loop
	docker build -t printf-i-en-loop container
