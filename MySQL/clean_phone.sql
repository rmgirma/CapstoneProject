update cdw_sapp_customer set CUST_PHONE = INSERT(CUST_PHONE, 4, 0, '-') where length(CUST_PHONE) = 7;
update cdw_sapp_customer set CUST_PHONE = concat('(555)',CUST_PHONE) where length(CUST_PHONE) = 8;
SELECT * FROM creditcard_capstone.cdw_sapp_customer;