CC = gcc
CFLAGS  = -g -Wall -Wpedantic

TARGET = witch_king_of_angmar

all: $(TARGET)

flag.c: generate.py
	python3 generate.py > flag.c

$(TARGET): $(TARGET).c flag.c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c flag.c
	strip $(TARGET)

clean:
	$(RM) $(TARGET)
