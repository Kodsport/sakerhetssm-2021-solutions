#!/usr/bin/env python3
from Crypto.Cipher import AES
import base64

with open("key", "rb") as f:
    key = f.read()

cipher = AES.new(key, AES.MODE_ECB)

def encrypt(m):
    if len(m) % 2 == 1:
        m += b"\0"
    c = b""
    for i in range(0, len(m), 2):
        c += cipher.encrypt(m[i:i+2] + b"\0"*14)[:4]
    return c

def banner():
    print("""S.       .S    sSSSSs   .S    S.   sdSS_SSSSSSbs   .S     S.     sSSs   .S    sSSSSs   .S    S.   sdSS_SSSSSSbs         .S_SSSs      sSSs    sSSs  
SS.     .SS   d%%%%SP  .SS    SS.  YSSS~S%SSSSSP  .SS     SS.   d%%SP  .SS   d%%%%SP  .SS    SS.  YSSS~S%SSSSSP        .SS~SSSSS    d%%SP   d%%SP  
S%S     S%S  d%S'      S%S    S%S       S%S       S%S     S%S  d%S'    S%S  d%S'      S%S    S%S       S%S             S%S   SSSS  d%S'    d%S'    
S%S     S%S  S%S       S%S    S%S       S%S       S%S     S%S  S%S     S%S  S%S       S%S    S%S       S%S             S%S    S%S  S%S     S%|     
S&S     S&S  S&S       S%S SSSS%S       S&S       S%S     S%S  S&S     S&S  S&S       S%S SSSS%S       S&S             S%S SSSS%S  S&S     S&S     
S&S     S&S  S&S       S&S  SSS&S       S&S       S&S     S&S  S&S_Ss  S&S  S&S       S&S  SSS&S       S&S             S&S  SSS%S  S&S_Ss  Y&Ss    
S&S     S&S  S&S       S&S    S&S       S&S       S&S     S&S  S&S~SP  S&S  S&S       S&S    S&S       S&S             S&S    S&S  S&S~SP  `S&&S   
S&S     S&S  S&S sSSs  S&S    S&S       S&S       S&S     S&S  S&S     S&S  S&S sSSs  S&S    S&S       S&S             S&S    S&S  S&S       `S*S  
S*b     S*S  S*b `S%%  S*S    S*S       S*S       S*S     S*S  S*b     S*S  S*b `S%%  S*S    S*S       S*S             S*S    S&S  S*b        l*S  
S*S.    S*S  S*S   S%  S*S    S*S       S*S       S*S  .  S*S  S*S.    S*S  S*S   S%  S*S    S*S       S*S             S*S    S*S  S*S.      .S*P  
 SSSbs  S*S   SS_sSSS  S*S    S*S       S*S       S*S_sSs_S*S   SSSbs  S*S   SS_sSSS  S*S    S*S       S*S             S*S    S*S   SSSbs  sSS*S   
  YSSP  S*S    Y~YSSY  SSS    S*S       S*S       SSS~SSS~S*S    YSSP  S*S    Y~YSSY  SSS    S*S       S*S             SSS    S*S    YSSP  YSS'    
        SP                    SP        SP                             SP                    SP        SP                     SP                   
        Y                     Y         Y                              Y                     Y         Y                      Y                    
                                                                                                                                                   """)
    print("------------------------------------------------------------------------------------------------------------------------------------------")

def main():
    banner()

    with open("flag", "rb") as f:
        flag = f.read()

    cflag = encrypt(flag)
    print("here is flag:", base64.b64encode(cflag).decode())

    for _ in range(1000):
        x = input(">")
        x = base64.b64decode(x)
        print(base64.b64encode(encrypt(x)).decode())

if __name__ == "__main__":
    main()
