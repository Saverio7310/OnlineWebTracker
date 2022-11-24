import csv
import math
import sys
import shutil as sh
from pathlib import Path as ph
from matplotlib.pyplot import figure, plot, scatter, show, text, subplots, imread, hist2d

# these few lines are used to select the right file to get from the download folder by associating each name with a number
img_array = ["griglia", "text", "task", "info1", "info2"]

z = list(zip(img_array, range(0, 5)))

for e in z:
    print(e[0] + " " + str(e[1]), sep="\n")

image_index = int(input("Type the number of the file you want to open: "))

if image_index not in [0, 1, 2, 3, 4]:
    sys.exit("Wrong number!")

# this part is used to move the file from the download folder of the PC into the csv folder 
# of the project. The library used is the best for this task because it
# automatically create the specific path based on the system used (Windows, MacOs)
data_source = ph.home() / 'Downloads' / (img_array[image_index] + '.csv')
data_destination = ph.home() / 'Desktop' / 'WebGazer' / 'csv'
data_exists = data_destination / (img_array[image_index] + '.csv')

# check whether the file is located in the download folder - move it into csv folder - or if
# it's in csv folder - just open the file
location = input(
    "Is your file in dowload or csv folder? (d for download, c for csv) ")

if (location == "d"):
    if (ph.exists(data_exists)):
        new_name = input(
            "How would you like to rename the existing file? (WITH EXTENSION) ")
        ph.rename(data_exists, data_destination / new_name)
        sh.move(data_source, data_destination, copy_function=sh.copy)
    else:
        sh.move(data_source, data_destination, copy_function=sh.copy)
elif (location == "c"):
    pass
else:
    sys.exit("Wrong input!")

