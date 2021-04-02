CC = gcc
CFLAGS  = -g -Wall -Wpedantic

TARGET = speak_friend_and_enter

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c

clean:
	$(RM) $(TARGET)
