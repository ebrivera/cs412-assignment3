# File: ./voter_analytics/views.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/4/25
# Description:This is the django part that returns 
# all views for all the instances of Voter(s) including
# the graphs and the details of voter(s)


from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objs as go


class VotersListView(ListView):
    '''View to display voter records'''

    template_name = 'voter_analytics/records.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['min_years'] = [i for i in range(1900, 2024)]
        context['max_years'] = [i for i in range(1900, 2024)]
        return context

    def get_queryset(self):
        
        # start with entire queryset
        voters = super().get_queryset()


        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation != '':
                voters = voters.filter(party_affiliation=party_affiliation)
        if 'min_years' in self.request.GET:
            min_year = self.request.GET['min_years']
            if min_year != '':
                voters = voters.filter(dob__year__gte=min_year)
        if 'max_years' in self.request.GET:
            max_year = self.request.GET['max_years']
            if max_year != '':
                voters = voters.filter(dob__year__lte=max_year)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score != '':
                voters = voters.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state != '':
                if v20state == 'True':
                    voters = voters.filter(v20state=True)
                else:
                    voters = voters.filter(v20state=False)
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town != '':
                if v21town == 'True':
                    voters = voters.filter(v21town=True)
                else:
                    voters = voters.filter(v21town=False)
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary != '':
                if v21primary == 'True':
                    voters = voters.filter(v21primary=True)
                else:
                    voters = voters.filter(v21primary=False)
        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general != '':
                if v22general == 'True':
                    voters = voters.filter(v22general=True)
                else:
                    voters = voters.filter(v22general=False)
        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town != '':
                if v23town == 'True':
                    voters = voters.filter(v23town=True)
                else:
                    voters = voters.filter(v23town=False)
        
        return voters

class VoterDetailView(DetailView):
    '''View to voter detail for one voter.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        # start with superclass context
        context = super().get_context_data(**kwargs)
        return context
    

class GraphListView(ListView):
    '''View to display voter records'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'


    
    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''

        # start with superclass context
        context = super().get_context_data(**kwargs)
        voter_context = context['voters']

        # create a graph illustrating the distribution of Voters by their year of birth.
        birth_years = [v.dob.year for v in voter_context]

        years = [i for i in range(1900, 2024)]
        number_of_ppl_born = [birth_years.count(i) for i in years]
        hist = go.Bar(x=years, y=number_of_ppl_born)
        title_text_hist = "Distribution of Voters by Year of Birth"
        # obtain the graph as an HTML div"
        graph_div_splits = plotly.offline.plot({"data": [hist], 
                                         "layout_title_text": title_text_hist,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['graph_div_splits'] = graph_div_splits


        # A pie chart illustrating the distribution of Voters by their party affiliation
        party_affiliations = [v.party_affiliation for v in voter_context]
        affiliations = list(set(party_affiliations))
        affiliation_counts = [party_affiliations.count(i) for i in affiliations]

        pie_labels = go.Pie(labels=affiliations, values=affiliation_counts)

        affiliation_pie = plotly.offline.plot({"data": [pie_labels], 
                                         "layout_title_text": "Voter distribution by Party",
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['affiliation_pie'] = affiliation_pie


        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        number_showed_up = [
            sum(v.v20state for v in voter_context),
            sum(v.v21town for v in voter_context),
            sum(v.v21primary for v in voter_context),
            sum(v.v22general for v in voter_context),
            sum(v.v23town for v in voter_context),
        ]
        attendance_bar = go.Bar(x=elections, y=number_showed_up)
        title_text_attendance = "Voter Attendance by Election"

        graph_attendance = plotly.offline.plot({"data": [attendance_bar], 
                                         "layout_title_text": title_text_attendance,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_attendance'] = graph_attendance
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['min_years'] = [i for i in range(1900, 2024)]
        context['max_years'] = [i for i in range(1900, 2024)]

        return context
    
    def get_queryset(self):
        
        # start with entire queryset
        voters = super().get_queryset()

        print('GET:', self.request.GET)

        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation != '':
                voters = voters.filter(party_affiliation=party_affiliation)
        if 'min_years' in self.request.GET:
            min_year = self.request.GET['min_years']
            if min_year != '':
                voters = voters.filter(dob__year__gte=min_year)
        if 'max_years' in self.request.GET:
            max_year = self.request.GET['max_years']
            if max_year != '':
                voters = voters.filter(dob__year__lte=max_year)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score != '':
                voters = voters.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state != '':
                if v20state == 'True':
                    voters = voters.filter(v20state=True)
                else:
                    voters = voters.filter(v20state=False)
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town != '':
                if v21town == 'True':
                    voters = voters.filter(v21town=True)
                else:
                    voters = voters.filter(v21town=False)
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary != '':
                if v21primary == 'True':
                    voters = voters.filter(v21primary=True)
                else:
                    voters = voters.filter(v21primary=False)
        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general != '':
                if v22general == 'True':
                    voters = voters.filter(v22general=True)
                else:
                    voters = voters.filter(v22general=False)
        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town != '':
                if v23town == 'True':
                    voters = voters.filter(v23town=True)
                else:
                    voters = voters.filter(v23town=False)
        
        return voters


        # # create graph of first half/second half as pie chart:
        # x = ['first half', 'second half']
        # first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        # second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        # y = [first_half_seconds , second_half_seconds]
        
        # # generate the Pie chart
        # fig = go.Pie(labels=x, values=y) 
        # title_text = f"Half Marathon Splits"
        # # obtain the graph as an HTML div"
        # graph_div_splits = plotly.offline.plot({"data": [fig], 
        #                                  "layout_title_text": title_text,
        #                                  }, 
        #                                  auto_open=False, 
        #                                  output_type="div")
        # # send div as template context variable
        # context['graph_div_splits'] = graph_div_splits


		# # create graph of runners who passed/passed by
        # x= [f'Runners Passed by {r.first_name}', f'Runners who Passed {r.first_name}']
        # y = [r.get_runners_passed(), r.get_runners_passed_by()]
        
        # fig = go.Bar(x=x, y=y)
        # title_text = f"Runners Passed/Passed By"
        # graph_div_passed = plotly.offline.plot({"data": [fig], 
        #                                  "layout_title_text": title_text,
        #                                  }, auto_open=False, output_type="div",
                                         
        #                                  ) 
        # context['graph_div_passed'] = graph_div_passed

        # return context
