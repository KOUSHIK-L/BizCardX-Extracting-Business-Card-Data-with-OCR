import pandas as pd 
import numpy as npcd
import re
import streamlit as st
from streamlit_option_menu import option_menu 
import pymysql
import easyocr
from PIL import Image

# Python and MySQL integration
mydb = pymysql.connect(host = "127.0.0.1", user ="root", password ="kk@sql")
sql = mydb.cursor()
sql.execute("CREATE DATABASE IF NOT EXISTS bizcard")
sql.execute("USE bizcard")


#  Function to gell all card details
def get_card_details(data):    
    card_data = {"Company_Name":[], "Card_Holder":[], "Designation":[], "Phone_Number":[], "Email_Id":[], "Website":[], "Area":[], "City":[], "State":[], "Pincode":[]}
    for i in range(len(data)):
        # To get WEBSITE_URL
        if "www " in data[i].lower() or "www." in data[i].lower():
            card_data["Website"].append(data[i].lower())
        elif "WWW" in data[i]:
            card_data["Website"].append((data[4] + "." + data[5]).lower())
        # To get EMAIL ID
        elif "@" in data[i]:
            card_data["Email_Id"].append(data[i].lower())
        # To get Phone NUMBER
        elif data[i].startswith('+') or '-' in data[i]:
            card_data["Phone_Number"].append(data[i].replace('-', ''))
            if len(card_data["Phone_Number"]) == 2:
                card_data["Phone_Number"] = " & ".join(card_data["Phone_Number"])
        # To get COMPANY NAME
        elif i == len(data) - 1:
            card_data["Company_Name"].append(data[i].capitalize())
        # To get CARD HOLDER NAME
        elif i == 0:
            card_data["Card_Holder"].append(data[i].capitalize())
        # To get DESIGNATION
        elif i == 1:
            card_data["Designation"].append(data[i].capitalize())
        # To get AREA
        if re.findall('^[0-9].+, [a-zA-Z]+', data[i]):
            card_data["Area"].append(data[i].split(',')[0])
        elif re.findall('[0-9] [a-zA-Z]+', data[i]):
            card_data["Area"].append(data[i])
        # To get CITY NAME
        match1 = re.findall('.+St , ([a-zA-Z]+).+', data[i])
        match2 = re.findall('.+St,, ([a-zA-Z]+).+', data[i])
        match3 = re.findall('^[E].*', data[i])
        if match1:
            card_data["City"].append(match1[0])
        elif match2:
            card_data["City"].append(match2[0])
        elif match3:
            card_data["City"].append(match3[0])
        # To get STATE
        state_match = re.findall('[a-zA-Z]{9} +[0-9]', data[i])
        if state_match:
            card_data["State"].append(data[i][:9])
        elif re.findall('^[0-9].+, ([a-zA-Z]+);', data[i]):
            card_data["State"].append(data[i].split()[-1])
        if len(card_data["State"]) == 2:
            card_data["State"].pop(0)
        # To get PINCODE
        if len(data[i]) >= 6 and data[i].isdigit():
            card_data["Pincode"].append(data[i])
        elif re.findall('[a-zA-Z]{9} +[0-9]', data[i]):
            card_data["Pincode"].append(data[i][10:])
    
    return card_data

# Function to convert image into binary data
def image_to_binary(file):
    with open(file, "rb") as bfile:
        binary_data = bfile.read()
        # Encode the binary data using pymysql.Binary
        encoded_binary = pymysql.Binary(binary_data)
    return encoded_binary

# Paths to business card images
image1 = r"D:\1.png"
image2 = r"D:\2.png"
image3 = r"D:\3.png"
image4 = r"D:\4.png"
image5 = r"D:\5.png"

# Object for EacyOcr.Reader Function
reader = easyocr.Reader(['en'])

# Creating a dictionary for images 
select_image = {image1 :'Business Card-1',
                image2 :'Business Card-2',
                image3 :'Business Card-3',
                image4 :'Business Card-4',
                image5 :'Business Card-5'}

