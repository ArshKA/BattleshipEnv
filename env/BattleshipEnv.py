


  
import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time





options = webdriver.ChromeOptions()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')







class BattleshipEnv(gym.Env):
    """A stock trading environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

#  def __init__(self, df):
    def __init__(self):
        super(BattleshipEnv, self).__init__()

        self.reward_range = (-100, 100)

        # Actions of the format Buy x%, Sell x%, Hold, etc.
        self.action_space = spaces.Discrete(100)

#        self.action_space = spaces.Box(
#            low=np.zeros((10, 10)), high=np.full((10, 10), 1), dtype=np.float16)

        # Prices contains the OHCL values for the last five prices
        self.observation_space = spaces.Box(
            low=0, high=2, shape=(10, 10), dtype=np.float16)


    def step(self, action):
      reward = -1
      done = False
      driver = self.driver
      yeet = self.yeet
      final = self.final

      print(action)

      win = False
      lose = False
      tie = False

      num1 = str((action%10)+1)
      num2 = str((action//10)+1)

      element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/table/tbody/tr['+num2+']/td['+num1+']')
      if (action in yeet):
        element.click()

        time.sleep(1)

        if (str(element.get_attribute('class')) != 'battlefield-cell battlefield-cell__miss battlefield-cell__last'):
          print('Hit')
          reward+=11



        element = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[9]')
        if (str(element.get_attribute('class'))[-1] == 'n'):
          print('WIN')
          reward+=50
          win = True

        yeet = []
        final = [[],[],[],[],[],[],[],[],[],[]]


        for x in range(1, 11):
          for y in range(1, 11):
            element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/table/tbody/tr['+str(x)+']/td['+str(y)+']')
            if (str(element.get_attribute('class'))[-1] == 'd' or str(element.get_attribute('class'))[-1] == 'y'):
              final[x-1].append(0)
              yeet.append((x-1)*10+(y-1))
            elif(str(element.get_attribute('class'))[-1] == 's' or str(element.get_attribute('class'))[-1] == 'o' or str(element.get_attribute('class'))[-4:-1] == 'las'):
              final[x-1].append(1)
            else: 
              final[x-1].append(2)

        self.final = final
        self.yeet = yeet



      else: 
        print('Already Hit')
        reward-=9

      if (action%3==0):
      	driver.save_screenshot("screenshot.png")

      last_played = time.time()
      while True:
        element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]')
        if (str(element.get_attribute('class')) == 'battlefield battlefield__rival'):
          break

        else:
          element = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[10]')
          if (str(element.get_attribute('class'))[-2] == 's'):
            print('LOSE')
            reward-=30
            lose = True
            break
          elif (time.time()-last_played >= 60):
            print('TIE')
            tie = True
            break


      if (win or lose or tie):
        done = True

      return np.array(final), reward, done, {}










    def reset(self):

        try: 
          driver = self.driver
          driver.close()

        except: pass
        driver = webdriver.Chrome('chromedriver',options=options)
        self.driver = driver
        driver.get("http://en.battleship-game.org")


        element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/ul/li[1]/span')
        element.click()

        element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]')
        element.click()

        time.sleep(4)


        last_played = time.time()

        self.yeet = list(range(100))

        final = np.zeros((10, 10))
        
        final.astype(int)

        final = final.tolist()

        self.final = final

        last_played = time.time()
        while True:
          element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]')
          if (str(element.get_attribute('class')) == 'battlefield battlefield__rival'):
            break

          elif (time.time()-last_played >= 60):
            tie = True
            break

        return np.array(final)





    def render(self, mode='human', close=False):
        driver.save_screenshot("screenshot.png")
        print('Hiiiiiiiiii')

