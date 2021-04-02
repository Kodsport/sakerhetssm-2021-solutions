.include "m328Pdef.inc"

init:
    ldi r16, 0
    sts UBRR0H, r16
    ldi r16, 103
    sts UBRR0L, r16
    ldi r16, (1<<RXEN0)|(1<<TXEN0)
    sts UCSR0B, r16

    ldi ZH, high(2*encrypted)
    ldi ZL, low(2*encrypted)
    ldi r25, 0

loop:
    lds r16, UCSR0A
    sbrs r16, RXC0
    jmp loop
    lds r16, UDR0

    ldi r17, 0

    sbrc r16, 0
    sbr r17, 0b00010000

    sbrc r16, 1
    sbr r17, 0b00000010

    sbrc r16, 2
    sbr r17, 0b00100000

    sbrc r16, 3
    sbr r17, 0b00000001

    sbrc r16, 4
    sbr r17, 0b00000100

    sbrc r16, 5
    sbr r17, 0b01000000

    sbrc r16, 6
    sbr r17, 0b10000000

    sbrc r16, 7
    sbr r17, 0b00001000

    ldi r16, 0
    out EEARH, r16
    out EEARL, r17
    sbi EECR, EERE
    in r16, EEDR

    ldi r17, 69
    eor r16, r17

    lpm r17, Z+
    cp r16, r17
    brne fail

    inc r25
    cpi r25, 52
    breq success

    jmp loop

success:
    ldi r16, '1'
    sts UDR0, r16
    jmp halt

fail:
    ldi r16, '0'
    sts UDR0, r16

halt:
    jmp halt

encrypted: .DB 0xbb, 0xbb, 0xae, 0x6f, 0x3e, 0xde, 0xbe, 0x79, 0x67, 0x49, 0xde, 0x21, 0x67, 0x79, 0xf0, 0xde, 0x8d, 0x79, 0xf0, 0xde, 0x49, 0x79, 0xde, 0x47, 0xeb, 0xa4, 0xde, 0xb7, 0x11, 0x49, 0xde, 0xfb, 0x08, 0x59, 0xde, 0x3e, 0x0a, 0xde, 0x4b, 0x59, 0x2d, 0x49, 0x49, 0xc1, 0xde, 0x0a, 0x3e, 0x03, 0x4b, 0x6c, 0x2d, 0x76
