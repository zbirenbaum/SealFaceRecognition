import numpy as np
import datetime
import pandas as pd

ls = np.array([273.35508847236633,
      264.9384355545044,
      264.4502398967743,
      281.8216619491577,
      282.46744561195374,])

print(datetime.timedelta(seconds=ls.sum()/5))


