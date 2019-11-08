-----Creating the Database----
CREATE DATABASE "drugDB"
    WITH 
    OWNER = root
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

drop table drug_review_data;
-----Creating tables------
create table drug_review_data (
   uniqueID integer primary key not null,
   drugName varchar not null,
   condition varchar not null,
   review text not null,
   rating integer not null,
   review_date date not null,
   usefulCount integer not null,
   review_outcome varchar not null
   );
   

 select * from drug_review_data limit 10;