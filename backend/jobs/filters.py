import django_filters
from django.db.models import Q
from .models import Job

class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search keywords')
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')
    state = django_filters.CharFilter(field_name='state', lookup_expr='iexact')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    work_mode = django_filters.CharFilter(field_name='work_mode', lookup_expr='iexact')
    employment_type = django_filters.CharFilter(field_name='employment_type', lookup_expr='iexact')
    verification_status = django_filters.CharFilter(field_name='verification_status', lookup_expr='iexact')
    eligibility_category = django_filters.CharFilter(field_name='eligibility_category', lookup_expr='iexact')
    salary_disclosed = django_filters.BooleanFilter(field_name='salary_disclosed')
    min_salary = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')

    # Strict experience filter controls
    eligibility = django_filters.CharFilter(method='filter_eligibility')

    class Meta:
        model = Job
        fields = [
            'city', 'state', 'location', 'work_mode', 'employment_type',
            'verification_status', 'eligibility_category', 'salary_disclosed'
        ]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) |
            Q(company_name__icontains=value) |
            Q(required_skills__icontains=value) |
            Q(original_description__icontains=value)
        )

    def filter_eligibility(self, queryset, name, value):
        if not value:
            return queryset.filter(eligibility_classification='ELIGIBLE_FRESHER')
        
        val_upper = value.upper()
        if val_upper == 'ALL':
            return queryset
        elif val_upper in ('UNCLEAR', 'ELIGIBILITY_UNCLEAR'):
            return queryset.filter(eligibility_classification='ELIGIBILITY_UNCLEAR')
        elif val_upper in ('INELIGIBLE', 'INELIGIBLE_EXPERIENCED'):
            return queryset.filter(eligibility_classification='INELIGIBLE_EXPERIENCED')
        elif val_upper in ('FRESHER', 'ELIGIBLE', 'ELIGIBLE_FRESHER'):
            return queryset.filter(eligibility_classification='ELIGIBLE_FRESHER')
        return queryset
