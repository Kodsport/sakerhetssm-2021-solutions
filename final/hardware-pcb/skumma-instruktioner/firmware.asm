.include "m328Pdef.inc"
.equ UNLOCKH = 0b10010101
.equ UNLOCKL = 0b11100010

init:
    ; init stack
    ldi r16, high(RAMEND)
    out SPH, r16
    ldi r16, low(RAMEND)
    out SPL, r16

    ; init pins
    ldi r16, 0b11000001
    out PORTB, r16
    ldi r16, 0b11000110
    out DDRB, r16
    ldi r16, 0b00000001
    out DDRC, r16
    ldi r16, 0xff
    out PORTD, r16
    ldi r16, 0x00
    out DDRD, r16

    ; init timer
    ldi r16, 0x20
    sts ICR1H, r16
    ldi r16, 0x00
    sts ICR1L, r16
    ldi r16, 0x02
    sts OCR1AH, r16
    ldi r16, 0x00
    sts OCR1AL, r16
    ldi r16, 0b10000011
    sts TCCR1A, r16

    ; init eeprom
    ldi r16, 0
    out EEARH, r16
    out EEARL, r16
    sbi EECR, EERE
    in r29, EEDR

    ; enable logic LEDs if unlocked
    cpi r29, 0
    breq main
    cbi PORTB, 6
    cbi PORTB, 7

    jmp main

delay:
    dec r16
    cpi r16, 0
    brne delay
    dec r17
    cpi r17, 0
    brne delay
    dec r18
    cpi r18, 0
    brne delay
    ret

beep_delay:
    ldi r16, 255
    ldi r17, 255
    ldi r18, 1
    call delay
    ret

beep_char:
    ldi r17, 128

beep_char_main:
    mov r18, r16
    and r18, r17
    push r16
    push r17
    cpi r18, 0
    brne beep_char_on
    ldi r16, 0b00000000
    sts TCCR1B, r16
    jmp beep_char_main_cont

beep_char_on:
    ldi r16, 0b00001010
    sts TCCR1B, r16

beep_char_main_cont:
    call beep_delay
    pop r17
    pop r16
    lsr r17
    cpi r17, 0
    brne beep_char_main
    ldi r16, 0b00000000
    sts TCCR1B, r16
    ret

beep_string:
    lpm r16, Z+

beep_string_main:
    call beep_char
    lpm r16, Z+
    cpi r16, 0
    brne beep_string_main
    ret

wrongsleep:
    ldi r16, 255
    ldi r17, 255
    ldi r18, 32
    call delay

main:
    ; wait for button
    in r16, PINB
    andi r16, 1
    cpi r16, 0
    brne main

    ; read DIP switches
    sbi PORTB, 6
    cbi PORTB, 7
    nop
    nop
    in r16, PIND
    sbi PORTB, 7
    cbi PORTB, 6
    nop
    nop
    in r17, PIND
    sbi PORTB, 6

    ; check if device is locked
    cpi r29, 0
    brne unlocked
    
    ; check for unlocking combination
    ldi r18, UNLOCKH
    cpi r16, UNLOCKL
    cpc r17, r18
    brne wrongsleep

    ; write to eeprom that the device is unlocked now
    inc r29
    out EEDR, r29
    sbi EECR, EEMPE
    sbi EECR, EEPE

    unlocked:
    ; enable logic LEDs
    cbi PORTB, 6
    cbi PORTB, 7

    ; delay before starting to beep
    push r16
    push r17
    ldi r16, 255
    ldi r17, 255
    ldi r18, 16
    call delay
    pop r17
    pop r16

    hardware_check:
    ldi r18, UNLOCKH
    cpi r16, UNLOCKL
    cpc r17, r18
    brne logic_check

    hardware_flag:
    sbi PORTB, 2
    ldi ZH, high(2*sync_tone)
    ldi ZL, low(2*sync_tone)
    call beep_string
    ldi ZH, high(2*flag1)
    ldi ZL, low(2*flag1)
    call beep_string
    cbi PORTB, 2
    jmp main

    logic_check:
    ldi r18, LOGICH
    cpi r16, LOGICL
    cpc r17, r18
    breq logic_flag

    ldi r18, LOGICH ^ 0xff
    cpi r16, LOGICL ^ 0xff
    cpc r17, r18
    brne instruction_check

    logic_flag:
    ldi ZH, high(2*sync_tone)
    ldi ZL, low(2*sync_tone)
    call beep_string
    ldi ZH, high(2*flag2)
    ldi ZL, low(2*flag2)
    call beep_string
    jmp main

    instruction_check:
    ldi r18, 0
    ldi r19, 0
    ldi r20, 0

    loop:
    sbrs r18, 0
    jmp loop1
    com r16

    loop1:
    sbrs r18, 1
    jmp loop2
    com r17

    loop2:
    sbrs r18, 2
    jmp loop3
    inc r16

    loop3:
    sbrs r18, 3
    jmp loop4
    dec r17
    dec r17

    loop4:
    sbrs r18, 4
    jmp loop5
    swap r16

    loop5:
    sbrs r18, 5
    jmp loop6
    clc
    rol r16
    rol r16
    rol r16
    rol r16
    rol r17
    rol r17
    rol r17
    rol r17
    rol r16
    rol r16
    rol r16
    rol r16
    rol r16

    loop6:
    sbrs r18, 6
    jmp loop7
    eor r16, r17

    loop7:
    sbrs r18, 7
    jmp loopfinal
    swap r17

    loopfinal:
    inc r18
    cpse r18, r19
    jmp loop

    ldi r18, 0b10011001
    cpi r16, 0b01100101
    cpc r17, r18
    brne default_path

    instruction_flag:
    sbi PORTC, 0
    ldi ZH, high(2*sync_tone)
    ldi ZL, low(2*sync_tone)
    call beep_string
    ldi ZH, high(2*flag3)
    ldi ZL, low(2*flag3)
    call beep_string
    cbi PORTC, 0
    jmp main

    default_path:
    ldi ZH, high(2*sync_tone)
    ldi ZL, low(2*sync_tone)
    call beep_string
    ldi ZH, high(2*default_msg)
    ldi ZL, low(2*default_msg)
    call beep_string

    jmp main

sync_tone: .DB 0xf0, 0xf0, 0xf0, 0xf0, 0
default_msg: .DB "incorrect code", 0
.include "secret.asm" # contains flag1, flag2, flag3, LOGICH and LOGICL

.ESEG
.DB 0
