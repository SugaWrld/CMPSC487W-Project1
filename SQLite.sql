
create table access (
ID int not null,
check_in timestamp not null,
check_out timestamp,
primary key (ID, check_in)
);


create table users (
name varchar(100) not null,
ID int not null,
type varchar(20) check ( type IN ('student', 'faculty member', 'staff member', 'janitor')) not null,
status varchar(10) check ( status IN ('active', 'suspended')) not null,
primary key (ID)
);

create table admins (
username varchar(100) not null,
password varchar(20) not null,
primary key (username)
);


CREATE TRIGGER delete_expire_data 
BEFORE INSERT ON access
FOR EACH ROW
BEGIN
	DECLARE current_time TIMESTAMP;
	SET current_time = DATE_SUB(NOW, INTERVAL 5 YEAR);
	
	DELETE FROM access
	WHERE check_in < current_time;
END;