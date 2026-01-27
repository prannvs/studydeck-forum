from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, Reply, Category,Tag, Report
from django.contrib.postgres.search import TrigramSimilarity
from .forms import ThreadForm, ReportForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages


def home(request):
    category_id = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    sort_by = request.GET.get('sort', 'newest')

    threads = Thread.objects.all()

    if category_id:
        threads = threads.filter(category_id=category_id)

    if tag_slug:
        threads = threads.filter(tags__slug=tag_slug)

    if sort_by == 'oldest':
        threads = threads.order_by('created_at')
    else:
        threads = threads.order_by('-created_at')

    paginator = Paginator(threads, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    from .models import Tag
    all_tags = Tag.objects.all()

    return render(request, 'forum/home.html', {
        'page_obj': page_obj, 
        'categories': categories,
        'tags': all_tags,
        'current_category': int(category_id) if category_id else None,
        'current_tag': tag_slug
    })

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    threads = Thread.objects.filter(author=profile_user).order_by('-created_at')
    replies = Reply.objects.filter(author=profile_user).order_by('-created_at')
    
    return render(request, 'forum/profile.html', {
        'profile_user': profile_user, 
        'threads': threads, 
        'replies': replies
    })

@login_required
def thread_detail(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    replies = thread.replies.filter(is_deleted=False)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')
            
        if thread.is_locked and not request.user.is_staff:
            return redirect('thread_detail', slug=thread.slug)

        content = request.POST.get('content')
        if content:
            Reply.objects.create(thread=thread, author=request.user, content=content)
            return redirect('thread_detail', slug=thread.slug)

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'replies': replies})

@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        results = Thread.objects.annotate(
            similarity=TrigramSimilarity('title', query)
        ).filter(similarity__gt=0.3).order_by('-similarity')
    else:
        results = Thread.objects.none()
    return render(request, 'forum/home.html', {'threads': results})
    
@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_detail', slug=thread.slug)
    else:
        form = ThreadForm()
    
    return render(request, 'forum/create_thread.html', {'form': form})

@staff_member_required
def lock_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    thread.is_locked = not thread.is_locked
    thread.save()
    return redirect('thread_detail', slug=thread.slug)

@login_required
def delete_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    if request.user == thread.author or request.user.is_staff:
        thread.delete()
        return redirect('home')
    return redirect('thread_detail', slug=slug)

@login_required
def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user in reply.likes.all():
        reply.likes.remove(request.user)
    else:
        reply.likes.add(request.user)
    return redirect('thread_detail', slug=reply.thread.slug)

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.author or request.user.is_staff:
        reply.is_deleted = True
        reply.save()
    return redirect('thread_detail', slug=reply.thread.slug)

@login_required
def like_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    
    if request.user in thread.likes.all():
        thread.likes.remove(request.user)
    else:
        thread.likes.add(request.user)
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def report_thread(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.thread = thread
            report.save()
            return redirect('thread_detail', slug=thread.slug)
    else:
        form = ReportForm()
    
    return render(request, 'forum/report_thread.html', {'form': form, 'thread': thread})

@staff_member_required
def moderator_dashboard(request):
    pending_reports = Report.objects.filter(status='PENDING').order_by('-created_at')
    if request.method == 'POST' and 'promote_username' in request.POST:
        username = request.POST.get('promote_username')
        try:
            user_to_promote = User.objects.get(username=username)
            user_to_promote.is_staff = True
            user_to_promote.save()
            messages.success(request, f"Successfully promoted {username} to Moderator.")
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' not found.")
            
    return render(request, 'forum/moderator_dashboard.html', {
        'reports': pending_reports
    })

@staff_member_required
def resolve_report(request, slug):
    report = get_object_or_404(Report, slug=slug)
    report.status = 'RESOLVED'
    report.save()
    messages.success(request, "Report marked as resolved.")
    return redirect('moderator_dashboard')