import sys, os
from ax import AX

ax = AX()
src = open(sys.argv[1], 'rb')
dst = sys.argv[2]
print(dst)

ax.write_command(4)  # CMD_PUT_FILE
ax.write_str(dst)
# result = ax.read_size()
#
# if result < 0:
#     msg = ax.read_str()
#     print(msg)
#     ax.close()
#     exit(1)

to_read = 1024
cur = 0
size = os.path.getsize(sys.argv[1])
ax.write_size(size)

while cur < size:
    if size - cur < 1024:
        to_read = size - cur

    data = src.read(to_read)
    ax.write_data(data)
    result = ax.read_result()
    print('result: %s' % result)
    cur += to_read


ax.close()

