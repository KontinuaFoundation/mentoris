import json, os, random
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from mentapp.models import (
    User,
    Email,
    Volume,
    Chapter,
    Chapter_Loc,
    Blob,
    Question_Loc,
    Quiz,
    Quiz_Question,
    Question,
    Verification,
    Question_Attachment,
    Support,
    Support_Loc,
    Support_Attachment
)
from mentoris.forms import UserForm, LatexForm, QuizForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.files.base import ContentFile


def latex(request):
    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )

    volume_id = 1
    chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()

    chapter_locs = Chapter_Loc.objects.filter(
        chapter__chapter_id__in=chapters
    ).distinct()

    chapter = chapter_locs[0]

    if request.method == "POST":
        form = LatexForm(request.POST)
        question = request.POST.get("latex_question")
        answer = request.POST.get("latex_answer")
        grading = request.POST.get("latex_grading")
        volume_id = request.POST.get("volume")
        volume_id = int(volume_id)
        chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()
        
    

        chapter_locs = Chapter_Loc.objects.filter(
            chapter__chapter_id__in=chapters
        ).distinct()

        hidden_question = request.POST.get("question_hidden")
        hidden_answer = request.POST.get("answer_hidden")
        hidden_grading = request.POST.get("grading_hidden")

        if "submit-question" in request.POST:
            question_object = Question()
            question_loc = Question_Loc()
            

            # TODO: question_object.creator = CURRENT USER

            chapter = request.POST.get("chapter")
            chapter_string = chapter.split("_")
            chapter_title = chapter_string[0]
            chapter_loc = get_object_or_404(Chapter_Loc, title=chapter_title)
            question_object.chapter = chapter_loc.chapter

            question_object.conceptual_difficulty = request.POST.get("difficulty")
            question_object.time_required_mins = request.POST.get("time_required")
            question_object.point_value = request.POST.get("points")
            question_object.pages_required = request.POST.get("pages_required")
            question_object.save()

            question_loc.question = question_object
            question_loc.question_latex = question
            question_loc.answer_latex = answer
            question_loc.rubric_latex = grading
            # TODO: question_loc.creator = CURRENT USER
            question_loc.save()

            question_attachments = request.FILES.getlist('attachments')
            
            for attachment in question_attachments:

                blob = Blob(
                    file = attachment,
                    content_type = attachment.content_type,
                    filename = attachment.name
                )
                blob.save()

                question_attachment_instance = Question_Attachment(
                    question=question_loc,
                    lang_code = question_loc.lang_code,
                    dialect_code = question_loc.dialect_code,
                    filename=blob.filename,
                    blob_key = blob
                )
                question_attachment_instance.save()


            return main(request)

        if "question-button" in request.POST:
            answer = hidden_answer
            grading = hidden_grading
        if "answer-button" in request.POST:
            question = hidden_question
            grading = hidden_grading
        if "grading-button" in request.POST:
            question = hidden_question
            answer = hidden_answer
        if "volume-button" not in request.POST:
            chapter = request.POST.get("chapter")
            chapter_string = chapter.split("_")
            chapter_title = chapter_string[0]
            chapter = get_object_or_404(Chapter_Loc, title=chapter_title)
        else:
            chapter = chapters[0]

        return render(
            request,
            "mentapp/latex_question.html",
            {
                "form": form,
                "question": question,
                "answer": answer,
                "grading": grading,
                "volume_id": volume_id,
                "volumes": volumes,
                "chapters": chapter_locs,
                "chapter": chapter,
            },
        )
    else:
        print(chapters)
        return render(
            request,
            "mentapp/latex_question.html",
            {
                "form": LatexForm(),
                "volumes": volumes,
                "volume_id": volume_id,
                "chapters": chapter_locs,
                "chapter": chapter,
            },
        )


