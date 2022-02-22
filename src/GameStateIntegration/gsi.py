import dota2gsi

server = dota2gsi.Server(ip='0.0.0.0', port=8080)


def handle_state_change(state):
    print(state)


server.on_update(handle_state_change)

if __name__ == '__main__':
    server.start()

