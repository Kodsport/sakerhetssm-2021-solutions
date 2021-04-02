AS = lcc -c
CC = lcc -Wa-l -Wl-m

BIN = spy-game.gb
OBJS = spy-game.o background-map.o background-tiles.o font-alpha.o

all: $(BIN)

%.s: %.ms
	maccer -o $@ $<

$(BIN): $(OBJS)
	$(CC) -o $(BIN) $(OBJS)

clean:
	rm -rf $(BIN) $(OBJS) *~