def sign_up(request):
    if request.method == "POST":
        # Add to User table
        form = UserForm(request.POST)

        if form.is_valid():
            email_exists = False
            other_email_exists = False

            if Email.objects.filter(
                email_address=request.POST.get("email_address")
            ).exists():
                email_exists = True

            other_emails = request.POST.get("other_emails")
            if other_emails is not None and other_emails != "":
                email_list = other_emails.split(",")
                for other_email in email_list:
                    if Email.objects.filter(email_address=other_email.strip()).exists():
                        other_email_exists = True
            if email_exists or other_email_exists:
                if email_exists:
                    form.add_error(None, "Primary")
                if other_email_exists:
                    form.add_error(None, "Other")
                return render(
                    request,
                    "mentapp/sign_up.html",
                    {
                        "form": form,
                        "email": request.POST.get("email_address"),
                        "other_emails": request.POST.get("other_emails"),
                    },
                )
            user = form.save()
            # Add to Email table
            email = request.POST.get("email_address")
            emailObject = Email()
            emailObject.email_address = email
            emailObject.user = user
            emailObject.is_primary = True
            emailObject.save()

            other_emails = request.POST.get("other_emails")
            if other_emails is not None and other_emails != "":
                email_list = other_emails.split(",")
                for other_email in email_list:
                    emailObject = Email()
                    emailObject.email_address = other_email.strip()
                    emailObject.user = user
                    emailObject.is_primary = False
                    emailObject.save()

            return redirect(f"../profile/{user.user_id}")

        return render(
            request,
            "mentapp/sign_up.html",
            {
                "form": form,
            },
        )
    else:
        return render(request, "mentapp/sign_up.html")


def profile(request):
    template = loader.get_template("mentapp/profile.html")
    return HttpResponse(template.render())


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            emailObject = Email.objects.get(email_address=email)
            user = emailObject.user
            if not user.check_password(password):
                user = None
        except Email.DoesNotExist:
            user = None

        if user is not None:
            # TODO: log user in
            return redirect(f"../profile/{user.user_id}")
        else:
            messages.error(
                request,
                "Could not find account, please double-check account credentials",
            )
            return render(
                request,
                "mentapp/login.html",
                {"email": email, "password": password},
            )
    else:
        return render(request, "mentapp/login.html")


def main(request, volume_id=1):
    template = loader.get_template("mentapp/main.html")

    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )

    if volume_id:
        chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()
    else:
        chapters = []

    chapter_locs = Chapter_Loc.objects.filter(
        chapter__chapter_id__in=chapters
    ).distinct()

    context = {
        "volumes": volumes,
        "chapters": chapters,
        "volume_id": volume_id,
        "chapter_locs": chapter_locs,
    }

    return HttpResponse(template.render(context, request))


def chapter(request, volume_id, chapter_id):
    volume_id = get_object_or_404(Volume, volume_id=volume_id)
    chapter_id = get_object_or_404(Chapter, chapter_id=chapter_id)
    try:
        chapter_loc = Chapter_Loc.objects.get(chapter=chapter_id)
        title = chapter_loc.title
    except Chapter_Loc.DoesNotExist:
        title = None

    return render(
        request,
        "mentapp/chapter.html",
        {"volume": volume_id, "chapter": chapter_id, "title": title},
    )


def promotion(request):
    if request.method == "POST":
        email_object = Email.objects.get(
            email_address=request.POST.get("email"), is_primary=True
        )
        user = get_object_or_404(User, user_id=email_object.user_id)

        if request.POST.get("command") == "promote":
            if user.is_active == True:
                if user.is_quizmaker == True:
                    user.is_admin = True
                elif user.is_verified == True:
                    user.is_quizmaker = True
                elif user.is_verified == False:
                    user.is_verified = True

        user.promotion_requested = False
        user.save()
        return JsonResponse({"success": True})
    else:
        users = grab_users(True)
        return render(
            request,
            "mentapp/promotion.html",
            {
                "newbies": users["newbies"],
                "mentors": users["mentors"],
                "quiz_makers": users["quiz_makers"],
            },
        )


