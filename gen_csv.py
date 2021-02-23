
print("generating...")

txt = "LoopingTimeStamp:60000\n"
txt += "Timestamp,/Meas/Acc/x,/Meas/Acc/y,/Meas/Acc/z,/Meas/Gyro/x,/Meas/Gyro/y,/Meas/Gyro/z,/Meas/Magn/x,/Meas/Magn/y,/Meas/Magn/z\n"
for i in range(0, 6000):
    txt += str(i * 20)
    txt += ',' + str(i) + ',' + str(i) + ',' + str(i) + ',' + str(i) + ',' + str(i) + ',' + str(i) + ',' + str(i) + ',' + str(i) + ',' + str(i)
    txt += '\n'

with open('data/accelerometer.csv', 'w') as out:
    out.write(txt)
