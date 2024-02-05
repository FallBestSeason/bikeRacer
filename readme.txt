bike racer game
by autumn! https://github.com/FallBestSeason

this game is about building and racing fixed gear bikes
the bikes are customizable, with different parts providing different advantages
inspired by the gameplay loop of racing games and the gun building of escape from tarkov. 

customizable parts:
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
main
    handles barebones pygame window management

gameHandler
    handles state change between game screens
    passes needed references to gui elements

inventory (todo)
    handles items and keeps them in inventory
    handles saving inventory on game quit
    handles loading inventory on game open
    hands inventory data off to gui modules for use

GUI folder
    contains resources and modules for GUI functionality.
    the modules here + gamehandler make up a "gui library" if you squint a little

    button
        abstract instance module, handles data and math for making buttons
        notably has mehtod to check if a click's coordinate is within a button 

    gui modules (mainMenu, bikeShop, etc)
        handles data about gui elements, sizes, positions, colors, resource refs, etc
        handles drawing each gui element in correct order
        handles button click logic for gameHandler