def user_directory(request):
    if request.method == "POST":
        email_object = Email.objects.get(
            email_address=request.POST.get("email"), is_primary=True
        )
        user = get_object_or_404(User, user_id=email_object.user_id)
        status = "Newbie"
        color = "btn btn-outline-secondary"

        if request.POST.get("command") == "demote":
            if user.is_active == True:
                if user.is_admin == True:
                    user.is_admin = False
                    status = "Quiz Maker"
                    color = "btn btn-outline-warning"
                elif user.is_quizmaker == True:
                    user.is_quizmaker = False
                    status = "Mentor"
                    color = "btn btn-outline-info"
                elif user.is_verified == True:
                    user.is_verified = False
        else:
            user.is_active = False

        user.save()
        return JsonResponse({"success": True, "status": status, "color": color})
    else:
        users = grab_users(False)
        return render(
            request,
            "mentapp/user_directory.html",
            {
                "newbies": users["newbies"],
                "mentors": users["mentors"],
                "quiz_makers": users["quiz_makers"],
                "admins": users["admins"],
            },
        )


def grab_users(get_promotion):
    try:
        newbie_ids = (
            User.objects.filter(
                is_verified=False,
                is_quizmaker=False,
                is_admin=False,
                is_active=True,
                promotion_requested=get_promotion,
            )
            .values_list("user_id", flat=True)
            .distinct()
        )
        newbies = grab_verification_info(newbie_ids)
    except:
        newbies = []

    try:
        mentor_ids = (
            User.objects.filter(
                is_verified=True,
                is_quizmaker=False,
                is_admin=False,
                is_active=True,
                promotion_requested=get_promotion,
            )
            .values_list("user_id", flat=True)
            .distinct()
        )
        mentors = grab_verification_info(mentor_ids)
    except:
        mentors = []

    try:
        quiz_maker_ids = (
            User.objects.filter(
                is_verified=True,
                is_quizmaker=True,
                is_admin=False,
                is_active=True,
                promotion_requested=get_promotion,
            )
            .values_list("user_id", flat=True)
            .distinct()
        )
        quiz_makers = grab_verification_info(quiz_maker_ids)
    except:
        quiz_makers = []

    try:
        admin_ids = (
            User.objects.filter(
                is_verified=True,
                is_quizmaker=True,
                is_admin=True,
                is_active=True,
            )
            .values_list("user_id", flat=True)
            .distinct()
        )
        admins = grab_verification_info(admin_ids)
    except:
        admins = []

    return {
        "newbies": newbies,
        "mentors": mentors,
        "quiz_makers": quiz_makers,
        "admins": admins,
    }


def grab_verification_info(user_ids):
    verification_info = []
    for user_id in user_ids:
        email = Email.objects.get(user_id=user_id, is_primary=True)
        try:
            verifications = Verification.objects.exclude(date_granted__isnull=True).get(
                verified=user_id
            )
            verifier_id = verifications.verifier.user_id
            verifier = get_object_or_404(User, user_id=verifier_id)
            verifier_email = Email.objects.get(user_id=verifier_id, is_primary=True)
        except Verification.DoesNotExist:
            verifier = None

        verification_info.append(
            (
                user_id,
                email.email_address,
                verifier.full_name,
                verifier_email.email_address,
            )
        )
    return verification_info


def user_info(request, user_id):
    user_profile = get_object_or_404(User, user_id=user_id)
    try:
        email = Email.objects.get(user_id=user_id, is_primary=True)
        other_emails = Email.objects.filter(user_id=user_id, is_primary=False)
        other_emailss = [obj.email_address for obj in other_emails]
        other_email = ", ".join(other_emailss)
    except Email.DoesNotExist:
        email = None
    return render(
        request,
        "mentapp/profile.html",
        {"user_profile": user_profile, "email": email, "other_email": other_email},
    )


