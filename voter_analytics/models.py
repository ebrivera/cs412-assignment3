# File: ./voter_analytics/models.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/4/25
# Description: this File creates a profile class for the table
# of Voters. load_data() function loads data from csv.


from django.db import models
from datetime import datetime
# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one individual who voted in Newton, MA.
    VOTER_ID, LAST NAME, FIRST NAME, RESIDENTIAL ADDRESS (STREET NUMBER, STREET NAME, APT NUMBER, ZIP CODE),
    DATE OF BIRTH, DATE OF REGISTRATION, PARTY AFFILIATION (2 CHARACTERS), PRECINCT NUMBER,
    VOTER SCORE + VOTER INDICATION
    '''
    # name
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()

    # address
    res_address_street_num = models.TextField()
    res_address_street_name = models.TextField()
    res_address_apt_num = models.TextField(blank=True)
    res_address_zip_code = models.TextField()

    # dates
    dob = models.DateField()
    date_of_registration = models.DateField()

    # party affiliation (**note, this is a 2-character wide field**))
    party_affiliation = models.CharField(max_length=2)
    # Precinct number
    precinct_number = models.TextField() # initially gave me some trouble

    # voting indication whether or not a given voter participated in
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False) #
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.precinct_number, self.party_affiliation})'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    Voter.objects.all().delete() 
    filename = '/Users/ernestorivera/Desktop/college/spring25/cs412/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    errors = 0
    successes = 0

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Voter
            voter = Voter(
                voter_id = fields[0],
                last_name = fields[1],
                first_name = fields[2],
                res_address_street_num = fields[3],
                res_address_street_name = fields[4],
                res_address_apt_num = fields[5],
                res_address_zip_code = fields[6],
                dob = datetime.strptime(fields[7], '%Y-%m-%d').date(), # trick i learned a while back to fill dates in well
                date_of_registration = datetime.strptime(fields[8], '%Y-%m-%d').date(), # trick i learned a while back to fill dates in well
                party_affiliation = fields[9].strip(),
                precinct_number = fields[10],
                v20state = (fields[11].upper() == 'TRUE'),
                v21town = (fields[12].upper() == 'TRUE'),
                v21primary = (fields[13].upper() == 'TRUE'),
                v22general = (fields[14].upper() == 'TRUE'),
                v23town = (fields[15].upper() == 'TRUE'),
                voter_score = int(fields[16]),
            )
            voter.save()
            print(f'Created voter: {voter}')
            successes += 1
            
        except:
            print(f"Skipped: {fields}")
            errors += 1
    
    print(f'Done. Created {len(Voter.objects.all())} Voters.')
    print(f'Errors: {errors}, Successes: {successes}')