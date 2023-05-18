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
        self.MIDPOINT = 1325  # what servo command (1000-2000) is straight forward for your bot?
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
      while self.read_distance() > 250:  
            self.fwd()
            time.sleep(.01)
      else:
        self.stop()
        self.manage_box()
        self.box_navigate()
        
    #Needs work
    def manage_box(self):
      self.servo(self.MIDPOINT-350)
      time.sleep(0.5)
      variable1 = self.read_distance() #right
      self.servo(self.MIDPOINT)
      self.servo(self.MIDPOINT+350)
      time.sleep(0.5)
      variable2 = self.read_distance() #left
      self.servo(self.MIDPOINT)
      if variable1 < variable2:
        self.turn_by_deg(-90)
        distance1 = variable1/200 
        self.fwd()
        time.sleep(distance1)
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(90)
      else:
        self.turn_by_deg(90)
        distance2 = variable2/200 
        self.fwd()
        time.sleep(distance2)
        self.fwd()
        time.sleep(1)
        self.turn_by_deg(-90)
        
    #Needs work
    def move_scan(self):
      # Write a move method which scans slightly to the left and right of the robot as it moves forward
      while self.read_distance() > 100: 
            self.fwd()
            time.sleep(1.5)
            self.read_distance()
            self.servo(self.MIDPOINT-500) 
            self.read_distance()
            self.servo(self.MIDPOINT+500)
            self.read_distance()
            self.servo(self.MIDPOINT)
      else:
        self.stop()
        self.decision()
        self.move_scan()

    def decision(self):
      variableb1 = self.read_distance()
      self.servo(self.MIDPOINT-500)
      variableb2 = self.read_distance() #right
      self.servo(self.MIDPOINT+500)
      variableb3 = self.read_distance() #left
      self.servo(self.MIDPOINT)
      if variableb1 < variableb2 and variableb3:
        if variableb3 < variableb2:
          self.wall_avoid_L(variableb3)
        else:
          self.wall_avoid_R(variableb2)
      else:
        if variableb2 < variableb3:
          self.wall_swerve_L
        else:
          self.wall_swerve_R

    def wall_avoid_L(self, variableb3):
      self.turn_by_deg(-90)
      distanceb1 = variableb3/100 
      self.fwd()
      time.sleep(distanceb1)

    def wall_avoid_R(self, variableb2):
      self.turn_by_deg(90)
      distanceb2 = variableb2/100 
      self.fwd()
      time.sleep(distanceb2)

    def wall_swerve_L(self):
      self.turn_by_deg(-90)
      self.fwd
      time.sleep(0.5)

    def wall_swerve_R(self):
      self.turn_by_deg(90)
      self.fwd
      time.sleep(0.5)
          

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
