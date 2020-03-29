import sys
import matplotlib.pyplot as plt

def GetXY(filename, xcol, ycol):
    retThing = []
    with open(filename) as file:
        for line in file:
            try:
                lin = line.split(",")
                x = float(lin[xcol])
                y = float(lin[ycol])
                a = (x,y)
                retThing.append(a)
            except Exception:
                print("Oh no, a thing happened. Maybe " + lin[xcol] + " or " + lin[ycol] + " aren't numbers?")
    return retThing

def plottify(filenm, xcol, ycol, xlab, ylab):
    xy = GetXY(filenm,xcol,ycol)
    x = [k[0] for k in xy]
    y = [k[1] for k in xy]
    fig = plt.figure(figsize=(8.0,5.0))
    fig.add_subplot(111).plot(x,y)
    fig.add_subplot(111).set_ylabel(ylab)
    fig.add_subplot(111).set_xlabel(xlab)
    fig.savefig(filenm + ".svg")

if __name__ == "__main__":
    fileToDoThingsTo = sys.argv[1]
    #plottify(fileToDoThingsTo,0,13,"Time Value (microseconds)","U over Threshold")
    plottify(fileToDoThingsTo,0,1,"Time Value (microseconds)", "U value")
