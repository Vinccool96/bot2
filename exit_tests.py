import signal


def exisigabrt():
    print('SIGABRT executed')


def exisigbreak():
    print('SIGBREAK executed')


def exisigfpe():
    print('SIGFPE executed')


def exisigill():
    print('SIGILL executed')


def exisigint():
    print('SIGINT executed')


def exisigsegv():
    print('SIGSEGV executed')


def exisigterm():
    print('SIGTERM executed')


signal.signal(signal.SIGABRT, exisigabrt)

signal.signal(signal.SIGBREAK, exisigbreak)

signal.signal(signal.SIGFPE, exisigfpe)

signal.signal(signal.SIGILL, exisigill)

signal.signal(signal.SIGINT, exisigint)

signal.signal(signal.SIGSEGV, exisigsegv)

signal.signal(signal.SIGTERM, exisigterm)

while True:
    print('True')
