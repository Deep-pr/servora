from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification
from providers.models import ProviderProfile
from .forms import MessageForm
from .models import Conversation


@login_required
def conversation_list(request):
    conversations = request.user.conversations.prefetch_related('participants', 'messages')
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_start(request, provider_id):
    provider = get_object_or_404(ProviderProfile, pk=provider_id, verification_status=ProviderProfile.APPROVED)
    if request.user == provider.user:
        raise PermissionDenied
    conversation = _conversation_between(request.user, provider.user)
    return redirect('messaging:detail', pk=conversation.pk)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation.objects.prefetch_related('participants', 'messages__sender'), pk=pk)
    if request.user not in conversation.participants.all():
        raise PermissionDenied
    form = MessageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.conversation = conversation
        message.sender = request.user
        message.save()
        conversation.save()
        for participant in conversation.participants.exclude(pk=request.user.pk):
            Notification.objects.create(
                user=participant,
                title='New message',
                message=f'{request.user.username} sent you a message.',
                link=f'/messages/{conversation.pk}/',
            )
        messages.success(request, 'Message sent.')
        return redirect('messaging:detail', pk=conversation.pk)
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'form': form})


def _conversation_between(user, provider_user):
    for conversation in user.conversations.filter(participants=provider_user):
        if conversation.participants.count() == 2:
            return conversation
    conversation = Conversation.objects.create()
    conversation.participants.set([user, provider_user])
    return conversation

# Create your views here.
