from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


import os
import time
from time import sleep
from secrets import pw
from utility_methods.utility_methods import *


class InstaBot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver = webdriver.Firefox()

        self.login()

        self.base_url = 'https:/www.instagram.com/'
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')

        sleep(2)

        username_input = self.driver.find_element_by_name('username')

        password_input = self.driver.find_element_by_name('password')


        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        login_btn = self.driver.find_element_by_xpath("//*[contains(text(), 'Log In')]").click()

        sleep(2)

        # self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()


    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//*[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        print("finished username")
        self.driver.find_element_by_xpath("//*[contains(@href,'/following')]")\
            .click()
        sleep(1)
        print("finished following")

        following = self.get_names()

        self.driver.find_element_by_xpath("//*[contains(@href, '/followers')]")\
            .click()

        followers = self.get_names()
        not_following_back = [user for user in following if user not in followers]

        
        print("Accounts who don't follow back: \n")
        print(not_following_back)

    def get_names(self):
        sleep(1)
        suggestions = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', suggestions)
        sleep(1)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        
        #test for closing the page opened
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()

        return names
    
    
    
    
    def search_tag(self, tag):
        # Navigates to a search with the specified tag on Instagram

        self.drive.get(self.get_tag_url.format(tag))
        
    def nav_user(self, user):
        # Navigate to a users profile page

        self.driver.get(self.nav_user_url.format(user))
        # self.driver.get(self.)

    def find_buttons(self, button_text):
        #locate following and unfollowing users by filtering elements

        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))


        return buttons

    def follow_user(self, user):
        self.nav_user(user)
        
        sleep(1)

        follow_buttons = self.find_buttons('Follow')

        for btn in follow_buttons:
            btn.click()



    def like_recent_posts(self, user, n_posts, like=True):
        action = 'Like' if like else 'Unlike'
        self.nav_user(user)
        
        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AHH0'))
        # imgs.extend(self.driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[3]/a/div/div[2]"))
        # print(self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[3]/a/div/div[2]"))
        # print(imgs)
        for img in imgs[:n_posts]:
            img.click()
            sleep(2)
            try:
                # self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
                self.driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button").click()
            except Exception as e:
                print(e)
            # self.driver.find_elements_by_class_name('ckWGn')[0].click()
            # self.driver.find_elements_by_class_name('_2dDPU  CkGkG')[0].click()
            sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[5]").click()




# Main stuff!!!!

if __name__ == '__main__':
    config_file_path = './config.ini' 
    config = init_config(config_file_path)

    #enter your username to login
    my_bot = InstaBot('yourusername', pw)

    # doesn't work
    # my_bot.get_unfollowers() 

    # my_bot.follow_user("otheruser")

    #enter user to follow here
    my_bot.like_recent_posts('otheruser', 3, True)
    



print("The account being accessed: ", my_bot.username)