CC = gcc
CFLAGS  = -g -Wall -Wpedantic

TARGET = saruman

all: $(TARGET)

flag.c: generate.py
	python3 generate.py > flag.c

$(TARGET): $(TARGET).c flag.c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c flag.c

clean:
	$(RM) $(TARGET)
