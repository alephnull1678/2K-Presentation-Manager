from pathlib import Path
import os
import shutil

from configparser import ConfigParser

import FreeSimpleGUI as sg




def isValidPath(filepath):
    if filepath and Path(filepath).exists():
        return True
    return False





#Some basic variables
packages = []
currentPackage = None

gameDir = ""
dirValid = False






#MAKE CONFIG FILE
def create_config():
    print("Creating default config.ini file...")

            
            

            
    config.add_section('main')
    config.set('main', 'loadedpackages', '¬'.join(packages))
    config.set('main', 'currentpackage', 'Not selected')
    config.set('main', 'gamedir', 'Not selected')
    config.set('main', 'dirvalid', 'False')


    with open('config.ini', 'w') as f:
        config.write(f)



#[GUI] MAKE WINDOW
def make_Window():

    


    layoutPackages = []

    for index, package in enumerate(packages):

        #Check if current index has an activate button: if so, show that button is activated
        if currentPackage == index:



            layoutPackages.append([sg.Text(os.path.basename(package)), sg.Button("ACTIVATE", key=("ACTIVATE", index), button_color = ("black on gray")), sg.Button("REMOVE PACKAGE", key=("REMOVE", index), button_color = ("white on red"))])
        else:
            layoutPackages.append([sg.Text(os.path.basename(package)), sg.Button("ACTIVATE", key=("ACTIVATE", index)), sg.Button("REMOVE PACKAGE", key=("REMOVE", index), button_color = ("white on red"))])

        layoutPackages.append([sg.HorizontalSeparator()])




    #Deciding whether being scrollable is useful yet
    isScrollable = False

    if len(packages) > 7:
        isScrollable = True




    #Deciding what type of text to show for 2k DIRECTORY
    if dirValid == True:
        dirText = "Current 2K directory: " + str(gameDir)
    else:
        dirText = "No 2K directory assigned!"



    

    #LAYOUT

    layout = [


    #PACKAGES COLUMN
    [sg.Column(layoutPackages, size=(350, 300), scrollable=isScrollable,  vertical_scroll_only=isScrollable)],
    



    #ADD NEW BUTTON
    
    [sg.Button("ADD PACKAGE")],
    [sg.HorizontalSeparator()],





    #2K DIR BUTTONS
    [sg.Text(dirText)],
    [sg.Button("SELECT 2K DIRECTORY")],
    [sg.HorizontalSeparator()],



    [sg.Exit(), sg.Button("Deactivate All")]

    
    ]




    #MAKE WINDOW

    return sg.Window("2K Presentation Manager", layout, layout,size=(400, 600))






#[GAME] SET 2K DIRECTORY
def set2kDirectory(fromActivation):
    global dirValid, gameDir, window, currentPackage


    #Keep just in case
    savedGameDir = gameDir


    #Getting game directory if not yet assigned
    while True:

        print(gameDir)

        

        gameDir = sg.popup_get_folder("Select your NBA2K directory...")

        if gameDir == None:
            gameDir = savedGameDir
            break


        #VALID PATH
        if isValidPath(gameDir):


            #CHECK IF MODS FOLDER
            modDir = os.path.join(gameDir, "mods")

            if not os.path.exists(modDir):
                sg.popup_error("This directory doesn't have a Mods folder!")
                continue


            reshade_Path = os.path.join(gameDir, "Reshade.ini")

            #WARNING FOR NON-RESHADE
            if not os.path.exists(reshade_Path):
                sg.popup_annoying("WARNING: It appears that you don't have Reshade installed in your 2K directory. Some presentation packs may require Reshade to function properly.")


            dirValid = True
            currentPackage = None

            
            #Remake window if this function didn't come from activating a package
            if fromActivation == False:
                window.close()
                window = make_Window()


            break

        else:
            sg.popup_error("Not a valid path!")





#[GAME] REMOVE FILES
def removeOldFiles():

    try:
        source_file_list = os.listdir(packages[currentPackage])
        destination_file_list = os.listdir(gameDir)
    except:
        sg.popup_annoying("ERROR: The package trying to be removed (or the 2k directory) is missing! Old files will not be deleted.")
        return


    #RESHADE/MAIN 2K DIR FILE CHECK
    for destination_file_name in destination_file_list:

        #Get path of each file in destination
        destination_file_path = os.path.join(gameDir, destination_file_name)
        
        # Check if the file is also in the source directory
        if destination_file_name in source_file_list:
            os.remove(destination_file_path)
            print(f"Removed '{destination_file_name}' from the destination directory.")

    try:
        modDir = os.path.join(gameDir, "mods")
        destination_file_list = os.listdir(modDir)
    except:
        sg.popup_annoying("ERROR: The mods folder no longer exists! Old mod files will not be deleted.")
        return

    #MOD FILE CHECK
    for destination_file_name in destination_file_list:

        #Get path of each file in destination
        destination_file_path = os.path.join(modDir, destination_file_name)
        
        # Check if the file is also in the source directory
        if destination_file_name in source_file_list:
            os.remove(destination_file_path)
            print(f"Removed '{destination_file_name}' from the Mods directory.")
    





#[GAME] COPY FILES
def copyFiles():
    global currentPackage
    try:
        # Get a list of all files in the source directory
        file_list = os.listdir(packages[currentPackage])
        print(file_list)


        for file_name in file_list:
            source_file_path = os.path.join(packages[currentPackage], file_name)

            #Change destination depending on if file is Reshade file or mod file
            file_extension = os.path.splitext(file_name)[1]

            if file_extension == ".ini":
                #RESHADE
                destination_file_path = os.path.join(gameDir, file_name)
            else:
                #MOD
                destination_file_path = os.path.join(gameDir, "mods")
                destination_file_path = os.path.join(destination_file_path, file_name)
            
            # Copy the file from the source directory to the destination directory
            shutil.copy(source_file_path, destination_file_path)
            
            print(f"Copied '{file_name}' to the destination directory.")
    except:
        #File has moved?
        sg.popup_annoying("ERROR: Package doesn't exist! Did you move it from its original location, or delete it?")
        currentPackage = None
        





