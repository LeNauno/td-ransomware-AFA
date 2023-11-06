mkdir -p token_data
docker run -it --rm --name ransomware \
    --net=ransomware-network \
    -v "$PWD"/sources:/root/ransomware:ro \
    -v "$PWD"/token_data:/root/token \
    -v "$PWD"/txt_folder:/root/myTxtfiles:rw \
    ransomware \
    python /root/ransomware/ransomware.py
