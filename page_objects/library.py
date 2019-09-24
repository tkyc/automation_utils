from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class Rooms:

    #Room names
    rooms = dict({
        0: "130D",
        1: "130E",
        2: "130F",
        3: "130G",
        4: "130H",
        5: "130I",
        6: "137",
        7: "138",
        8: "140",
        9: "141",
        10: "312"
    })



class TimeBlocks:
    
    #Time blocks within timetable
    time_blocks = dict({
        0 : "7:30AM",
        1 : "8:00AM",
        2 : "8:30AM",
        3 : "9:00AM",
        4 : "9:30AM",
        5 : "10:00AM",
        6 : "10:30AM",
        7 : "11:00AM",
        8 : "11:30AM",
        9 : "12:00PM",
        10 : "12:30PM",
        11 : "1:00PM",
        12 : "1:30PM",
        13 : "2:00PM",
        14 : "2:30PM",
        15 : "3:00PM",
        16 : "3:30PM",
        17 : "4:00PM",
        18 : "4:30PM",
        19 : "5:00PM",
        20 : "5:30PM",
        21 : "6:00PM",
        22 : "6:30PM",
        23 : "7:00PM",
        24 : "7:30PM",
        25 : "8:00PM",
        26 : "8:30PM",
        27 : "9:00PM",
        28 : "9:30PM",
        29 : "10:00PM",
        30 : "10:30PM",
    })



class Library:

    #A "." within an xpath denotes a child element

    #Hour per time block
    factor = 0.5

    #URL
    url = "https://studyrooms.lib.bcit.ca/day.php?area=2"

    #The timetable containing the time blocks
    timetable = "//table[@id= 'day_main']/tbody"

    #The rows in the timetable. Each row corresponds to a room 
    room_bookings = "//table[@id= 'day_main']/tbody//tr"

    #The the time blocks in a row within the timetable. First index contains room number
    booking_block = ".//td"



    def __init__(self, driver):
        self.driver = driver



    def get_room_schedule(self, index):
        """
        Get the booked schedule for the room at the specified index.

        Args:
            index - The room index (refer to Rooms enum).

        Return:
            Dict. containing booked hours.
        """
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.visibility_of_element_located((By.XPATH, Library.timetable)))

        time_blocks = (self.driver.find_elements(By.XPATH, Library.room_bookings)[index]
                                  .find_elements(By.XPATH, Library.booking_block))

        print(self.get_booked_hours(time_blocks, index))



    def get_booked_hours(self, blocks, index):
        """
        Gets the booked hours for the room given the time block elements.

        Args:
            blocks - The time blocks for the room (Refer to time_blocks in get_room_schedule()).
            index - The room index (refer to Rooms enum).

        Return:
            Dict. containing booked hours.
        """

        #Indicating current time block in time block hashmap when looping over blocks
        hash_block_index = 0

        room = {"room": Rooms.rooms[index], "booked_hours": []}

        #First time block in timetable starts at index 1
        for block in range(1, len(blocks) - 1): 
            block_type = blocks[block].get_attribute("class")

            if block_type == "I private":
                booked_time = (0.5 if blocks[block].get_attribute("colspan") is None
                                   else int(blocks[block].get_attribute("colspan")) 
                                            * Library.factor)

                #Offset is number of blocks from start time to end time for a booked room
                offset = booked_time / Library.factor

                #Get the booked hours for specified block
                #print(self.get_block_hour(offset, hash_block_index))
                room["booked_hours"].append(self.get_block_hour(offset, hash_block_index))
                hash_block_index += offset

            else:
                hash_block_index += 1

        return room



    def get_block_hour(self, offset, hash_block_index):
        """
        Get the booked time range.

        Args:
            offset - Number of blocks from the start time to the end time.
            hash_block_index - The index of the current time block.

        Return:
            The booked time range.
        """
        return (TimeBlocks.time_blocks[hash_block_index] + " - " 
              + TimeBlocks.time_blocks[hash_block_index + offset])