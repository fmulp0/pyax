import sys
from ax import AX

ax = AX()
ax.write_command(3)
ax.write_str(sys.argv[1])
ax.close()
