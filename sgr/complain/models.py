from django.db import models
from django.utils import timezone
from django.db.models import Q

from datetime import date
import os

from user.models import Student, Member
from thread.models import Thread
from sgr.settings import BASE_DIR

class Complain(models.Model):
    
    ### CONSTANTS
    categories = ( ('A','Administrative Office'),
                   ('I', 'Infrastructure'),
                   ('C', 'Committee/Teacher'),
                   ('M', 'Management activites'),
                   ('O', 'Other' )
                   )
    sub_categories = ( ( ('A', 'Admission'), ('C', 'Concession'), ('S', 'Scholarship/Freeship'),
                         ('O', 'Other') ),
                       ( ('C', 'Canteen'), ('A', 'Classroom'), ('G', 'Gymnasium'), ('L', 'Library'),
                         ('L', 'Lift'), ('P', 'Parking'), ('Y', 'Playground'),
                         ('R', 'Practical Lab'), ('T', 'Toilets/Washrooms'), ('W', 'Workshop'),
                         ('X', 'Xerox Office'), ('O', 'Other') ),
                       ( ('B', 'Branch Committees'), ('E', 'E-Cell'), ('N', 'NSS'), ('W', 'Women Development'),
                         ('O', 'Other') ),
                       ( ('A', 'Attendance'), ('C', 'Cleanliness'), ('T', 'Timetable'),
                         ('O', 'Other') ),
                       ( ('O', 'Other'), )
                     )
    
    id = models.CharField(max_length = 12, primary_key = True)
    subject = models.CharField(max_length = 35)
    category = models.CharField(max_length = 30)
    sub_category = models.CharField(max_length = 30)
    brief = models.TextField()
    file = models.FileField(upload_to = 'complain/', blank = True, null = True)
    complainer = models.ForeignKey(Student, on_delete = models.CASCADE)
    reg_datetime = models.DateTimeField(default = timezone.now)
    sorted = models.BooleanField(default = False)
    rejected = models.BooleanField(default = False)
    rejeced_msg = models.TextField(null = True, blank = True)
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE, null = True, blank = True)
    pinned_in_thread = models.BooleanField(default = False)
    threaded_by = models.ForeignKey(Member, on_delete = models.CASCADE, null = True, blank = True)
    threaded_at = models.DateTimeField(null = True, blank = True)
    
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
            for category_wise in Complain.sub_categories:
                for code, sub_cat in category_wise:
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
                count_data[index] = count_data[index].split(' ')
            cat_index = 1
            count_file.write(curr_date+'\n')
            for cat_code, cat in Complain.categories:
                sub_index = 0
                for sub_cat_code, sub in Complain.sub_categories[cat_index-1]:
                    if (sub == sub_category and cat == category):
                        generated_id = count_data[cat_index][sub_index]
                        count_data[cat_index][sub_index] = str( int(generated_id) + 1 )
                        code = cat_code + sub_cat_code
                    count_file.write(count_data[cat_index][sub_index]+' ')
                    sub_index += 1
                count_file.write('\n')
                cat_index += 1
            count_file.close()
        while len(generated_id) < 4:
            generated_id = '0' + generated_id
        generated_id = curr_date + code + generated_id
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
            valid = False
        elif self.category == '' or self.category == None:
            valid = False
        elif self.sub_category == '' or self.sub_category == None:
            valid = False
        elif self.brief == '' or self.brief == None:
            valid = False
        elif self.complainer == None:
            valid = False
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



class Note(models.Model):
    note = models.TextField()
    file = models.FileField(upload_to = 'note/', blank = True, null = True)
    complain = models.ForeignKey(Complain, on_delete = models.CASCADE)
    reg_datetime = models.DateTimeField(default = timezone.now)
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE)
    pinned_in_thread = models.BooleanField(default = False)
    solver = models.ForeignKey(Member, on_delete = models.CASCADE)
    
    def init_all(self, request):
        self.note = request.POST.get('note')
        self.file = request.POST.get('file')
        id = request.POST.get('complain_id')
        if id != None and id != '':
            self.complain = Complain.objects.get(id = id)
        self.solver = Member.objects.get(user = request.user)
    
    def is_valid(self):
        valid = True
        if self.note == '' or self.note == None:
            valid = False
        return valid
