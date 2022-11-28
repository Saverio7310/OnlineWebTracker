import csv
import math
import sys
import shutil as sh
from pathlib import Path as ph
from matplotlib.pyplot import plot, scatter, show, text, subplots, imread, hist2d

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

    # it's used to create a list that contains the distance, the time difference between each pair
    # of points and True if the distance is less than DMAX or False otherwise. DMAX is the maximum
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
        i = i + 1

    # this part is used to find the indexes of the final fixation points
    list_fix_temp = list()
    i = 0
    sum_t = list_distances[0][1]
    while i + 1 < len(list_distances):

        # the minimum time to have a fixation point is 80ms. Since the difference between
        # each point is more or less 40ms, we aggregate 3 consecutive gaze points even if
        # they are too far away. We do this because even if their distance is bigger than the
        # minimum, the time of sampling was too short to consider them distinct fixation points
        if not list_distances[i][2] and i + 3 < len(list_distances):
            # after joining 3 gaze points we update the index by 3 because we need to move on
            # and work with the right points
            list_fix_temp.append((i, i+1, i+2))
            sum_t = list_distances[i+3][1]
            i = i + 3

        else:
            # if the points are close enough, we take the first available and calculate the
            # distance between itself and all consecutive gaze points until the relative
            # distance is greater than DMAX or the sum of timestamps i greater than TMAX.
            # Later we are going to create a unique fixation point for each group of gaze
            # points found here by calculating the middle point.
            j = i
            while i + 1 < len(list_distances):

                num = (list_circles[i+1][0]-list_circles[j][0])**2 + \
                    (list_circles[i+1][1]-list_circles[j][1])**2
                square = math.sqrt(num)
                time_difference = list_circles[i+1][2]-list_circles[j][2]

                if square < DMAX and time_difference <= TMAX:

                    list_fix_temp.append((j, i+1))
                    i = i + 1

                else:
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

    # eventually, for every set (that represents the points that should be considered
    # as the same fixation point), it's calculated the medium point to create the
    # real fixation point
    list_fix_points = list()
    for fix_set in list_fix:
        list_x = list()
        list_y = list()
        for ind in fix_set:
            list_x.append(list_circles[ind][0])
            list_y.append(list_circles[ind][1])
        t = (sum(list_x)/len(list_x), sum(list_y)/len(list_y))
        list_fix_points.append(t)

    # setting of the graph with background image and the dimension of the axes
    img = imread("img/" + img_array[image_index] + ".png")
    fig, ax = subplots()
    ax.imshow(img, extent=[0, 2000, 1200, 0])

    # shows each fixation point as a blue empty circle
    for center in list_fix_points:
        scatter(center[0], center[1], s=200,
                facecolors='none', edgecolors='blue')

    # enumerate every fixation point from 0 to len(list_fix_points)
    i = 0
    for cir in list_fix_points:
        text(cir[0], cir[1], str(i), color="red", fontsize=10)
        i = i+1

    # shows the saccades by plotting the distances between each consecutive fixation point
    list_x = list()
    list_y = list()
    for fix in list_fix_points:
        list_x.append(fix[0])
        list_y.append(fix[1])
    plot(list_x, list_y, color="#9ACD32")

    # setting the graph for the heatmap. Unfortunatly i couldn't find a way to set the
    # background image
    fig, ak = subplots()
    ak.imshow(img)

    # create the heatmap. The difference (1200 - y) is used because the coordinate (0, 0)
    # is in the top-left corner for the data gathered in the csv file while for this type
    # of graph it is located in the bottom-left corner.
    list_y_vecchi = list()
    for y in list_y:
        list_y_vecchi.append(1200 - y)
    hist2d(list_x, list_y_vecchi, bins=30, range=[
           [0, 2000], [0, 1200]], cmap="Greys")

    # this call is used to show each graph created before.
    show()