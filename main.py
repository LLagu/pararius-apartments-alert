import itertools
import threading
import time
import sys

from libraries.pararius_alert import ParsePage

done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rMonitoring the website ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

ParsePage()

# time.sleep(10)
# done = True