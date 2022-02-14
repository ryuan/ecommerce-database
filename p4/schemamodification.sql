--Adding column taxExempt to track tax-exempt customers who provided resale certificate
ALTER TABLE customers
ADD taxExempt boolean DEFAULT 0
;


--Remove the collection description attribute from the collections relation
ALTER TABLE collections
DROP c_description
;
