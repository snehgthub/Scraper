import os
import pandas as pd
from bs4 import BeautifulSoup

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


def getVarName(variable):
    for name in globals():
        if id(globals()[name]) == id(variable):
            return name
    for name in locals():
        if id(locals()[name]) == id(variable):
            return name
    return None

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
        singlespec = '• ' + phoneSpecLiTag.text.strip() + '\n\n'
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
            'Available Colors': f"• {phoneColor} \n",
            'Internal Storage': phoneStorage,
            'Price': phonePrice,
            'Rating': f"{phoneStarRating} ★",
            'Product Feedbacks': f"{phoneRating} & {phoneReview}",
            'Specifications': phoneSpecs
            })               
    dataframe = dataframe._append(phoneInfoDict, ignore_index = True)

    if not isPhoneInfoinDict(phoneInfoDict, phoneInfoListDict): # ERROR
        # print(phoneName + " ==> " + phoneColor + " ==> " + phonePrice + " ==> "+ phoneRating + " ==> "+ phoneReview + " ==> "+ phoneStarRating + " ★" + " ==> " + phoneStorage)
        phoneInfoListDict.append(phoneInfoDict)
    
    return dataframe

def createExcelEntry(df, writer, varName):

    df.drop_duplicates(inplace=True)

    column_to_merge = 'Available Colors'
    unique_identifier_columns = ['Model', 'Internal Storage', 'Price', 'Rating', 'Product Feedbacks', 'Specifications']

    merged_df = df.groupby(unique_identifier_columns, as_index=False)[column_to_merge].agg('\n'.join)

    merged_df = merged_df[[unique_identifier_columns[0], column_to_merge, unique_identifier_columns[1], unique_identifier_columns[2], unique_identifier_columns[3], unique_identifier_columns[4], unique_identifier_columns[5]]]
    
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
    worksheet.set_column('G:G', 42.86, format_left_center)

    worksheet.set_row(1, 154.5)


for file in os.listdir('html-flipkart'):

    with open(f"html-flipkart/{file}", 'r') as fp:
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
    