def edit_quiz(request, quiz_id):
    quiz_instance = get_object_or_404(Quiz, quiz_id=quiz_id)
    quiz_questions = (
        Quiz_Question.objects.all()
        .filter(quiz=quiz_instance.quiz_id)
        .order_by("ordering")
    )
    questions_Loc = list()

    for quiz_question in quiz_questions:
        questions_Loc_local = Question_Loc.objects.all().filter(
            question=quiz_question.question
        )

        for question_Loc in questions_Loc_local:
            # TODO add an if statement for language, quizzes currently have no language
            questions_Loc.append((question_Loc, quiz_question))

    initial_values = {
        "conceptual_difficulty": quiz_instance.conceptual_difficulty,
        "time_required_mins": quiz_instance.time_required_mins,
        "computer_allowed": quiz_instance.computer_allowed,
        "internet_allowed": quiz_instance.internet_allowed,
        "book_allowed": quiz_instance.book_allowed,
        "calculator_allowed": quiz_instance.calculator_allowed,
        "volume": quiz_instance.volume,
        "chapter": quiz_instance.chapter,
    }

    if request.method == "POST":
        form = QuizForm(request.POST, initial_values)

        if request.POST.get("command") == "save":
            orderings_str = json.loads(request.POST.get("orderings"))
            ids_str = json.loads(request.POST.get("ids"))

            orderings = list()
            ids = list()
            for id_str, ordering_str in zip(ids_str, orderings_str):
                ids.append(int(id_str))
                orderings.append(int(ordering_str))

            for question in quiz_questions:
                if question.question not in ids:
                    question.delete()

            for id, ordering in zip(ids, orderings):
                for quiz_question in quiz_questions:
                    if quiz_question.question.question_id == id:
                        quiz_question.ordering = ordering
                        quiz_question.save()
            return JsonResponse({"success": True})

        # TODO modify behavior once add quiz question page is added
        elif request.POST.get("command") == "add_question":
            question_latex = list()
            question_latex.append("f(x) = ax^2 + bx + c")
            question_latex.append("\int_{0}^{\pi}x^2 \,dx")
            question_latex.append("\\boxed{\log(x) + \sqrt{1+x^2}}")
            question_latex.append("\\frac{-b\pm\sqrt{b^2-4ac}}{2a}")
            question_latex.append(
                "x = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \cfrac{1}{a_3 + a_4}}} "
            )
            question_latex.append(
                "\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \\right) \left( \sum_{k=1}^n b_k^2 \right) "
            )
            question_latex.append("2\\times2")
            question_latex.append("2_2 +2^2")
            question_latex.append("\oint_a^bx^2")

            question = Question.objects.create()
            quiz_question = Quiz_Question.objects.create(
                quiz=quiz_instance, question=question, ordering=quiz_questions.count()
            )
            quiz_question_loc = Question_Loc.objects.create(
                question=question,
                lang_code="ENG",
                dialect_code="US",
                question_latex=question_latex[random.randint(0, 8)],
                answer_latex=question_latex[random.randint(0, 8)],
                rubric_latex=question_latex[random.randint(0, 8)],
            )
            return JsonResponse({"success": True})

        if form.is_valid():
            quiz_instance.conceptual_difficulty = form.cleaned_data[
                "conceptual_difficulty"
            ]
            quiz_instance.time_required_mins = form.cleaned_data["time_required_mins"]
            quiz_instance.computer_allowed = form.cleaned_data["computer_allowed"]
            quiz_instance.book_allowed = form.cleaned_data["book_allowed"]
            quiz_instance.calculator_allowed = form.cleaned_data["calculator_allowed"]
            quiz_instance.internet_allowed = form.cleaned_data["internet_allowed"]
            quiz_instance.volume = form.cleaned_data["volume"]
            quiz_instance.chapter = form.cleaned_data["chapter"]
            quiz_instance.save()

            return render(
                request,
                "mentapp/edit_quiz.html",
                {
                    "form": form,
                    "quiz_instance": quiz_instance,
                    "questions_Loc_and_quiz": questions_Loc,
                },
            )

    form = QuizForm(initial_values)
    return render(
        request,
        "mentapp/edit_quiz.html",
        {
            "form": form,
            "quiz_instance": quiz_instance,
            "questions_Loc_and_quiz": questions_Loc,
        },
    )


