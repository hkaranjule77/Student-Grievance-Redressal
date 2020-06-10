from django.db import models
from django.utils import timezone
from django.db.models import Q

from user.models import Student, Member
from sgr.settings import BASE_DIR

from datetime import date
import os

class Complain(models.Model):
    id = models.CharField(max_length = 12, primary_key = True)
    subject = models.CharField(max_length = 35)
    category = models.CharField(max_length = 30)
    sub_category = models.CharField(max_length = 30)
    brief = models.TextField()
    complainer = models.ForeignKey(Student, on_delete = models.CASCADE)
    file = models.FileField(upload_to = 'complain/', blank = True, null = True)
    reg_datetime = models.DateTimeField(default = timezone.now)
    solved = models.BooleanField(default = False)
    approved = models.BooleanField(default = False)
    solver = models.ForeignKey(Member, on_delete =  models.CASCADE, blank = True, null = True)
    solve_date = models.DateField(blank = True, null = True)
    
    ### VARIABLE_CONSTANTS
    
    categories = ( 'Administrative Office', 'Infrastructure', 'Committee/Teacher', 'Management activites', 'Other' )
    sub_categories = ( { 'Admission' : 'A', 'Concession' : 'C', 'Scholarship/Freeship' : 'S', 'Other' : 'O' },
                       { 'Canteen' : 'C', 'Classroom' : 'A', 'Gymnasium' : 'G','Library' : 'L', 'Lift' : 'L',
                         'Parking' : 'P', 'Playground' : 'Y', 'Practical Lab' : 'R', 'Toilets/Washrooms' : 'T',
                         'Workshop' : 'W', 'Xerox Office' : 'X', 'Other' : 'O' },
                       { 'Branch Committees' : 'B', 'E-Cell' : 'E', 'NSS' : 'N', 'Women Development' : 'W', 'Other' : 'O' },
                       { 'Attendance' : 'A', 'Cleanliness' : 'C', 'Timetable' : 'T', 'Other' : 'O'},
                       { 'Other' : 'O', }
                     )
    
    ### Adding methods
    
    def generate_id(category, sub_category):
        complain = Complain.objects.all().last()
        today = date.today()
        curr_date = today.strftime('%y%m%d')
        count_file = open(os.path.join(BASE_DIR, 'count_files/complain_id.txt'), 'r')
        count_data = count_file.read().split('\n')
        count_file = open(os.path.join(BASE_DIR, 'count_files/complain_id.txt'), 'w')
        if curr_date != count_data[0]:
            data = ''
            for section in Complain.sub_categories:
                for sub_cat in section:
                    if sub_cat == sub_category:
                        data+='1 '
                    else:
                        data+='0 '
                data+='\n'
            data = curr_date+ '\n' + data
            count_file.write(data)
            count_file.close()
            generated_id = '0'
        else:
            for index in range(len(count_data)):
                print('b',count_data[index])
                count_data[index] = count_data[index].split(' ')
                print('a',count_data[index])
            print(count_data)
            cat_index = 1
            count_file.write(curr_date+'\n')
            for cat in Complain.categories:
                sub_index = 0
                for sub in Complain.sub_categories[cat_index-1].keys():
                    if (sub == sub_category and cat == category):
                        generated_id = count_data[cat_index][sub_index]
                        count_data[cat_index][sub_index] = str( int(generated_id) + 1 )
                        print('generated_id', generated_id)
                    print()
                    print('count data', count_data)
                    print('cat_index', cat_index)
                    print('sub_index', sub_index)
                    print()
                    count_file.write(count_data[cat_index][sub_index]+' ')
                    sub_index += 1
                count_file.write('\n')
                cat_index += 1
            count_file.close()
        while len(generated_id) < 4:
            generated_id = '0' + generated_id
        generated_id = curr_date + category[0] + Complain.sub_categories[Complain.categories.index(category)][sub_category] + generated_id
        return generated_id
        
    
    def init(request):
        complain = Complain()
        complain.subject = request.POST.get('subject')
        complain.category = request.POST.get('category')
        complain.sub_category = request.POST.get('sub_category')
        complain.brief = request.POST.get('brief')
        complain.complainer = Student.objects.get(user = request.user)
        file = request.FILES.get('file')
        return complain
        
    def is_valid(self):
        valid = True
        if self.subject == '' or self.subject == None:
            print(1)
            valid = False
        elif self.category == '' or self.category == None:
            valid = False
            print(2)
        elif self.sub_category == '' or self.sub_category == None:
            valid = False
            print(3)
        elif self.brief == '' or self.brief == None:
            valid = False
            print(4)
        elif self.complainer == None:
            valid = False
            print(5)
        print('valid or not', valid)
        if valid:
            self.id = Complain.generate_id(self.category, self.sub_category)
        return valid
    
    ### Searching methods
    
    def get_filename(self):
        return self.file.name[9:]
    
    def search_id(query):
        return Q(id__icontains = query)

    def search_subject(query):
        return Q(subject__icontains = query)
    
    def search_category(query):
        return Q(category__icontains = query)
    
    def search_sub_category(query):
        return Q(sub_category__icontains = query)
    
    def search_brief(query):
        return Q(brief__icontains = query)
	
	
	
##class Note(models.Model):
##    note = models.TextField()
##    file = models.FileField(upload_to = 'note/', blank = True, null = True)
##    complain = models.ForeignKey(Complain, on_delete = models.CASCADE)
##    reg_datetime = models.DateTimeField(default = timezone.now)
##    solver = models.ForeignKey(Member, on_delete = models.CASCADE)