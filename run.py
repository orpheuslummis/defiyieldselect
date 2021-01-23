import threading
import signal
from datetime import datetime, timezone

import dfo.collect
import dfo.score
import dfo.serve
import dfo.db


def exit_gracefully(signumber, _):
  print("Received signal", signumber, "cleaning up...")
  exit(0)

signal.signal(signal.SIGTERM, exit_gracefully)


if __name__ == "__main__":
    print(f'DFO starting at {datetime.now(timezone.utc)}')
    threading.Thread(target=dfo.collect.run).start()
    threading.Thread(target=dfo.score.run).start()
    threading.Thread(target=dfo.serve.run).start()
    threading.Thread(target=dfo.db.fresh_only).start()