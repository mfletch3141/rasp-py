'''This program uses the DS18B20 waterproof temperature sensors from adafruit. The sensors use Dallas Protocol.
This is dsigned to be used with a Heat Transfer experiment. It updates a graph as new data comes in. It also writes the 
data to a text file that can be analyzed after.'''

import time
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

folder_list =[]
device_file_list = []
id_list = []
sorted_serials = []


#number of connected sensors
a = len(glob.glob('/sys/bus/w1/devices/28*'))
print 'Number of sensors read: ' + str(a)

#order the sensors
for i in range(a):
    folder_list.append(glob.glob('/sys/bus/w1/devices/28*')[i]) #get device serial numbers
    id_list.append(int(folder_list[i][-7:],16)) #convert the last seven digits to decimal from hex

id_list.sort()

#rebuild directories in order
for i in range(a):
    sorted_serials.append('/sys/bus/w1/devices/28-00000' + hex(id_list[i])[2:] + '/w1_slave')

#get number of samples to collect
sec = int(float(raw_input('Enter the number of seconds to run: ')))
print '\nWorking\nPress ctrl+C to break'

# Output text file

out = open('therm_output.txt','w')
#column spacing
w = 10

#print serial numbers for each sensor and column heads
slist = ''
head = 'Time'.ljust(w)
for i in range(a):
    slist = slist + 'Sensor ' + str(i+1) + ' ' + sorted_serials[i][20:35]+'\n'
    sens = 'Sensor ' + str(i+1)
    head = head + sens.ljust(w)
out.write(slist) 
out.write(head+'\n')

# end output text file

#set up plot window
fig = plt.figure()
fig.suptitle('Heat Exchange Experiment', fontsize=12, fontweight= 'bold')
ax = fig.add_subplot(111)
line1, = ax.plot([], [], 'r', label='Hot in', lw=2)
line2, = ax.plot([], [], 'g', label='Cold out', lw=2)
line3, = ax.plot([], [], 'b', label='Cold in', lw=2)
line4, = ax.plot([], [], 'm', label='Hot out', lw=2)


ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (C)')
ax.set_ylim(20, 35)
ax.set_xlim(0, sec + 10)
ax.grid()
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
plt.legend(bbox_to_anchor=(0.5,-0.12), loc="upper center", ncol=5,borderaxespad=0.)
xdata, t1data, t2data, t3data, t4data = [], [], [], [], []

begin = time.time()

def data_gen():
    cnt = 0
    while cnt < sec:
        cnt = time.time()-begin
        print cnt
        yield cnt, read_tempi()
        
def run(data):
    # update the data
    t,y = data
    xdata.append(t)
    t1data.append(y[0])
    t2data.append(y[1])
    t3data.append(y[2])
    t4data.append(y[3])
    print y

    #write out to file
    aa = ''
    for j in range(len(y)):
         aa = aa + str(y[j]).ljust(w)
    out.write(str(round(t,3)).ljust(w) + aa +'\n')

    #set limits on axes in plot
    ymin, ymax = ax.get_ylim()
    if max(y) >= ymax:
        if max(y) >= ymax:
            ax.set_ylim(ymin, 5+ymax)
            ax.figure.canvas.draw()
    line1.set_data(xdata, t1data)
    line2.set_data(xdata, t2data)
    line3.set_data(xdata, t3data)
    line4.set_data(xdata, t4data)
    return line1, line2, line3, line4,

#get temperatures from sensors
def read_tempi():
    templist = []
    for i in range(a):
        f = open(sorted_serials[i],'r')
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            f = open(sorted_serials[i],'r')
            lines = f.readlines()
            f.close()
            #debug: print to see when sensors fail
            #dd = 'miss' + str(i)
            #print dd
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
            templist.append(temp)
        time.sleep(.8)
    return templist  #list of all 4 sensor readings

ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=1000,
    repeat=False)

plt.show()import time
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

