import sys
import os

sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "BaseLib"))

import DetectChars
import cv2
import DetectPlates
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def run():
    training_data = DetectChars.loadKNNDataAndTrainKNN()

    if not training_data:
        print "Invalid Training Data"
        return

    test_image = cv2.imread("BaseLib/LicPlateImages/6.png")
    if test_image is None:
        print "Failed to load test data"

    plates = DetectPlates.detectPlatesInScene(test_image)
    chars = DetectChars.detectCharsInPlates(plates)

    best_fit = None

    for char in chars:
        if best_fit is None:
            best_fit = char.strChars
        else:
            if abs(len(char.strChars) - 6) < abs(len(best_fit) - 6):
                best_fit = char.strChars

    print "Best Fit: " + best_fit


def get_page(rego):
    driver = webdriver.Chrome()
    driver.get("https://www.service.transport.qld.gov.au/checkrego/application/TermAndConditions.xhtml?windowId=9b2")
    driver.find_element_by_id("tAndCForm:confirmButton").click()
    driver.find_element_by_id("vehicleSearchForm:plateNumber").send_keys(rego)
    driver.find_element_by_id("vehicleSearchForm:confirmButton").click()
    src = driver.page_source
    driver.close()
    return src

if __name__ == '__main__':
    run()
    page = get_page("")
    print page