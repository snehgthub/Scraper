import os
import re
from bs4 import BeautifulSoup
import pandas as pd

platform = 'amazon'
phoneNames = ["Apple iPhone 15", "Apple iPhone 15 Plus", "Apple iPhone 15 Pro", "Apple iPhone 15 Pro Max"]
phoneStorageVariants = ["128 GB", "256 GB", "512 GB", "1 TB"]
phoneInfoListDict = []
count = 0

files = os.listdir('html-amazon')
files.reverse()

df = pd.DataFrame()

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

def getVarName(variable):
    for name in globals():
        if id(globals()[name]) == id(variable):
            return name
    for name in locals():
        if id(locals()[name]) == id(variable):
            return name
    return None

def getStarRatingsTags(soup):
    pattern = pattern = re.compile(r'a-icon\s+a-icon-star-small\s+a-star-small-(5|4-5|4|3-5|3|)\s+aok-align-bottom')
    ratingItalicTag = soup.find('i', class_=pattern)
    ratingSpanTags = []

    ratingSpanTag = ratingItalicTag.contents[1]

    return ratingSpanTag

def getPhoneInfo(tag):
    return tag.string.strip()

def getPhoneName(tag):
    return tag.string.split('(')[0].strip()

def getPhonePrice(tag):
    return tag.string.strip()

def getPhoneStorage(tag):
    return tag.string.split('-')[-1].strip()

def getPhoneColor(tag):
    return tag.string.split('(')[-1].split(')')[0].strip()

def getPhoneStarRating(tag):
    return tag.string.split()[0].strip()

def getPhoneFeedback(tag):
    return tag.string.strip()

def isPhoneInfoinDict(phoneInfoDict, phoneInfoListDict):
    return any(phoneInfoDict.items() <= d.items() for d in phoneInfoListDict)

def isStorage128GB(tag):
    return tag.strip().find(phoneStorageVariants[0]) != -1

def isStorage256GB(tag):
    return tag.strip().find(phoneStorageVariants[1]) != -1

def isStorage512GB(tag):
    return tag.strip().find(phoneStorageVariants[2]) != -1

def isStorage1TB(tag):
    return tag.strip().find(phoneStorageVariants[3]) != -1

def createDataframe(phoneName, phoneStorage, phoneColor, phonePrice, phoneStarRating, phoneFeedback, dataframe):
    phoneInfoDict = dict({
                    'Model': phoneName,
                    'Available Colors': f"• {phoneColor} \n",
                    'Internal Storage': phoneStorage,
                    'Price': f"₹{phonePrice}",
                    'Rating': f"{phoneStarRating} ★",
                    'Product Feedbacks': f"{phoneFeedback} Ratings"
                })
    
    dataframe = dataframe._append(phoneInfoDict, ignore_index=True)

    if not isPhoneInfoinDict(phoneInfoDict, phoneInfoListDict):
        # print(phoneName + " ==> "+ phoneColor + " ==> "+ phoneStorage + " ==> " + phonePrice + " ==> " + phoneStarRating + " ==> " + phoneFeedback)
        phoneInfoListDict.append(phoneInfoDict)
    
    return dataframe

def createExcelEntry(df, writer, varName):
    column_to_merge = 'Available Colors'
    unique_identifier_columns = ['Model', 'Internal Storage', 'Price', 'Rating', 'Product Feedbacks']

    if not df.empty:
        df.drop_duplicates(inplace=True)
        merged_df = df.groupby(unique_identifier_columns, as_index=False)[column_to_merge].agg('\n'.join)

        merged_df = merged_df[[unique_identifier_columns[0], column_to_merge, unique_identifier_columns[1], unique_identifier_columns[2], unique_identifier_columns[3], unique_identifier_columns[4]]]
        
        sheet_name = varName.split('df_')[-1]

        merged_df.to_excel(writer, sheet_name=sheet_name, index=False)

        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]

        format_center_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        format_left_center = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap': True})

        worksheet.set_column('A:A', 21.43, format_center_center)
        worksheet.set_column('B:B', 18.14, format_left_center)
        worksheet.set_column('C:C', 17.86, format_center_center)
        worksheet.set_column('D:D', 16.43, format_center_center)
        worksheet.set_column('E:E', 13.57, format_center_center)
        worksheet.set_column('F:F', 28.57, format_center_center)

        worksheet.set_row(1, 158.5)
        

