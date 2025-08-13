### Idea : 

    Kinda near to UAF bug but it's just a logic bug that allows you call win function
    1. Creates Data packet
    2. Edit this data packet with the win function address at the offset of handler() at ControlPacket (+8)
    3. Upgrades the data packet to be a control packet
    4. Process the control packet to call win


docker build -t babypwn . 
docker run -d --rm --name babypwn -p 8000:8000 babypwn
