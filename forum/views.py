from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, Reply, Category
from django.contrib.postgres.search import TrigramSimilarity


def home(request):
    sort_by = request.GET.get('sort', 'latest')
    if sort_by == 'popular':
        threads = sorted(Thread.objects.all(), key=lambda t: t.total_likes(), reverse=True)
    else:
        threads = Thread.objects.all().order_by('-created_at')
    
    return render(request, 'forum/home.html', {'threads': threads})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = thread.replies.filter(is_deleted=False)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        Reply.objects.create(thread=thread, author=request.user, content=content)
        return redirect('thread_detail', thread_id=thread.id)

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'replies': replies})

def search(request):
    query = request.GET.get('q')
    results = Thread.objects.annotate(
        similarity=TrigramSimilarity('title', query)
    ).filter(similarity__gt=0.3).order_by('-similarity')
    
@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.author or request.user.is_staff:
        reply.is_deleted = True
        reply.save()
    return redirect('thread_detail', thread_id=reply.thread.id)

def home(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'forum/home.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    replies = thread.replies.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')
        content = request.POST.get('content')
        if content:
            Reply.objects.create(thread=thread, author=request.user, content=content)
            return redirect('thread_detail', thread_id=thread.id)

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'replies': replies})