def edit_quiz_add_question(request, quiz_id):
    questions_Locs = Question_Loc.objects.all()
    chapters = Chapter.objects.all()
    volumes = Volume.objects.all()
    creators = User.objects.all()

    if request.method == "POST":
        quiz_instance = get_object_or_404(Quiz, quiz_id=quiz_id)
        if request.POST.get("command") == "save_changes":
            quiz_questions = (
                Quiz_Question.objects.all().filter(quiz=quiz_id).order_by("ordering")
            )
            questions_to_add_id_str = json.loads(
                request.POST.get("questions_to_add_ids")
            )

            for question_id in questions_to_add_id_str:
                if quiz_questions.filter(question_id=question_id).count() == 0:
                    question_instance = get_object_or_404(
                        Question, question_id=question_id
                    )
                    Quiz_Question.objects.create(
                        quiz=quiz_instance,
                        question=question_instance,
                        ordering=quiz_questions.count(),
                    )

            return JsonResponse({"success": True})
    elif request.method == "GET" and request.GET.get("command") == "filter":
        chapter_filter = request.GET.get("chapter")
        creator_filter = request.GET.get("creator")
        volume_filter = request.GET.get("volume")
        point_filter = request.GET.get("point")
        time_filter = request.GET.get("time")
        difficulty_filter = request.GET.get("difficulty")
        question_instances = Question.objects.all()

        if volume_filter:
            question_instances = question_instances.filter(
                chapter__volume__volume_id=volume_filter
            )

        if chapter_filter:
            question_instances = question_instances.filter(chapter=chapter_filter)

        if creator_filter:
            question_instances = question_instances.filter(creator=creator_filter)

        if point_filter:
            question_instances = question_instances.filter(point_value=point_filter)

        if difficulty_filter:
            question_instances = question_instances.filter(
                conceptual_difficulty=difficulty_filter
            )

        if time_filter:
            question_instances = question_instances.filter(
                time_required_mins=time_filter
            )

        questions_list = list()
        for question in question_instances:
            question_Loc = (
                Question_Loc.objects.all()
                .filter(
                    lang_code="ENG", dialect_code="US", question=question.question_id
                )
                .first()
            )
            question_values = dict()
            question_values["question_id"] = question.question_id

            if question.chapter is not None:
                question_values["chapter"] = question.chapter.chapter_id
                question_values["volume"] = question.chapter.volume.volume_id
            else:
                question_values["chapter"] = ""
                question_values["volume"] = ""

            if question.creator is not None:
                question_values["creator"] = question_Loc.creator.full_name
            else:
                question_values["creator"] = ""

            question_values["conceptual_difficulty"] = question.conceptual_difficulty
            question_values["time_required_mins"] = question.time_required_mins
            question_values["point_value"] = question.point_value
            question_values["question_latex"] = question_Loc.question_latex
            questions_list.append(question_values)
        return JsonResponse(questions_list, safe=False)

    return render(
        request,
        "mentapp/edit_quiz_add_question.html/",
        {
            "quiz_id": quiz_id,
            "questions_Locs": questions_Locs,
            "chapters": chapters,
            "volumes": volumes,
            "creators": creators,
        },
    )

def edit_quiz_add_support(request, quiz_id):

    return render(request,
        "mentapp/edit_quiz_add_support.html/",
        {
            "quiz_id": quiz_id
        }
    )


