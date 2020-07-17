from clf import Parser

def extract_path(child_conn):
    cls = Parser()
    while True:
        img_path = child_conn.recv()
        data = cls.parse(img_path)
        if data == -1:
            break
        else:
            child_conn.send(data)