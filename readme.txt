Welcome to BikeRacer!
by autumn! https://github.com/FallBestSeason

this game is about building and racing fixed gear bikes on criterium tracks
the bikes are customizable, with different parts providing different pros and cons
inspired by: 
    -the gameplay loop and car upgrading of forza motorsport 3 
    -the gun building of escape from tarkov
    -the customization of FR legends
    -my love of fixed gear bikes and the scene

I am making this game to get better at coding. I have an associates in software
development but I don't yet feel capable of working in an enterprise setting. 
The goal of this project is to prove that I can function as a full-stack dev on
a framework I know nothing about. 

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
        tires

basic program breakdown:
main
    handles barebones pygame window management

gameHandler
    handles state change between game screens
    passes needed references to gui elements

inventory
    handles inventory.json file 
    represents items to be acessed in shop 

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

