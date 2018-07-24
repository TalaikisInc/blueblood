from asyncnotify import AsyncNotify
from twisted.internet import reactor

from .notify import Notify

dsn = 'dbname=%s host=%s user=%s password=%s' % (getenv("PG_DB"), getenv("PG_SERVER"), getenv("PG_USER"), getenv("PG_PASS"))

def errorHandler(error):
    print(str(error))
    notifier.stop()
    reactor.stop()

def shutdown(notifier):
    print('Shutting down.')
    reactor.stop()

def tableUpdated(notify, pid):
    tablename, op = notify.split('_')
    print( '%s just occured on %s from process ID %s' % (op, tablename, pid))

class Instance(Notify):
    def gotNotify(self, pid, notify):
        if notify == 'quit':
            print('Stopping the listener.')
            self.stop()
        elif notify.split('_')[0]  in ('table1', 'table2'):
            tableUpdated(notify, pid)
        else:
            print("got asynchronous notification '%s' from process id '%s'" % (notify, pid))

def main()
    notifier = Instance(dsn)
    listener = notifier.run()
    listener.addCallback(shutdown)
    listener.addErrback(errorHandler)

    """
    notifier.addNotify('test1')
    notifier.addNotify('test2')
    notifier.addNotify('table1_insert')
    notifier.addNotify('table1_update')
    notifier.addNotify('table1_delete')
    notifier.addNotify('table2_insert')
    notifier.addNotify('table2_update')
    notifier.addNotify('table2_delete')
    notifier.addNotify('quit')

    # Unsubscribe from one
    reactor.callLater(15, notifier.removeNotify, 'test2')
    """

    reactor.run()

main()