for file in files:
    with open(f"html-amazon/{file}", 'r') as f:
        htmlContent = f.read()
        soup = BeautifulSoup(htmlContent, 'html.parser')
        phoneDivContainer = soup.find_all('div', class_='puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v3r8vhjnob15102b2lwfscmu1lk s-latency-cf-section puis-card-border')
        for phone in phoneDivContainer:
            with open(f"temp-html/{count}.html", 'w') as f:
                phone = str(phone)
                f.write(phone)
                count+=1
        tempFiles = os.listdir('temp-html')
        
        for tempFile in tempFiles: 
            with open(f"temp-html/{tempFile}", 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

                phoneInfoSpanTag = soup.find('span', class_='a-size-medium a-color-base a-text-normal')
                phoneInfo = getPhoneInfo(phoneInfoSpanTag)
                phoneName = getPhoneName(phoneInfoSpanTag)

                if phoneName in phoneNames:
                    phonePriceSpanTag = soup.find('span', class_='a-price-whole')
                    phoneStarRatingTag = getStarRatingsTags(soup)
                    phoneFeedbackTag = soup.find('span', class_='a-size-base s-underline-text')
                    phoneStorage = getPhoneStorage(phoneInfoSpanTag)
                    phoneColor = getPhoneColor(phoneInfoSpanTag)
                    phonePrice = getPhonePrice(phonePriceSpanTag)
                    phoneStarRating = getPhoneStarRating(phoneStarRatingTag)
                    phoneFeedback = getPhoneFeedback(phoneFeedbackTag)
                
                
                    if phoneName == phoneNames[0] and isStorage128GB(phoneInfo):
                        df_15_128GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_128GB)

                    elif phoneName == phoneNames[0] and isStorage256GB(phoneInfo):
                        df_15_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_256GB)
                    
                    elif phoneName == phoneNames[0] and isStorage512GB(phoneInfo):
                        df_15_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_512GB)

                    elif phoneName == phoneNames[1] and isStorage128GB(phoneInfo):
                        df_15_Plus_128GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Plus_128GB)
                    
                    elif phoneName == phoneNames[1] and isStorage256GB(phoneInfo):
                        df_15_Plus_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Plus_256GB)
                    
                    elif phoneName == phoneNames[1] and isStorage512GB(phoneInfo):
                        df_15_Plus_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Plus_512GB)
                    
                    elif phoneName == phoneNames[2] and isStorage128GB(phoneInfo):
                        df_15_Pro_128GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Pro_128GB)
                    
                    elif phoneName == phoneNames[2] and isStorage256GB(phoneInfo):
                        df_15_Pro_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Pro_256GB)
                    
                    elif phoneName == phoneNames[2] and isStorage512GB(phoneInfo):
                        df_15_Pro_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Pro_512GB)
                    
                    elif phoneName == phoneNames[2] and isStorage1TB(phoneInfo):
                        df_15_Pro_1TB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_Pro_1TB)
                                
                    elif phoneName == phoneNames[3] and isStorage256GB(phoneInfo):
                        df_15_ProMax_256GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_ProMax_256GB)
                    
                    elif phoneName == phoneNames[3] and isStorage512GB(phoneInfo):
                        df_15_ProMax_512GB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_ProMax_512GB)
                    
                    elif phoneName == phoneNames[3] and isStorage1TB(phoneInfo):
                        df_15_ProMax_1TB = createDataframe(phoneName, phoneColor, phoneStorage, phonePrice, phoneStarRating, phoneFeedback, df_15_ProMax_1TB)

        os.system('rm temp-html/*')
os.system('rmdir temp-html/')

with pd.ExcelWriter(f"data/{platform}.xlsx") as writer:
    createExcelEntry(df_15_128GB, writer, getVarName(df_15_128GB))
    createExcelEntry(df_15_256GB, writer, getVarName(df_15_256GB))
    createExcelEntry(df_15_512GB, writer, getVarName(df_15_512GB))

    createExcelEntry(df_15_Plus_128GB, writer, getVarName(df_15_Plus_128GB))
    createExcelEntry(df_15_Plus_256GB, writer, getVarName(df_15_Plus_256GB))
    createExcelEntry(df_15_Plus_512GB, writer, getVarName(df_15_Plus_512GB))
    
    createExcelEntry(df_15_Pro_128GB, writer, getVarName(df_15_Pro_128GB))
    createExcelEntry(df_15_Pro_256GB, writer, getVarName(df_15_Pro_256GB))
    createExcelEntry(df_15_Pro_512GB, writer, getVarName(df_15_Pro_512GB))
    createExcelEntry(df_15_Pro_1TB, writer, getVarName(df_15_Pro_1TB))

    createExcelEntry(df_15_ProMax_256GB, writer, getVarName(df_15_ProMax_256GB))
    createExcelEntry(df_15_ProMax_512GB, writer, getVarName(df_15_ProMax_512GB))
    createExcelEntry(df_15_ProMax_1TB, writer, getVarName(df_15_ProMax_1TB))