st.set_page_config(page_title='BizCardX', layout='wide')
st.markdown(f'<h1 style="text-align:center; color: #d9138a">BizCardX <br> Extracting Business Card Data with OCR</h1>', unsafe_allow_html=True)

select_menu = option_menu(None, ["About BizCardX", "BizCard Extraction","Bizcard Updation", "BizCard Deletion"],
                       icons=["clipboard2-data", "cloud-download", "file-earmark-plus", "trash"],orientation="horizontal")


if select_menu == "About BizCardX":
    st.subheader('Problem Statement:')
    st.markdown('- Deploy a Streamlit Application that allow to upload a Business card and extract its information using Python library eacy OCR.')
    st.markdown('- Extracted information should include details such as;')
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(':red[ - Company name]')
        st.markdown(':red[ - Card holder name]') 
        st.markdown(':red[ - Designation]')
        st.markdown(':red[ - Phone number]')
        st.markdown(':red[ - Email address]')
    with c2:
        st.markdown(':red[ - Website URL]')
        st.markdown(':red[ - Area]')
        st.markdown(':red[ - City]')
        st.markdown(':red[ - State]')
        st.markdown(':red[ - Pincode]')
    with c3:
        pass
    with c4:
        pass
    st.markdown('- The extracted information then should be displayed in the application interface in a clean, organized manner and should easily allow user;') 
    st.markdown(':red[ - To Alter and Update the Etracted information]')
    st.markdown(':red[ - To Store the Etracted and Updated information into a database along with the uploaded business card image]')
    st.markdown(':red[ - To Delete the Stored information from the database]')
    st.markdown('- The application should have simple and intuitive user interface that guides users through the process')

    st.subheader('Problem Approach:')
    st.markdown('To Solve the Problem, the Approach has been made into different Sections and Steps')
    st.markdown('- First section on Introdction to Problem Statement]')
    st.markdown('- Further sections involve Steps approched in this solution]')
    st.markdown(':red[ - BizCard Extraction - User selected BizCard will be uploaded and the information will be extracted]')
    st.markdown(':red[ - BizCard Updation - User can update the stored information]')
    st.markdown(':red[ - BizCard Deletion - User can delete the selected BizCard information from the database]')
    st.markdown('- Last Section for Conclusion')  

    st.subheader('Tools and Technologies used in this Project involves;')
    st.markdown(':red[ - Python and SQL programming]')
    st.markdown(':red[ - Eacy OCR (Optical Charecter Recognition) python library for Image processing]') 
    st.markdown(':red[ - Streamlit Application]')
    st.markdown(':red[ - MySQL Database]')


