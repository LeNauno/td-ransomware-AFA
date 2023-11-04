docker run -it --rm --name ransomware \
    --net=ransomware-network \
    -v "$PWD"/sources:/root/ransomware:ro \
    -v "$PWD"/dist:/root/bin:ro \
    ransomware \
    /bin/bash -c "python3 /root/ransomware/create_txt_files.py && /bin/bash"
