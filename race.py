from villager_turtle import VillagerTurtle
import turtle, sys, getopt, os
import numpy as np

def collision(a, b):
    """
    Determines if object a and b are intersecting.
    @param a first object
    @param b second object
    @return True or False
    """
    return abs(a.xcor() - b.xcor()) < 25 and abs(a.ycor() - b.ycor()) < 25

def choose_background(backgrounds, bg):
    """
    Selects a background to use for the race.
    @param backgrounds list of backgrounds in images/backgrounds directory
    @return path for chosen background image
    """
    if bg is not None:
        return 'images/backgrounds/{}.gif'.format(bg)
    else:    
        return 'images/backgrounds/{}'.format(backgrounds[np.random.randint(len(backgrounds))])

def register_shapes(villagers, bg):
    """
    Registers shapes for all villagers and picks background.
    @param villagers list of villagers in images/villagers directory
    @param bg background argument (can be None)
    @return screen that shapes have been registered to
    """
    screen = turtle.Screen()
    backgrounds = [f for f in os.listdir('images/backgrounds/') if os.path.isfile(os.path.join('images/backgrounds/', f))]

    screen.bgpic(choose_background(backgrounds, bg))

    for villager in villagers:
        screen.register_shape('images/villagers/{}'.format(villager))

    return screen

def race(targ, bg=None):
    """
    Simulates a turtle race between all of the players in players.txt. 
    The objective of this race is to reach the target first.
    @param target the target image to race to (a stationary turtle)
    """
    villagers = [f for f in os.listdir('images/villagers/') if os.path.isfile(os.path.join('images/villagers/', f))]
    space, target = register_shapes(villagers, bg), turtle.Turtle()
    space.register_shape('images/{}.gif'.format(targ)), target.shape('images/{}.gif'.format(targ))
    turtles, players = [], open('players.txt').read().split()

    for player in players:
        turtles.append(VillagerTurtle(turtle=turtle, target=target, villagers=villagers, name=player, screensize=space.screensize()))

    for turt in turtles:
        turt.info()

    done = False
    while not done:
        for turt in turtles:
            turt.random_turn()
            turt.move()

            if collision(turt.turtle, target):
                done = True
                turt.win()
                break

    space.exitonclick()

def main(argv):
    """
    Parses input arguments to determine whether target or background is used.
    @param argv command-line arguments
    @return target and background
    """
    target, background = 'turnip', None

    opts, args = getopt.getopt(argv,"t:bg:",["target=","background="])

    for opt, arg in opts:
        if opt in ("-t", "--target"):
            target = arg
        if opt in ("-bg", "--background"):
            background = arg

    if opts == [] and args == []:
        print('No background or target specified.')
        print('Usage [short]: python3 race.py -t bells -bg grass')
        print('Usage [long]: python3 race.py --target=nmt --background=grass')

    return target, background

if __name__ == "__main__":
  target, background = main(sys.argv[1:])

  race(targ=target, bg=background)