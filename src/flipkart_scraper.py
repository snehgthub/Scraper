import os
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook

platform = 'flipkart'
phoneNames = ["Apple iPhone 15", "Apple iPhone 15 Plus", "Apple iPhone 15 Pro", "Apple iPhone 15 Pro Max"]
phoneStorageVariants = ["128 GB", "256 GB", "512 GB", "1 TB"]
phoneInfoListDict = []

df_15_128GB = pd.DataFrame()
df_15_Plus_128GB = pd.DataFrame()
df_15_Pro_128GB = pd.DataFrame()
df_15_ProMax_128GB = pd.DataFrame()

df_15_256GB = pd.DataFrame()
df_15_Plus_256GB = pd.DataFrame()
df_15_Pro_256GB = pd.DataFrame()
df_15_ProMax_256GB = pd.DataFrame()

df_15_512GB = pd.DataFrame()
df_15_Plus_512GB = pd.DataFrame()
df_15_Pro_512GB = pd.DataFrame()
df_15_ProMax_512GB = pd.DataFrame()

df_15_Pro_1TB = pd.DataFrame()
df_15_ProMax_1TB = pd.DataFrame()

def getPhoneDesc(tag):
    return tag.string.strip()

def getPhoneName(tag):
    phoneName = tag.split('(')[0].rstrip()
    return phoneName

def getColor(tag):
    phoneColor = tag.split('(')[-1].split(',')[0]
    return phoneColor

def getPhoneStorage(tag):
    phoneStorage = tag.split(',')[-1][:-1].strip()
    return phoneStorage

def getPhonePrice(tag):
    return tag.string.strip()

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

def isPhoneInfoinDict(phoneInfoDict, phoneInfoListDict): # ERROR here
    return any(phoneInfoDict.items() <= d.items() for d in phoneInfoListDict)

def isStorage128GB(tag):
    return tag.strip().find(phoneStorageVariants[0]) != -1

def isStorage256GB(tag):
    return tag.strip().find(phoneStorageVariants[1]) != -1

def isStorage512GB(tag):
    return tag.strip().find(phoneStorageVariants[2]) != -1

def isStorage1TB(tag):
    return tag.strip().find(phoneStorageVariants[3]) != -1

def createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, dataframe):
    phoneInfoDict = dict({
            'Model': phoneName,
            'Color': phoneColor,
            'Internal Storage': phoneStorage,
            'Price': phonePrice,
            'Rating': f"{phoneStarRating} ★",
            'Product Feedbacks': f"{phoneRating} & {phoneReview}",
            'Specifications': phoneSpecs
            })
                    
    dataframe = dataframe._append(phoneInfoDict, ignore_index = True) # This is not getting executed so returning None on page 2
    # UPDATE: Made it work by using drop_duplicates() method of dataframe

    if not isPhoneInfoinDict(phoneInfoDict, phoneInfoListDict): # ERROR
        # print(phoneName + " ==> " + phoneColor + " ==> " + phonePrice + " ==> "+ phoneRating + " ==> "+ phoneReview + " ==> "+ phoneStarRating + " ★" + " ==> " + phoneStorage)
        phoneInfoListDict.append(phoneInfoDict)
        # dataframe was initially inside this but iphone 15 GREEN got repeated twice hence it never got executed and value was set to None
        # print(phoneInfoDict)

    
    return dataframe  # Decide where to put this

for file in os.listdir('html'):

    with open(f"html/{file}", 'r') as fp:
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
            phoneStorage = getPhoneStorage(phoneDesc)

            if phoneName in phoneNames:
                if phoneName == phoneNames[0] and isStorage128GB(phoneDesc):
                    df_15_128GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_128GB)

                elif phoneName == phoneNames[0] and isStorage256GB(phoneDesc):
                    df_15_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_256GB)
                
                elif phoneName == phoneNames[0] and isStorage512GB(phoneDesc):
                    df_15_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_512GB)

                elif phoneName == phoneNames[1] and isStorage128GB(phoneDesc):
                    df_15_Plus_128GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Plus_128GB)
                
                elif phoneName == phoneNames[1] and isStorage256GB(phoneDesc):
                    df_15_Plus_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Plus_256GB)
                
                elif phoneName == phoneNames[1] and isStorage512GB(phoneDesc):
                    df_15_Plus_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Plus_512GB)
                
                elif phoneName == phoneNames[2] and isStorage128GB(phoneDesc):
                    df_15_Pro_128GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Pro_128GB)
                
                elif phoneName == phoneNames[2] and isStorage256GB(phoneDesc):
                    df_15_Pro_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Pro_256GB)
                
                elif phoneName == phoneNames[2] and isStorage512GB(phoneDesc):
                    df_15_Pro_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Pro_512GB)
                
                elif phoneName == phoneNames[2] and isStorage1TB(phoneDesc):
                    df_15_Pro_1TB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_Pro_1TB)
                               
                elif phoneName == phoneNames[3] and isStorage256GB(phoneDesc):
                    df_15_ProMax_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_ProMax_256GB)
                
                elif phoneName == phoneNames[3] and isStorage512GB(phoneDesc):
                    df_15_ProMax_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_ProMax_512GB)
                
                elif phoneName == phoneNames[3] and isStorage1TB(phoneDesc):
                    df_15_ProMax_1TB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneRating, phoneReview, phoneSpecs, df_15_ProMax_1TB)


with pd.ExcelWriter('data/flipkart.xlsx') as writer:
    df_15_128GB.drop_duplicates(inplace=True)
    df_15_128GB.to_excel(writer, sheet_name='15_128GB', index=False)

    df_15_256GB.drop_duplicates(inplace=True)
    df_15_256GB.to_excel(writer, sheet_name='15_256GB', index=False)

    df_15_512GB.drop_duplicates(inplace=True)
    df_15_512GB.to_excel(writer, sheet_name='15_512GB', index=False)

    df_15_Plus_128GB.drop_duplicates(inplace=True)
    df_15_Plus_128GB.to_excel(writer, sheet_name='15_Plus_128GB', index=False)

    df_15_Plus_256GB.drop_duplicates(inplace=True)
    df_15_Plus_256GB.to_excel(writer, sheet_name='15_Plus_256GB', index=False)

    df_15_Plus_512GB.drop_duplicates(inplace=True)
    df_15_Plus_512GB.to_excel(writer, sheet_name='15_Plus_512GB', index=False)

    df_15_Pro_128GB.drop_duplicates(inplace=True)
    df_15_Pro_128GB.to_excel(writer, sheet_name='15_Pro_128GB', index=False)

    df_15_Pro_256GB.drop_duplicates(inplace=True)
    df_15_Pro_256GB.to_excel(writer, sheet_name='15_Pro_256GB', index=False)

    df_15_Pro_512GB.drop_duplicates(inplace=True)
    df_15_Pro_512GB.to_excel(writer, sheet_name='15_Pro_512GB', index=False)

    df_15_Pro_1TB.drop_duplicates(inplace=True)
    df_15_Pro_1TB.to_excel(writer, sheet_name='15_Pro_1TB', index=False)

    df_15_ProMax_256GB.drop_duplicates(inplace=True)
    df_15_ProMax_256GB.to_excel(writer, sheet_name='15_ProMax_256GB', index=False)

    df_15_ProMax_512GB.drop_duplicates(inplace=True)
    df_15_ProMax_512GB.to_excel(writer, sheet_name='15_ProMax_512GB', index=False)

    df_15_ProMax_1TB.drop_duplicates(inplace=True)
    df_15_ProMax_1TB.to_excel(writer, sheet_name='15_ProMax_1TB', index=False)


# print(phoneInfoListDict)

