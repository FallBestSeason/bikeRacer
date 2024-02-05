bike racer game
by autumn day! https://github.com/DayAut

this game is about building and racing fixed gear bikes
the bikes are customizable, with different parts providing different advantages
inspired by the gameplay of fr legends and other racing games

part slots:
    frameset
    stem
    handlebar
        color of bar tape
    seatpost 
    saddle
    chain
    crankset
        f. chainring
    flats w/ straps vs clips
    wheelset
        r. cog
        lock ring
        hubs
        spokes
        rims

groups in ui:
cockpit
    stem
    bar
        tape
saddle:
    saddle 
    seatpost
drivetrain:
    crankset
        f.chainring
    chain
    pedals
wheelset:
        r. cog
        hubs
        spokes
        rims

basic program breakdown:
main.py
    handles barebones pygame window management

gameHandler
    handles state change between game screens
    passes needed references to gui elements

GUI folder
    contains resources and modules for GUI functionality.
    the modules here + gamehandler make up a "gui library" if you squint a little

    button
        abstract instance module, handles data and math for making buttons
        notably has mehtod to check if a click's coordinate is within a button 

    gui classes (mainMenu, bikeShop, etc)
        handles data about gui elements, sizes, positions, colors, resource refs, etc
        handles drawing each gui element in correct order
        handles button click logic for gameHandler

