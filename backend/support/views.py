from django.shortcuts import render

# Create your views here.


def chat(request, job_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        if not user_message:
            return JsonResponse({'empty': 'Empty message'})

        job = get_object_or_404(Jobs, id=job_id)
        conversation, created = Conversation.objects.get_or_create(job=job)

        Message.objects.create(conversation=conversation, role='user', context=user_message)

        reply = run_support_agent(user_message, conversation_id, job_id)

        return JsonResponse({'reply': reply})