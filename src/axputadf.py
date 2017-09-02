import sys, os
from ax import AX

# This currently only works with 512 * 11 bytes / track and 160 tracks / disk
ax = AX()
src = open(sys.argv[1], 'rb')

ax.write_command(5)  # CMD_PUT_ADF

to_read = 11 * 512
cur = 0
track = 0
size = os.path.getsize(sys.argv[1])
ax.write_command(1)

while cur < size:
    if size - cur < to_read:
        to_read = size - cur

    data = src.read(to_read)
    ax.write_data(data)
    result = ax.read_result()
    track += 1
    print('result: %s, track: %s' % (result, track))

    cur += to_read

ax.close()
