# -*- coding: utf-8 -*-
import datetime
import time

times = datetime.datetime.now().timetuple()
print(time.mktime(times))