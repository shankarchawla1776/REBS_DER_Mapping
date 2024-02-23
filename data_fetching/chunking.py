def chunk(chunk): 
    for i in chunk: 
        print(i)

chunk_size = 10 

with open('data.txt', 'r') as f:
    while True: 
        chunk = [next(f) for i in range(chunk_size)]

        if not chunk: 
            break

        chunk(chunk)