total = 0
count = 1
with open("times.txt") as fp:
    line = fp.readline()
    while line:
        num = float(line)
        total += num
        line = fp.readline()
        count += 1

print("Count = %d" % count)
print("Average time to detect hand = %f" % (total / count))