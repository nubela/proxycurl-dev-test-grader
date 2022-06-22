import time
import json
import os
import random
import secrets
import socket
import string

import manager

manager = manager.Manager()

@manager.command
def verify(socks_path):
    def random_str(n):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    def gen_job():
        number_range = [random.choice(range(50)), random.choice(range(50))]
        job = {
            "id": random_str(10),
            "from": min(number_range),
            "to": max(number_range),
            "fizz": random_str(4),
            "buzz": random_str(4),
            "dull": random_str(4),
        }
        return job

    def verify_response(resp, job):
        job_dic = json.loads(job)
        id = job_dic['id']
        fizz_word = job_dic['fizz']
        buzz_word = job_dic['buzz']
        word_str = []
        for i in range(job_dic['from'], job_dic['to']+1):
            if (i % 5 == 0) and (i % 3 == 0):
                word_str += [f"{fizz_word}{buzz_word}"]
            elif (i % 3 == 0):
                word_str += [f"{fizz_word}"]
            elif (i % 5 == 0):
                word_str += [f"{buzz_word}"]
            else:
                word_str += [i]

        try:
            assert resp[id] == word_str
        except Exception:
            print(f"Expecting f{word_str}")
            print(f"Got f{resp[id]}")
            print(f"For the job of {job_dic}")
            raise Exception

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.connect(socks_path)

        for _ in range(random.randint(2, 5)):
            json_job = json.dumps(gen_job())
            job_str = f"{json_job}\n"
            print("Sending job.")
            server.send(job_str.encode())
            received_msg = ""
            print("Waiting for response..")
            while True:
                time.sleep(1)
                received_msg += server.recv(1024).decode("utf-8")
                print(f"Received something... {received_msg}")
                if len(received_msg.split("\n")) >= 2:
                    print("All received, verifying..")
                    json_str = received_msg.split("\n")[0].strip()
                    resp_dic = json.loads(json_str)
                    verify_response(resp_dic, json_job)
                    break

    return True


if __name__ == '__main__':
    manager.main()
