#! /bin/bash


#Two tries at once
    python3 encoder.py demofile.txt && python3 client.py --input_file channel_input.txt --output_file channel_output.txt --srv_hostname=iscsrv72.epfl.ch --srv_port=80 && python3 decoder.py > result.txt
    diff -s testfile.txt result.txt
    sleep 45
    python3 encoder.py demofile.txt && python3 client.py --input_file channel_input.txt --output_file channel_output.txt --srv_hostname=iscsrv72.epfl.ch --srv_port=80 && python3 decoder.py > result.txt