# from now on, the file with the data is opened and it is possible to work with it. I used the 'with open'
# because it closes by default the file. That's helpful in case you forget to call the function .close()
with open("csv/" + img_array[image_index] + ".csv") as file:

    # read the csv file
    reader_obj = csv.reader(file)

    # create a list to insert the data from the raw data
    list_data = list()
    for row in reader_obj:
        list_data.append(row)

    # pop the first two line which do not contain useful data (for example the name of the columns)
    list_data.pop(0)
    list_data.pop(0)

    # create a list which contains the same data as before but casted to float type in order to
    # use them to create the fixation points in the chart. This list contains tuples made of x coords,
    # y coords and timestamps.
    list_circles = list()
    for [a, b, c] in list_data:
        list_circles.append([float(a), (float(b)), float(c)])

    # it's used to create a list that contains the distance, the time difference between of each pair
    #  of points and True if the distance is less than DMAX or False otherwise. DMAX is the maximum 
    # space distance between two points to consider them a fixation; TMAX is the maximum time
    #list_distances = [(float, float, bool), (float, ...), ...]
    list_distances = list()
    i = 0
    DMAX = 90
    TMAX = 400
    while i + 1 < len(list_circles):
        num = (list_circles[i+1][0]-list_circles[i][0])**2 + \
            (list_circles[i+1][1]-list_circles[i][1])**2
        square = math.sqrt(num)
        time_difference = list_circles[i+1][2]-list_circles[i][2]
        list_distances.append(
            (round(square, 2), round(time_difference, 2), square < DMAX))
        i = i+1

    # this part is used to find the indexes of the final fixation points
    list_fix_temp = list()
    i = 0
    sum_t = list_distances[0][1]
    while i + 1 < len(list_distances):

        # each consecutive point sampled within 80ms that is going to be assimilated in one 
        # fixation point besides their relative distance (even if grater than DMAX) because
        # sampling rate is about 40ms, so 
        # la distanza temporale di campionamento è intorno ai 40 ms, quindi nel caso in cui
        # siano di per sé troppo lontani Prendiamo i tre punti successivi e li includiamo
        # in un unico Fixation point dato che la distanza temporale di questi tre punti si
        # aggira intorno agli 80 ms più o meno qualche millisecondo.la distanza spaziale
        # in questo caso non ci interessa
        if not list_distances[i][2] and i + 3 < len(list_distances):
            # aggrego i tre punti e non passo l'iterazione successiva ma tre successive perché
            # i punti di mezzo li ho già inseriti in un Fixation
            list_fix_temp.append((i, i+1, i+2))
            sum_t = list_distances[i+3][1]
            #print("primo if, t e i sono " + str(i) + ", " + str(i+1) + ", " + str(i+2) + ", "+ str(i+3))
            i = i+3

        else:
            # Negli altri casi invece prendo il primo punto a disposizione e lo utilizzo
            # come possibile Fixation point. Vado quindi a determinare la distanza tra questo
            # punto e tutti i successivi fino a quando o la distanza degll'iesimo punto è
            # maggiore di DMAX, Oppure il tempo di campionamento ha superato i 400 ms.
            # Successivamente per ogni Fixation point andrò a calcolare la media di tutti
            # i punti andando a trovare il punto medio e utilizzando quello come Fixation finale
 
            j = i
            while i + 1 < len(list_distances):

                num = (list_circles[i+1][0]-list_circles[j][0])**2 + \
                    (list_circles[i+1][1]-list_circles[j][1])**2
                square = math.sqrt(num)
                time_difference = list_circles[i+1][2]-list_circles[j][2]

                if square < DMAX and time_difference <= TMAX:

                    list_fix_temp.append((j, i+1))
                    #print("while, t e i sono " + str(j) + ", " + str(i+1) + ", " + str(i+1))
                    i = i + 1

                else:
                    #print("sono nel while + else")
                    i = i + 1
                    break

    # used to cast the tuples of indexes contained in the previous list into sets of indexes
    list_fix = list()
    i = 0
    for elem in list_fix_temp:
        list_fix.append(set(elem))

    # each set is checked to join the sets that represent the same fixation point
    while i + 1 < len(list_fix):
        if len(list_fix[i].intersection(list_fix[i+1])) > 0:
            j = i
            while i + 1 < len(list_fix) and len(list_fix[j].intersection(list_fix[i+1])) > 0:
                list_fix[j] = list_fix[j].union(list_fix[i+1])
                list_fix.pop(i+1)
        else:
            i = i+1

    # eventually, with this part, for every set (that represents the points that should be considered
    # as the same fixation point), it's calculated the medium point to create the final fixation point
    list_fix_points = list()
    for fix_set in list_fix:
        list_x = list()
        list_y = list()
        for ind in fix_set:
            list_x.append(list_circles[ind][0])
            list_y.append(list_circles[ind][1])
        t = (sum(list_x)/len(list_x), sum(list_y)/len(list_y))
        list_fix_points.append(t)

    # setting of the graph
    img = imread("img/" + img_array[image_index] + ".png")
    fig, ax = subplots()
    # per le prime due immagini va bene extent=[0, 2000, 1200, 0], ma per le infografiche no perché non sono in 16:9, sono in 4:3, penso sia per questo dato che se usato così l'immagine viene stretchata
    ax.imshow(img, extent=[0, 2000, 1200, 0])

    # shows the fixation points
    for center in list_fix_points:
        scatter(center[0], center[1], s=200,
                facecolors='none', edgecolors='blue')

    # cycle used to enumerate all the circles
    i = 0
    for cir in list_fix_points:
        text(cir[0], cir[1], str(i), color="red", fontsize=10)
        i = i+1

    # shows the saccades
    list_x = list()
    list_y = list()
    for fix in list_fix_points:
        list_x.append(fix[0])
        list_y.append(fix[1])
    plot(list_x, list_y, color="#9ACD32")

    # I want to create the heatmap
    # Default heatmap
    img = imread("img/" + img_array[image_index] + ".png")
    fig, ak = subplots()
    ak.imshow(img)

    list_y_vecchi = list()
    for y in list_y:
        list_y_vecchi.append(1200 - y)
    hist2d(list_x, list_y_vecchi, bins=30, range=[
           [0, 2000], [0, 1200]], cmap="Greys")  # icefire, Greys
    

    # funziona ma è da migliorare

    show()