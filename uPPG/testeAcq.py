from threading import Thread

def ftt():
    print('thread')

if __name__ == '__main__':
    get_level_thread = Thread(target = ftt)
    get_level_thread.daemon = True
    get_level_thread.start() 
    #while True:
       # print('main')
