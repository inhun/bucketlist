from datetime import datetime
from pytz import timezone, utc

KST = timezone('Asia/Seoul')

print(KST)
print(datetime.now(KST))