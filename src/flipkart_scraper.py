import pandas as pd
from bs4 import BeautifulSoup

platform = 'flipkart'
phoneNames = ["Apple iPhone 15", "Apple iPhone 15 Plus", "Apple iPhone 15 Pro", "Apple iPhone 15 Pro Max"]
phoneStorage = ["128 GB", "256 GB", "512 GB", "1 TB"]
phoneInfo = []



def getPhoneDesc(tag):
    return tag.string.strip()

def getPhoneName(tag):
    phoneName = tag.split('(')[0].rstrip()
    return phoneName

def getPhonePrice(tag):
    return tag.string.strip()

def getColor(tag):
    phoneColor = tag.split('(')[-1].split(',')[0]
    return phoneColor

def getStarRating(tag):
    return tag.text.strip()

def getRatingReview(tag):
    phoneRatingTag = tag.span.span
    phoneReviewTag = phoneRatingTag.next_sibling.next_sibling.next_sibling.next_sibling
    return (phoneRatingTag.string.strip(), phoneReviewTag.string.strip())

def getPhoneSpecs(phoneSpecsUlTag):
    specs = str()
    phoneSpecLiTags = phoneSpecsUlTag.find_all('li')

    for phoneSpecLiTag in phoneSpecLiTags:
        singlespec = '• ' + phoneSpecLiTag.text.strip() + '\n'
        specs += singlespec
    
    return specs

def isStorage128(tag):
    return tag.find(phoneStorage[0]) != -1



with open(f"html/{platform}.html", 'r') as fp:
    htmlContent = fp.read()
    soup = BeautifulSoup(htmlContent, 'html.parser')

    phoneDescDivTags = soup.find_all('div', class_='_4rR01T')
    phonePriceDivTags = soup.find_all('div', class_='_30jeq3 _1_WHN1')
    phoneStarRatingDivTags = soup.find_all('div', class_ = '_3LWZlK')
    phoneRRParentSpanTags = soup.find_all('span', class_='_2_R_DZ')
    phoneSpecsUlTags = soup.find_all('ul', class_ ='_1xgFaf')

    for phoneDescDivTag, phonePriceDivTag, phoneStarRatingDivTag, phoneRRParentSpanTag, phoneSpecsUlTag in zip(phoneDescDivTags,phonePriceDivTags,phoneStarRatingDivTags,phoneRRParentSpanTags, phoneSpecsUlTags):
        
        phoneDesc = getPhoneDesc(phoneDescDivTag)
        phoneName = getPhoneName(phoneDesc)
        phonePrice = getPhonePrice(phonePriceDivTag)
        phoneColor = getColor(phoneDesc)
        phoneStarRating = getStarRating(phoneStarRatingDivTag)
        phoneRating, phoneReview = getRatingReview(phoneRRParentSpanTag)
        phoneSpecs = getPhoneSpecs(phoneSpecsUlTag)

        if phoneName == phoneNames[0] and isStorage128(phoneDesc):
            print(phoneNames[0] + " ==> " + phoneColor + " ==> " + phonePrice + " ==> "+ phoneRating + " ==> "+ phoneReview + " ==> "+ phoneStarRating + " ★")
            phoneInfo.append(dict({
                'Model': phoneName,
                'Color': phoneColor,
                'Price': phonePrice,
                'Rating': f"{phoneStarRating} ★",
                'Product Feedbacks': f"{phoneRating} & {phoneReview}",
                'Specifications': phoneSpecs
            }))

df = pd.DataFrame(phoneInfo)
df.to_excel("data/flipkart.xlsx", index=False, sheet_name='Flipkart')














        # if getPhoneName(phoneName) in phoneNames:

        #     if phoneName == phoneNames[0]:
        #         pass

        #     elif phoneName == phoneNames[1]:
        #         pass
            
        #     elif phoneName == phoneNames[2]:
        #         pass

        #     elif phoneName == phoneNames[3]:
        #         pass

        # else:
        #     pass

