from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from .forms import CreateJobForm, CommentForm, EmployerForm
from .models import Comment, JobVacancy


# Create your views here.
@login_required(login_url='login')
def like_view(request, pk):
    if request.method == 'POST':
        job = get_object_or_404(JobVacancy, id=pk)
        if job.likes.filter(id=request.user.id).exists():
            job.likes.remove(request.user)
        else:
            job.likes.add(request.user)
        return HttpResponseRedirect(reverse('job_detail', args=[str(pk)]))

# class LikeUnlikeView(View):
#
#     def post(self, request, pk, **kwargs):
#         job = get_object_or_404(JobVacancy, pk)
#         job.


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.user.is_authenticated:
            return redirect('home')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User with this username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect!')

    context = {'page': page}
    return render(request, 'registration/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def register_user(request):
    form = EmployerForm()

    if request.method == 'POST':
        form = EmployerForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')

    context = {'form': form}
    return render(request, 'registration/login.html', context)


def home(request):
    jobs = JobVacancy.objects.all()
    search = request.GET.get('q') if request.GET.get('q') is not None else ""
    if request.user.is_authenticated:
        jobs = JobVacancy.objects.filter(
            Q(position__icontains=search) |
            Q(company_name__icontains=search) |
            Q(address__icontains=search) |
            Q(location__name__icontains=search) |
            Q(employee_type__name__icontains=search) |
            Q(experience_level__name__icontains=search)
        )
    else:
        jobs = JobVacancy.active_jobs.filter(
            Q(position__icontains=search) |
            Q(company_name__icontains=search) |
            Q(address__icontains=search) |
            Q(location__name__icontains=search) |
            Q(employee_type__name__icontains=search) |
            Q(experience_level__name__icontains=search)
        )
    job_count = jobs.count()
    context = {
        'jobs': jobs[:4],
        'job_count': job_count,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def create_job(request):
    form = CreateJobForm()
    if request.method == 'POST':
        form = CreateJobForm(request.POST, request.FILES)
        if form.is_valid():
            employer = request.user
            position = form.cleaned_data['position']
            address = form.cleaned_data['address']
            company_name = form.cleaned_data['company_name']
            company_logo = form.cleaned_data['company_logo']
            location = form.cleaned_data['location']
            employee_type = form.cleaned_data['employee_type']
            experience_level = form.cleaned_data['experience_level']
            description = form.cleaned_data['description']
            expiry_date = form.cleaned_data['expiry_date']

            job = JobVacancy.objects.create(employer=employer,
                                            position=position,
                                            address=address,
                                            company_name=company_name,
                                            company_logo=company_logo,
                                            location=location,
                                            employee_type=employee_type,
                                            experience_level=experience_level,
                                            description=description,
                                            expiry_date=expiry_date,
                                            )
            return HttpResponseRedirect(reverse('home'))
    context = {
        'form': form,
    }
    return render(request, 'add_job.html', context)


class JobListView(ListView):
    model = JobVacancy
    paginate_by = 5
    template_name = 'job_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return JobVacancy.objects.all()
        else:
            return JobVacancy.active_jobs.all()


def job_detail(request, pk):
    job = JobVacancy.objects.get(id=pk)
    if request.user.is_authenticated and job.employer == request.user:
        comments = job.comment_set.all()
    else:
        comments = job.comment_set.filter(is_hidden=False)
    if job.likes.filter(id=request.user.id).exists():
        like = True
    else:
        like = False
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.job_vacancy = job
            comment_form.save()
            return redirect('job_detail', job.pk)
    context = {
        'job': job,
        'comments': comments,
        'form': form,
        'like': like,
    }
    return render(request, 'job_detail.html', context)


# def add_comment(request, pk):
#     job = JobVacancy.objects.get(id=pk)
#     form = CommentForm()
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         form.job_vacancy = job
#         if form.is_valid():
#             form.job_vacancy = request.POST.get('job_vacancy')
#             form.save()
#             return redirect('job_detail', job.id)
#     context = {
#         "form": form
#     }
#     return render(request, 'add_comment.html', context)


# class AddCommentView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'add_comment.html'
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         form.instance.post_id = self.kwargs['pk']
#         return super().form_valid(form)


@login_required(login_url='login')
def hide_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    job = JobVacancy.objects.get(comment=comment)
    comment.is_hidden = not comment.is_hidden
    comment.save()
    return redirect(reverse_lazy('job_detail', kwargs={'pk': job.id}))