if select_menu == "BizCard Extraction":
    extract1, extract2 = st.tabs(['Upload & Extract','Alter & Store'])
    # Display a selectbox in the sidebar
    select_card = st.sidebar.selectbox("**Select a Business Card**", ['', image1, image2, image3, image4, image5], format_func=lambda x: select_image.get(x, x))

    # Display all card images in the sidebar to select 
    for img, card in select_image.items():
        st.sidebar.subheader(f":red[**{card}**]")
        st.sidebar.image(Image.open(img), output_format="JPEG", use_column_width=True)
    
    with extract1:
        st.subheader('In BizCard Extraction - Upload & Extract Section:')
        st.markdown(' -> Select a Business Card image to be uploaded')
        st.markdown(' -> After the image gets uploaded it gets displayed here')
        st.markdown(' -> With the Image selection the BixCared extraction also take place with help of EacyOCR')
        st.markdown(' -> Once Infomation gets extracted it will be displayed as table here')

        if select_card !='':
            st.image(Image.open(select_card), output_format="JPEG", use_column_width=True)

        if select_card != '':
            result = reader.readtext(select_card)
            data = [i[1] for i in result]
            df_image_details = pd.DataFrame(get_card_details(data))
            st.table(df_image_details)
            # Get binary data for the selected image
            selected_image_binary = image_to_binary(select_card)
            # Add the binary data to the DataFrame
            df_image_details["Image"] = [selected_image_binary]
            st.table(df_image_details["Image"])

            
    with extract2:
        st.subheader('In BizCard Extraction - Alter & Store Section:')
        st.markdown(' -> The selected BizCard will be dispalyed for Reference')
        st.markdown(' -> Check for any wrongly processed information')
        st.markdown(' -> If any mismatch found alter the specific data and press enter')
        st.markdown(' -> Once corrected the card details press preview button to get tabular form of altered data')
        st.markdown(' -> Then press Store data button to export the alterd data to databse')

        # Display the selected image
        if select_card != '':
            st.image(Image.open(select_card), output_format="JPEG", use_column_width=True)
            detail1, detail2 = st.columns(2)
            with detail1:
                company_name_ = st.text_input('Company Name', df_image_details['Company_Name'][0])
                card_holder_ = st.text_input('Card Holder', df_image_details['Card_Holder'][0])
                designanation_ = st.text_input('Designation', df_image_details['Designation'][0])
                Phone_number_ = st.text_input('Phone Number', df_image_details['Phone_Number'][0])
                email_id_ = st.text_input('Email Id', df_image_details['Email_Id'][0])
            
                df_image_details['Company_Name'][0] = company_name_
                df_image_details['Card_Holder'][0] = card_holder_
                df_image_details['Designation'][0] = designanation_
                df_image_details['Phone_Number'][0] = Phone_number_
                df_image_details['Email_Id'][0] = email_id_

            with detail2:
                website_ = st.text_input('Website', df_image_details['Website'][0])
                area_ = st.text_input('Area', df_image_details['Area'][0])
                city_ = st.text_input('City', df_image_details['City'][0])
                state_ = st.text_input('State', df_image_details['State'][0])
                pincode_ = st.text_input('Pincode', df_image_details['Pincode'][0])
                
                df_image_details['Website'][0] = website_
                df_image_details['Area'][0] = area_
                df_image_details['City'][0] = city_
                df_image_details['State'][0] = state_
                df_image_details['Pincode'][0] = pincode_


            alter, upload = st.columns(2)
            with alter:
                st.write('')
                Preview = st.button("**Preview Modified Data**")
            with upload:
                st.write('')
                Upload_to_db = st.button("**Store Data into Database**")
            if Preview:
                df_card = df_image_details.drop(['Image'],axis=1)
                st.table(df_card)
                st.table(df_image_details['Image'])
            else:
                pass    

            if Upload_to_db:
                sql.execute("CREATE TABLE IF NOT EXISTS card_details(Company_name TEXT, Card_holder TEXT, Designation TEXT, Phone_number LONGTEXT, Email_id TEXT, Website TEXT, Area TEXT, City TEXT, State TEXT, Pincode VARCHAR(10), Image LONGBLOB)")
                data = pd.read_sql_query('Select company_name FROM card_details',mydb)
                company = ['']
                for card in data['company_name']:
                    company.append(card)

                if company_name_ not in company:
                    insert = "INSERT INTO card_details(Company_name, Card_holder, Designation, Phone_number, Email_id, Website, Area, City, State, Pincode, Image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    for i in range(len(df_image_details)):
                        sql.execute(insert, tuple(df_image_details.iloc[i]))
                        mydb.commit()
                    
                    st.success('**Successfully Data Stored into Database**')
                else:
                        st.error('**Data Already Present in Database**')


