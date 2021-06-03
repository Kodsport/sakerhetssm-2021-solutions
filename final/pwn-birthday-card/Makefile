flags := 

container/birthday-card: birthday-card.c
	gcc $< $(flags) -o $@

debug: birthday-card.c
	gcc $< $(flags) -o container/birthday-card -DDEBUG

clean:
	rm container/birthday-card

docker: container/birthday-card
	docker build -t birthday-card container

.PHONY: debug clean docker
