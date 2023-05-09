#!/usr/bin python3
from teacher import PiggyParent
import sys
import time


class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "sd": ("Safe to Dance", self.safe_to_dance),
                "ws": ("Move with Stops", self.wall_stop),
                "wt": ("Move with Turns", self.wall_turn),
                "ms": ("Move + Scan", self.move_scan),
                "b": ("Navigate Box", self.box_navigate),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "z": ("Square", self.square),
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def square(self):
      self.fwd()
      time.sleep(1)
      self.stop()
      self.turn_by_deg(90)
      self.fwd()
      time.sleep(1)
      self.stop()
      self.turn_by_deg(90) 
      self.fwd()
      time.sleep(1)
      self.stop()
      self.turn_by_deg(90) 
      self.fwd()
      time.sleep(1)
      self.stop()
      self.turn_by_deg(90)
      self.stop()
      
    def dance(self):
        """A higher-ordered algorithm to make your robot dance"""
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(90)
        self.turn_by_deg(-90)
        self.back()
        time.sleep(2)
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(90)
        self.turn_by_deg(-90)
        self.back()
        time.sleep(2) 
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(90)
        self.turn_by_deg(-90)
        self.back()
        time.sleep(2) 
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(90)
        self.turn_by_deg(-90)
        self.back()
        time.sleep(2)
        # TODO: check to see if it's safe before dancing
        
        # lower-ordered example...
        self.right(primary=50, counter=50)
        time.sleep(2)
        self.stop()

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        for x in range(7):
          self.turn_by_deg(45)
          if self.read_distance() < 700:
            self.stop() 
          else:
            pass
        self.turn_by_deg(45)
        if self.read_distance() < 700:
          self.stop() 
        else:
          self.dance()

    def wall_stop(self):
      self.servo(1500)
      self.fwd()
      time.sleep(1)
      if self.read_distance() < 200:
        self.stop()
      else:
        self.wall_stop()

    def wall_turn(self):
      self.servo(1500)
      self.fwd()
      time.sleep(1)
      if self.read_distance() < 200:
        self.turn_by_deg(180)
        self.wall_turn()
      else:
        self.wall_turn()

    def box_navigate(self):
      # Move to box and go around it. Before moving around box, figure out which side of closer. If you are closer to the left end of the box, go around left. If you are closer to the right end of the box, go around to the right.
      self.fwd()
      time.sleep(1)
      if self.read_distance() < 200:
        self.manage_box
      else:
        self.box_navigate()

    def manage_box(self):
      self.turn_by_deg(-90)
      #Read distance and save as variable
      self.turn_by_deg(90)
      self.turn_by_deg(90)
      #Read distance and save as different variable
      #Find out which variabble is greater
      #Look for which side is closer
      #If left is closer:
        #Turn -90 degrees and travel on loop until the end is passed, then turn 90 degrees
      #If right is closer:
        #Turn 90 degrees and travel on loop until the end is passed, then turn -90 degrees
      pass

    def move_scan(self):
      # Write a move method which scans slightly to the left and right of the robot as it moves forward
      self.fwd()
      time.sleep(1)
      #if self.read_distance() < 200:
        #Decide to swerve or go around
        #Do self.wall_avoid or self.wall_swerve accordingly
      pass

    def wall_avoid(self):
      #If it senses a wall straight ahead, it goes around to the closest side as above
      #If edge is on left: 
        #Turn -90 degrees and travel on loop until the end is passed, then turn 90 degrees
      #If wall is on right:
        #Turn 90 degrees and travel on loop until the end is passed, then turn -90 degrees
      pass

    def wall_swerve(self):
      # If it senses a wall at the edges of the robot, swerve slightly to miss the wall
      # If wall is on left:
      self.turn_by_deg(45)
      self.fwd
      time.sleep(1)
      # If wall is on right:
      self.turn_by_deg(45)
      self.fwd
      time.sleep(1)
      pass
          
    def shake(self):
        """ Another example move """
        self.deg_fwd(720)
        self.stop()

    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        while self.read_distance() > 250:  # TODO: fix this magic number
            self.fwd()
            time.sleep(.01)
        self.stop()
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
