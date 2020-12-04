"""view functionlaties.."""
from django.shortcuts import render, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post  # Comment
from .forms import EmailPostForm, CommentForm
# Create your views here.


"""
function based view
def post_list(request):
    # Post list ..
    posts = Post.published.all()
    paginator = Paginator(posts, per_page=3)  # no of post in per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # page not return an integer value then it return first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page out of range delivar it return last page
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})

"""
# class based view


class PostListView(ListView):
    """docstring for ClassName.."""

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    """Return post object detail..."""
    post = get_object_or_404(Post, slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    # Comment box
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a comment object but did not save in the data base
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            # save the comment into the data base
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form
                                                     })


def post_share(request, post_id):
    """Send the email.."""
    sent = False
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():

            # form field pass validation..
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({})    recommends  you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at  {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comment'])
            # email = EmailMessage(subject, message, to=[cd['to']])
            print(send_mail(subject, message, 'durgeshxvf@gmail.com', [cd['to'], ], fail_silently=False,))
            print(cd['to'])
            # email.send()
            print(cd['to'])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