folder_list =[]
device_file_list = []
id_list = []
sorted_serials = []


#number of connected sensors
a = len(glob.glob('/sys/bus/w1/devices/28*'))
print 'Number of sensors read: ' + str(a)

#order the sensors
for i in range(a):
    folder_list.append(glob.glob('/sys/bus/w1/devices/28*')[i]) #get device serial numbers
    id_list.append(int(folder_list[i][-7:],16)) #convert the last seven digits to decimal from hex

id_list.sort()

#rebuild directories in order
for i in range(a):
    sorted_serials.append('/sys/bus/w1/devices/28-00000' + hex(id_list[i])[2:] + '/w1_slave')

#get number of samples to collect
sec = int(float(raw_input('Enter the number of seconds to run: ')))
print '\nWorking\nPress ctrl+C to break'

################################### Output text file
'''
The text file is included for diagnostic purposes and as an easy import for
data analysis in Excel. The following code sets up the file. Lines are written
in the data collection loop and the file is closed at the end.

'''
out = open('therm_output.txt','w')
#column spacing
w = 10

#print serial numbers for each sensor and column heads
slist = ''
head = 'Time'.ljust(w)
for i in range(a):
    slist = slist + 'Sensor ' + str(i+1) + ' ' + sorted_serials[i][20:35]+'\n'
    sens = 'Sensor ' + str(i+1)
    head = head + sens.ljust(w)
out.write(slist) 
out.write(head+'\n')

################################## end output text file

#set up plot window
fig = plt.figure()
fig.suptitle('Heat Exchange Experiment', fontsize=12, fontweight= 'bold')
ax = fig.add_subplot(111)
line1, = ax.plot([], [], 'r', label='Hot in', lw=2)
line2, = ax.plot([], [], 'g', label='Cold out', lw=2)
line3, = ax.plot([], [], 'b', label='Cold in', lw=2)
line4, = ax.plot([], [], 'm', label='Hot out', lw=2)


ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (C)')
ax.set_ylim(20, 35)
ax.set_xlim(0, sec + 10)
ax.grid()
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
plt.legend(bbox_to_anchor=(0.5,-0.12), loc="upper center", ncol=5,borderaxespad=0.)
xdata, t1data, t2data, t3data, t4data = [], [], [], [], []

begin = time.time()

def data_gen():
    cnt = 0
    while cnt < sec:
        cnt = time.time()-begin
        print cnt
        yield cnt, read_tempi()
        
def run(data):
    # update the data
    t,y = data
    xdata.append(t)
    t1data.append(y[0])
    t2data.append(y[1])
    t3data.append(y[2])
    t4data.append(y[3])
    print y

    #write out to file
    aa = ''
    for j in range(len(y)):
         aa = aa + str(y[j]).ljust(w)
    out.write(str(round(t,3)).ljust(w) + aa +'\n')

    #set limits on axes in plot
    ymin, ymax = ax.get_ylim()
    if max(y) >= ymax:
        if max(y) >= ymax:
            ax.set_ylim(ymin, 5+ymax)
            ax.figure.canvas.draw()
    line1.set_data(xdata, t1data)
    line2.set_data(xdata, t2data)
    line3.set_data(xdata, t3data)
    line4.set_data(xdata, t4data)
    return line1, line2, line3, line4,

#get temperatures from sensors
def read_tempi():
    templist = []
    for i in range(a):
        f = open(sorted_serials[i],'r')
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            f = open(sorted_serials[i],'r')
            lines = f.readlines()
            f.close()
            #debug: print to see when sensors fail
            #dd = 'miss' + str(i)
            #print dd
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp = float(temp_string) / 1000.0
            templist.append(temp)
        time.sleep(.8)
    return templist  #list of all 4 sensor readings

ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=1000,
    repeat=False)

plt.show()


print '\nDone\nData saved to therm_output.txt\n'
out.close()

print '\nDone\nData saved to therm_output.txt\n'
out.close()
