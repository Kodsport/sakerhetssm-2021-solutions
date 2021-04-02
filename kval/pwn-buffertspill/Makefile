flags := -no-pie -fno-stack-protector

buffertspill: buffertspill.c
	gcc $< $(flags) -o container/$@

docker: container/buffertspill
	docker build -t buffertspill container
