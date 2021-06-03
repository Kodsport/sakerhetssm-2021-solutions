flags := 

alloca-balloca: alloca-balloca.c
	gcc $< $(flags) -o container/$@

docker: container/alloca-balloca
	docker build -t alloca-balloca container
