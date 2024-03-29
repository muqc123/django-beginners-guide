from django.shortcuts import \
	render, HttpResponse, redirect, \
	get_object_or_404, Http404
from django.contrib.auth.models import User

# Create your views here.

from .models import Board, Topic, Post
from .forms import NewTopicForm


def home(request):
	boards = Board.objects.all()
	return render(request, 'home.html', {'boards': boards})


def base(request):
	return render(request, 'base.html')


def board_topics(request, pk):
	# board = Board.objects.get(pk=pk)

	try:
		board = Board.objects.get(pk=pk)
	except Board.DoesNotExist:
		raise Http404

	# board = get_object_or_404(Board, pk=pk)
	return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)
	user = User.objects.first()

	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = user
			topic.save()
			post = Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=user,
			)
			return redirect('board_topics', pk=pk)
	else:
		form = NewTopicForm()

	return render(request, 'new_topic.html', {'board': board, 'form': form})
