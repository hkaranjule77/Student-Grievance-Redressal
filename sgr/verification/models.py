from django.db import models

class DBDetail(models.Model):
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    hostname = models.CharField(max_length = 20)
    db_name = models.CharField(max_length = 35)
    db_type = models.CharField(max_length = 15)
    
    db_types = ( 'MySQL', 'PostgreSQL', 'SQLite3' )
    
    

class TableDetail(models.Model):
    name = models.CharField(max_length = 25)
    type = models.CharField(max_length = 25)
    year = models.CharField(max_length = 20, null = True, blank = True)
    branch = models.CharField(max_length = 20, null = True, blank = True)
    year_col_name = models.CharField(max_length = 20, null = True, blank = True)
    branch_col_name = models.CharField(max_length = 20, null = True, blank = True)
    student_id_col_name = models.CharField(max_length = 20)
    name_storage_type = models.CharField(max_length = 20)
    first_name_col_name = models.CharField(max_length = 20, null = True, blank = True)
    last_name_col_name = models.CharField(max_length = 20, null = True, blank = True)
    full_name_col_name = models.CharField(max_length = 20, null = True, blank = True)
    full_name_type = models.CharField(max_length = 20, null = True, blank = True)
    email_col_name = models.CharField(max_length = 20)
    contact_no_col_name = models.CharField(max_length = 20)
    
    table_types = ( 'All Year data in One Table',
                    'Year-Wise Table',
                    'Branch-Wise Table' )
    
    name_storage_types = ( 'Firstname, Lastname in separate column',
                   "Full name in same column of format 'Lastname Firstname Middlename'",
                   "Full name in same column of format 'Firstname Middlename Lastname'")
    