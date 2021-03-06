# Alternate Fillings
Alternate Fillings is a pattern found on the doors between two train compartments. It is built up of rectangles, where each overlapping rectangle inverts the color of the overlapped region. 

The code in this repository creates similar filling patterns. The algorithm is designed such that the rectangles are visually pleasing. The user of this code can play around with the configuration for different results. Below two example drawings with 10 rectangles, with either all rectangles completely inside the canvas or not respecitvely.

![Alternate Filling 01](readme_data/alternate_filling_01.png)
![Alternate Filling 02](readme_data/alternate_filling_02.png)

## Execution notes

There are multiple implementations of the same algorithm, one in OOP and on in functional. To run the code, run the following from the `src` folder:
```shell script
python alternate_fillings_<xxx>
```

Where <xxx> is either oop or functional. Running the code requires Python 3.6 or up. 

## Efficiency notes

### The algorithm is quadratic in canvas size

The following timings are averages of three drawings with 10 rectangles with varying CANVAS_SIZE.

| CANVAS_SIZE | Time in seconds |
|:-----------:|:---------------:|
|     100     |        3.0      |
|     200     |        3.6      |
|     400     |       15.8      |
|     800     |       62.7      |

### The algorithm is linear in number of rectangles

The following timings are averages of three drawings with CANVAS_SIZE of 400 with varying number of rectangles.

| NR_RECTANGLES | Time in seconds |
|:-------------:|:---------------:|
|        5      |       13.2      |
|       10      |       23.2      |
|       20      |       27.4      |
|       40      |       50.8      |
|       80      |       99.2      |

## Parallellization

5 times with 10 rectancgles, CANVAS_SIZE = 400
1 27.3
2 14.4
3 10.6
4 8.9
5 9.0
6 9.4
7 9.2
8 9.3
9 9.2
10 9.2
15 9.2
20 9.2
25 9.2
30 9.1
35 9.4
40 9.6

5 times with 10 rectancgles, CANVAS_SIZE = 1000 
1 184.9
2 95.0
3 70.0
4 68.4
5 65.5
6 60.2
7 57.2
8 57.6
9 59.0
10 59.8
15 62.7
20 61.2
25 58.2
30 63.3