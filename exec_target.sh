docker run -it --rm --name ransomware \
    --net=ransomware-network \
    -v "$PWD"/sources:/root/ransomware:ro \
    -v "$PWD"/dist:/root/bin:ro \
    -v "$PWD"/txt_folder:/root/myTxtfiles:rw \
    ransomware \
    /bin/bash
