import socket
import uvicorn

from a2a_module import A2AModule

def main():
    hostname = socket.gethostname()
    port = 8081
    a2a = A2AModule(host=hostname, port=port)
    uvicorn.run(a2a.get_starlette(), port=port)

if __name__ == "__main__":
    main()
