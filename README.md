For testing purposes
I have the following users
id  username    email   password_hash   is_admin
3	"test_user"	"test@test.com"	"$2b$12$iOCOfYc3sgFLRaEt4rEykexTzGWRlZ0C3OJqp/gLEoRoAFeLI0JQ6"	false
4	"test_admin"	"test_admin@test.com"	"$2b$12$iOCOfYc3sgFLRaEt4rEykexTzGWRlZ0C3OJqp/gLEoRoAFeLI0JQ6"	true
The password for both is 'pass'

@startchen
left to right direction

entity Person {
id: INT
gender: ENUM
first_name: STRING
middle_name: STRING
last_name: STRING
profile_picture: IMAGE
}

entity Address {
id: INT
person_id : INT FK
is_permanent: BOOL
first_line: STRING
second_line: STRING
pin_code: INT
state: STRING
country: STRING
landmark: STRING
}

entity Important_Dates {
person_id : INT FK
date_of_birth: DATE 
date_of_death: DATE
}

entity Contact_Details {
id: INT
person_id : INT FK
country_code: INT
mobile_no: INT
email: EMAIL
}

entity Record {
id: INT
person_id : INT FK
created_at: DATETIME
created_by: INT
updated_at: DATETIME
updated_by: INT
}

relationship Person_Address {
}

Person =1= Person_Address
Person_Address =N= Address

relationship Person_Dates {
}

Person =1= Person_Dates
Person_Dates =1= Important_Dates

relationship Person_Contact {
}

Person =1= Person_Contact
Person_Contact =1= Contact_Details

relationship Person_Record {
}

Person =1= Person_Record 
Person_Record =1= Record 


@endchen