#[GAME] ACTIVATE PACKAGE
def activatePackage(packageIndex):
    global currentPackage, dirValid, window

    #Check if is already activated
    if currentPackage == packageIndex:
        sg.popup_ok("This package is already activated!")

    
    
    else:

        if dirValid == False:
            set2kDirectory(fromActivation=True)

        
                



        if dirValid == True:



            #REMOVE PREVIOUS FILES
            if currentPackage != None:
                removeOldFiles()


                

            
            currentPackage = packageIndex
            print("Activated package: " + packages[currentPackage])




            #COPY FILES TO 2k DIR
            copyFiles()




        #Make new window to show changes
        window.close()
        window = make_Window()

    



#[GAME] REMOVE PACKAGE
def removePackage(packageIndex):
    global window, currentPackage

    #Remove files from this package if it is currently activated (NOTE: Should add warning for this later)
    if currentPackage == packageIndex:
        removeOldFiles()
        currentPackage = None

    elif currentPackage != None:

        #Move current package down if removing certain package changes order
        if packageIndex < currentPackage:
            currentPackage -= 1
        
    print("Largest index of packages list is " + str((len(packages) - 1)))
    print('packageIndex is ' + str(packageIndex))

    packages.remove(packages[packageIndex])

    

    window.close()
    window = make_Window()







#CONFIG

try:
    config = ConfigParser()
    config.read('config.ini')

except:
    print("Broken config, remaking...")
    os.remove("config.ini")

if not os.path.exists('config.ini'):
        create_config()
        
        
        
else:
    print("config.ini file already exists.")

    try:
        #READ FROM FILE
        temp = config['main']['loadedpackages']
        packages = temp.split("¬")
        

        #Current package
        if config['main']['currentpackage'] == "Not selected":
            currentPackage = None
        else:
            currentPackage = int(config['main']['currentpackage'])
        

        #Fix oversight if there are no packages
        if "" in packages:
            packages.clear()



        #GAME DIR
        if config['main']['gamedir'] == "Not selected":
            gameDir = ""
        else:
            gameDir = config['main']['gamedir']
        
        #DIRVALID
        if config['main']['dirValid'] == 'False':
            dirValid = False
        else:
            dirValid = True
    except:
        os.remove("config.ini")
        print("Broken config, remaking...")
        create_config()









#INITIAL WINDOW
window = make_Window()









#~~~~~~~~~~~~~~~~
#BIG WHILE LOOP

while True:

    event, values = window.read()





    #EXIT
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    


    #DEACTIVATE ALL
    if event == "Deactivate All":

        if(currentPackage == None):
            pass
        else:

            removeOldFiles()
            currentPackage = None
            

            window.close()
            window = make_Window()
        






    #ACTIVATION




    #ACTIVATE (first)
    if event == "ACTIVATE":

        print(event)

        activatePackage(0)


    if isinstance(event, tuple):
        action, idx = event          
        if action == "ACTIVATE":
            activatePackage(idx)
        elif action == "REMOVE":
            removePackage(idx)
        continue      


    #ACTIVATE (everything else)
    for i in range(0, 100):

        if event == "ACTIVATE" + str(i):

            print(event)

            activatePackage(i)





    #REMOVE PACKAGE (first)
    if event == "REMOVE PACKAGE":


        removePackage(0)



    #REMOVE PACKAGE (everything else)
    for i in range(1, 100):

        if event == "REMOVE PACKAGE" + str(i - 1):


            
            removePackage(i)








    #SELECT 2K DIRECTORY
    if event == "SELECT 2K DIRECTORY":

        set2kDirectory(fromActivation=False)





        


    #ADD NEW
    if event == "ADD PACKAGE":

        window.close()



        #ADDING PACKAGE

       


        while True:

             #Pop-Up
            packageDir = sg.popup_get_folder("Choose a package!")


            #CHECK IF CANCELLED
            if packageDir == None or packageDir == "":
                window = make_Window()
                break

            else:

                #CHECK IF VALID PATH
                if isValidPath(packageDir):


                    #CHECK IF NOT ALREADY USED
                    if packageDir not in packages:


                        #SUCCESS

                        packages.append(packageDir)

                        print("Package directory located at " + str(packageDir))
                        window = make_Window()

                        break
                    else:

                        #ALREADY USED
                        sg.popup_error("This package has already been selected!")

                else:
                    #INVALID PATH
                    sg.popup_error("Please choose a valid package path!")





        

    



#WRITE TO CONFIG BEFORE CLOSING
config.set('main', 'loadedpackages', '¬'.join(packages))    #Please don't judge for the amateur save system

#Current package
if currentPackage == None:
    config.set('main', 'currentpackage', 'Not selected')
else:      
    config.set('main', 'currentpackage', str(currentPackage))


#Gamedir
if gameDir == "":
    config.set('main', 'gamedir', 'Not selected')
else:
    config.set('main', 'gamedir', gameDir)


#Dirvalid
if dirValid == False:
    config.set('main', 'dirvalid', 'False')
else:
    config.set('main', 'dirvalid', 'True')


with open('config.ini', 'w') as f:
    config.write(f)


#Close window
window.close()


