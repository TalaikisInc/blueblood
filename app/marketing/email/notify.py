from select import select

from psycopg2 import connect
from twisted.internet import threads


class Notify():
    def __init__(self, dsn):
        self.conn = connect(dsn)
        self.conn.set_isolation_level(0)
        self.curs = self.conn.cursor()
        self.__listening = False

    def __listen(self):
        if self.__listening:
            return 'Already listening!'
        else:
            self.__listening= True
                while self.__listening:
                    if select([self.curs],[],[],60)!=([],[],[]) and self.curs.isready():
                        if self.curs.connection.notifies:
                            pid, notify = self.curs.connection.notifies.pop()
                            self.gotNotify(pid, notify)

    def addNotify(self, notify):
        '''Subscribe to a PostgreSQL NOTIFY'''
        sql = "LISTEN %s" % notify
        self.curs.execute(sql)

    def removeNotify(self, notify):
        '''Unsubscribe a PostgreSQL LISTEN'''
        sql = "UNLISTEN %s" % notify
        self.curs.execute(sql)

    def stop(self):
        '''Call to stop the listen thread'''
        self.__listening = False

    def run(self):
        '''Start listening in a thread and return that as a deferred'''
        return threads.deferToThread(self.__listen)

    def gotNotify(self, pid, notify):
        # @TODO send email, check if not already sent
        pass