if select_menu == "Bizcard Updation":
    st.subheader("In BizCard Updation Section:")
    st.markdown(' -> Select a Card with its Company name for updation')
    st.markdown(' -> Change the card details to update')
    st.markdown(' -> Once changes done press the button to commit it into the Database')
    st.markdown(' -> After updation to check the changes done press button to view the updated Data')

    company = pd.read_sql_query('Select company_name FROM card_details',mydb) 
    company_names = ['']
    for card in company['company_name']:
        company_names.append(card)

    select_company = st.selectbox("Select Company name", company_names)
    if select_company != '':
        sql.execute(f"SELECT Company_name, Card_holder, Designation, Phone_number, Email_id, Website, Area, City, State, Pincode FROM card_details WHERE company_name='{select_company}'")
        info = sql.fetchall()
        if info:
            table_update = pd.DataFrame(info, columns=['Company_name', 'Card_holder',  'Designation', 'Phone_number', 'Email_id', 'Website', 'Area', 'City', 'State', 'Pincode'])
            st.table(table_update)

            st.subheader("Modify Data And Update It In Database")
            update1, updat2 = st.columns(2)
            with update1:
                company_name = st.text_input("Company Name", table_update["Company_name"][0])
                card_holder = st.text_input("Card Holder", table_update["Card_holder"][0])
                designation = st.text_input("Designation", table_update["Designation"][0])
                phone_number = st.text_input("Phone Number", table_update["Phone_number"][0])
                email = st.text_input("Email Id", table_update["Email_id"][0])

            with updat2:
                website = st.text_input("Website", table_update["Website"][0])
                area = st.text_input("Area", table_update["Area"][0])
                city = st.text_input("City", table_update["City"][0])
                state = st.text_input("State", table_update["State"][0])
                pincode = st.text_input("Pincode", table_update["Pincode"][0])

            commit, view = st.columns(2)
            with commit:
                commit_ = st.button("**Commit Changes into DataBase**")
            with view:
                view_ = st.button("**View Updated Data**")

            if commit_:        
                sql.execute(f"UPDATE card_details SET Company_name = '{company_name}',Card_holder='{card_holder}', Designation = '{designation}',Phone_number ='{phone_number}', Email_id = '{email}', Website='{website}',Area = '{area}',City = '{city}',State = '{state}' ,PinCode = '{pincode}' WHERE company_name = '{select_company}'")
                mydb.commit()
                st.success("Changes Commited Successfully!!")
            if view_:    
                sql.execute(f"SELECT Company_name, Card_holder,  Designation, Phone_number, Email_id, Website, Area, City, State, Pincode FROM card_details WHERE company_name ='{select_company}'")
                updated_df = pd.DataFrame(sql.fetchall(),columns=['Company_name', 'Card_holder',  'Designation', 'Phone_number', 'Email_id', 'Website', 'Area', 'City', 'State', 'Pincode'])
                st.table(updated_df)

if select_menu == "BizCard Deletion":
    st.subheader('In BizCard Deletion section:')
    st.markdown(' -> The card Details Table from Database before and after deletion are displayed')
    st.markdown(' -> Select the table to be Droped from Database by chossing its respective Company Name')
    st.markdown(' -> Once selected click on the button to delete the table permanantly from database')
    st.markdown(' -> After Deletion the Success message will be displayed')
    
    st.subheader(':green[Card Details Table before Deletion]')
    df_before = pd.read_sql_query('SELECT Company_name AS "Company Name", Card_holder AS "Card holder Name",  Designation, Phone_number, Email_id, Website, Area, City, State, Pincode FROM card_details',mydb)
    st.table(df_before)

    query = pd.read_sql_query('Select company_name FROM card_details',mydb)
    name = ['']
    for card in query['company_name']:
        name.append(card)
    
    select_name = st.selectbox('**Select a Card to Delete**', name)
    delete = st.button('**Proceed to Delete**')

    if select_name !='' and delete:
        sql.execute(f"DELETE FROM card_details WHERE company_name='{select_name}'")
        mydb.commit()
        if True:
            st.warning('**Successfully Data Delated from Database**')
            st.subheader(':red[Card Details Table after Deletion]')
            df_after = pd.read_sql_query('SELECT Company_name, Card_holder,  Designation, Phone_number, Email_id, Website, Area, City, State, Pincode FROM card_details',mydb)
            st.table(df_after)

            
        st.title('Thank You !!!')
