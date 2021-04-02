#include <gb/gb.h>
#include <gb/console.h>
#include <gb/drawing.h>
#include <time.h>
#include <stddef.h>

#include "background-tiles.h"
#include "background-map.h"
#include "font-alpha.h"

#define CHAR_BLANK 65

void main() {
    DISPLAY_ON;
    HIDE_WIN;
    SHOW_SPRITES;
    SHOW_BKG;
    wait_vbl_done();
    //scroll_bkg(4,4);
    set_bkg_data(0x00, 0x02, background);
    set_bkg_tiles(0x00, 0x00, background_mapWidth, background_mapHeight, background_map);

    set_sprite_data(0x00, CHAR_BLANK, FontAlpha);
    
    UINT8 i;

    for(i = 0; i < 10; i++) {
        move_sprite(i, 8*(i+3), 8*8);
        set_sprite_tile(i, CHAR_BLANK);
    }

    for(i = 10; i < 20; i++) {
        move_sprite(i, 8*(i-10+3), 10*8);
        set_sprite_tile(i, CHAR_BLANK);
    }

    time_t t0 = time(NULL);
    //"WELL DONE";
    for(i = 0; i < 20; i++) {
        set_sprite_tile(i, CHAR_BLANK);
    }
    set_sprite_tile(0, 'W'-'A');
    set_sprite_tile(1, 'E'-'A');
    set_sprite_tile(2, 'L'-'A');
    set_sprite_tile(3, 'L'-'A');

    set_sprite_tile(15, 'D'-'A');
    set_sprite_tile(16, 'O'-'A');
    set_sprite_tile(17, 'N'-'A');
    set_sprite_tile(18, 'E'-'A');
    
    while(time(NULL) - t0 < 1);
    t0 = time(NULL);
    
    for(i = 0; i < 20; i++) {
        set_sprite_tile(i, CHAR_BLANK);
    }
    set_sprite_tile(0, 'T'-'A');
    set_sprite_tile(1, 'H'-'A');
    set_sprite_tile(2, 'E'-'A');

    set_sprite_tile(14, 'F'-'A');
    set_sprite_tile(15, 'L'-'A');
    set_sprite_tile(16, 'A'-'A');
    set_sprite_tile(17, 'G'-'A');

    while(time(NULL) - t0 < 1);
    t0 = time(NULL);
    
    for(i = 0; i < 20; i++) {
        set_sprite_tile(i, CHAR_BLANK);
    }
    set_sprite_tile(0, 'I'-'A');
    set_sprite_tile(1, 'S'-'A');

    set_sprite_tile(4, 'S'-'A');
    set_sprite_tile(5, 'S'-'A');
    set_sprite_tile(6, 'M'-'A');
    set_sprite_tile(7, 62);

    set_sprite_tile(11, 'G'-'A');
    set_sprite_tile(12, 'A'-'A');
    set_sprite_tile(13, 'M'-'A');
    set_sprite_tile(14, 'E'-'A');
    set_sprite_tile(15, 'B'-'A');
    set_sprite_tile(16, 'O'-'A');
    set_sprite_tile(17, 'Y'-'A');
    set_sprite_tile(18, 64);

    while(time(NULL) - t0 < 1);
    t0 = time(NULL);

    for(i = 0; i < 20; i++) {
        set_sprite_tile(i, CHAR_BLANK);
    }
    
    set_sprite_tile(0, 'L'-'A');
    set_sprite_tile(1, 'C'-'A');
    set_sprite_tile(2, 'D'-'A');
    set_sprite_tile(3, 64);
    set_sprite_tile(4, 'F'-'A');
    set_sprite_tile(5, 'U'-'A');
    set_sprite_tile(6, 'N'-'A');
    set_sprite_tile(7, 63);
    
}