def header(request, page):
    return render(
        request,
        "mentapp/header.html",
    )


def footer(request, page):
    return render(
        request,
        "mentapp/footer.html",
    )


def user_edit(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    # print("user items", user)
    # print("request items", request.POST)
    for key, value in request.POST.items():
        # print("KEY", key, "VALUE", value)
        if key == "primary_email":
            Email.objects.filter(user_id=user_id, is_primary=True).update(
                email_address=value
            )
        if key == "other_emails":
            Email.objects.filter(user_id=user_id, is_primary=False).delete()
            insEmails = value.split(",")
            for em in insEmails:
                emailObject = Email()
                emailObject.email_address = em
                emailObject.user_id = user_id
                emailObject.save()
        # Check if the user object has this field and the value is not empty
        if hasattr(user, key) and value.strip():
            # print("USERKEY", key, "USERVAL", value)
            setattr(user, key, value)
    user.save()
    return redirect(f"/profile/{user.user_id}")


def request_translation(request, user_id):
    # need to verify email to ses when they sign up in order for this to work
    email = get_object_or_404(Email, user_id=user_id, is_primary=True)
    primary_language = get_object_or_404(User.primary_language, user_id=user_id)
    send_mail(
        "Kontinua Quiz Questions Translations Request",
        "Hi there! We have noticed you are fluent in "
        + primary_language
        + ". This week these questions were added in "
        + primary_language
        + ". I can do a preliminary translation to "
        + primary_language
        + " using Google Translate. Would you look at and correct those preliminary translations?  Click here.",
        "notifications@kontinua.org",
        [email],
    )


def download_pdf(request, blob_key):
    blob_instance = get_object_or_404(Blob, blob_key=blob_key)

    response = HttpResponse(blob_instance.file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{blob_instance.filename}"'
    return response


def upload_pdf(request, pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()

        # Use Django's ContentFile to create a file-like object
        content_file = ContentFile(pdf_content, name=os.path.basename(pdf_path))

        blob_instance = Blob(
            file=content_file,
            content_type="application/pdf",
            filename=os.path.basename(pdf_path),
        )
        blob_instance.save()

        return JsonResponse(
            {"status": "success", "message": "File uploaded successfully"}
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    

def create_support(request):
    
    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )

    volume_id = 1

    if request.method == "POST":
        form = LatexForm(request.POST, request.FILES)
        support_content = request.POST.get("latex_support")
        support_title = request.POST.get("title")
        volume_id = int(request.POST.get("volume"))
        volume = get_object_or_404(Volume, volume_id=volume_id)
        support_attachments = request.FILES.getlist('attachments')
        print(support_attachments)

        

        if "submit-support" in request.POST:
            
            support = Support(volume_id = volume)
            support.save()
            
            support_loc = Support_Loc(
            support=support,
            title_latex=support_title,
            content_latex=support_content,
            creator_id="e79c167f-6900-4525-9aa6-bd7263c1fbb3",
            approver_id="e79c167f-6900-4525-9aa6-bd7263c1fbb3"
            )

            support_loc.save()


            for attachment in support_attachments:
                blob = Blob(
                    file = attachment,
                    content_type = attachment.content_type,
                    filename = attachment.name
                )
                blob.save()

                support_attachment_instance = Support_Attachment(
                    support=support,
                    lang_code = support_loc.lang_code,
                    dialect_code = support_loc.dialect_code,
                    filename=blob.filename,
                    blob_key = blob
                )
                support_attachment_instance.save()

            return redirect('main')
            
        return render(
            request, 
            "mentapp/create_support.html",
            {
                "form": form,
                "volumes": volumes,
                "volume_id": volume_id,
                "support_content": support_content,
                }
            )
    else:
        return render(
            request, 
            "mentapp/create_support.html",
            {
                "form": LatexForm(),
                "volumes": volumes
                }
            )