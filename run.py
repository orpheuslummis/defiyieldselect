import threading

import dfo.collect
import dfo.score
import dfo.serve
import dfo.db

if __name__ == "__main__":
    threading.Thread(target=dfo.collect.run).start()
    threading.Thread(target=dfo.score.run).start()
    threading.Thread(target=dfo.serve.run).start()
    threading.Thread(target=dfo.db.fresh_only).start()