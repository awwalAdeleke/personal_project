from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from .forms import CreateJobForm, CommentForm, EmployerForm
from .models import Comment, JobVacancy


# Create your views here.
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
    search = request.GET.get('q') if request.GET.get('q') is not None else ""
    jobs = JobVacancy.objects.filter(
        Q(position__icontains=search) |
        Q(company_name__icontains=search) |
        Q(address__icontains=search) |
        Q(location__name__icontains=search) |
        Q(employee_type__name__icontains=search) |
        Q(experience_level__name__icontains=search)
    )
    job_count = jobs.count()
    context = {
        'jobs': jobs,
        'job_count': job_count,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def create_job(request):
    form = CreateJobForm()
    if request.method == 'POST':
        form = CreateJobForm(request.POST, request.FILES)
        # form.employer = request.user
        if form.is_valid():
            job = JobVacancy.objects.create(employer=form.employer,
                                            position=form.position,
                                            address=form.address,
                                            company_name=form.company_name,
                                            company_logo=form.company_logo,
                                            location=form.location,
                                            employee_type=form.employee_type,
                                            experience_level=form.experience_level,
                                            description=form.description,
                                            expiry_date=form.expiry_date,
                                            )
            job.save()
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
        return JobVacancy.active_jobs.all()


def job_detail(request, pk):
    job = JobVacancy.objects.get(id=pk)
    if request.user.is_authenticated():
        comments = job.comment_set.all()
    else:
        comments = job.comment_set.filter(is_hidden=False)
    context = {
        'job': job,
        'comments': comments,
    }
    return render(request, 'job_detail.html', context)


def add_comment(request, pk):
    job = JobVacancy.objects.get(id=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.job_vacancy = job
        if form.is_valid():
            form.save()
            return redirect('job_detail', job.id)
    context = {
        "form": form
    }
    return render(request, 'add_comment.html', context)


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
