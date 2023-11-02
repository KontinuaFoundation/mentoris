# Generated by Django 5.0.1 on 2024-04-30 16:52

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blob',
            fields=[
                ('blob_key', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('content_type', models.CharField(blank=True, max_length=255, null=True)),
                ('filename', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapter_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('ordering', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('site_id', models.CharField(default='site', max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('support_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('volume_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.CharField(default='email@default.com', max_length=100, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('full_name', models.CharField(default='new_user', max_length=50)),
                ('password_hash', models.CharField(default='password', max_length=128)),
                ('org_name', models.CharField(default='org', max_length=50)),
                ('country_code', models.CharField(default='code', max_length=10)),
                ('latitude', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('promotion_requested', models.BooleanField(default=False)),
                ('primary_lang_code', models.CharField(default='EN', max_length=20)),
                ('primary_dialect_code', models.CharField(default='US', max_length=20)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_quizmaker', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('email_address', models.CharField(default='email', max_length=100, primary_key=True, serialize=False)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('conceptual_difficulty', models.FloatField(default=0)),
                ('time_required_mins', models.FloatField(default=0)),
                ('point_value', models.FloatField(default=0)),
                ('pages_required', models.FloatField(default=0)),
                ('approval_requested', models.BooleanField(default=True)),
                ('approved', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.chapter')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question_Loc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('question_latex', models.TextField()),
                ('answer_latex', models.TextField()),
                ('rubric_latex', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_chapter_loc', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_chapter_loc', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.question')),
            ],
        ),
        migrations.CreateModel(
            name='Question_Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('filename', models.CharField(max_length=255)),
                ('blob_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.question_loc')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('conceptual_difficulty', models.FloatField()),
                ('time_required_mins', models.IntegerField()),
                ('calculator_allowed', models.BooleanField(default=False)),
                ('computer_allowed', models.BooleanField(default=False)),
                ('internet_allowed', models.BooleanField(default=False)),
                ('book_allowed', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.chapter')),
                ('creator_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('volume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.volume')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_completed', models.DateField(blank=True, null=True)),
                ('challenge_rating', models.IntegerField(default=0)),
                ('time_rating', models.IntegerField(default=0)),
                ('creator_comment', models.TextField(default='')),
                ('viewer_comment', models.TextField()),
                ('creator_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator_id', to=settings.AUTH_USER_MODEL)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.quiz')),
                ('viewer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='viewer_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Rendering',
            fields=[
                ('rendering_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('lang_code', models.CharField(default='EN', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('paper_size', models.CharField(default='8x11', max_length=50)),
                ('blob_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Handle',
            fields=[
                ('handle_id', models.CharField(default='handle', max_length=100, primary_key=True, serialize=False)),
                ('handle', models.CharField(default='handle', max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.site')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.quiz')),
                ('support', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.support')),
            ],
        ),
        migrations.CreateModel(
            name='Support_Loc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('title_latex', models.CharField(max_length=100, null=True)),
                ('content_latex', models.CharField(max_length=500, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_approved', models.DateTimeField(default=django.utils.timezone.now)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_support_loc', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_support_loc', to=settings.AUTH_USER_MODEL)),
                ('support', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.support')),
            ],
        ),
        migrations.CreateModel(
            name='Support_Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(max_length=5)),
                ('dialect_code', models.CharField(max_length=5)),
                ('filename', models.FileField(upload_to='support_attachments/')),
                ('blob_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob')),
                ('support', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.support_loc')),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateTimeField(blank=True, null=True)),
                ('date_granted', models.DateTimeField(blank=True, null=True)),
                ('verified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verified_user', to=settings.AUTH_USER_MODEL)),
                ('verifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verifier_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='support',
            name='volume_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.volume'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='volume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.volume'),
        ),
        migrations.CreateModel(
            name='Chapter_Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=300, null=True)),
                ('creator_comment', models.CharField(max_length=300, null=True)),
                ('viewer_comment', models.CharField(max_length=300, null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.chapter')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_chapter_feedback', to=settings.AUTH_USER_MODEL)),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_chapter_feedback', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['chapter', 'lang_code', 'dialect_code'], name='chapter_feedback_comp_pkey')],
                'unique_together': {('chapter', 'lang_code', 'dialect_code')},
            },
        ),
        migrations.CreateModel(
            name='Chapter_Loc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('title', models.CharField(max_length=200, null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.chapter')),
            ],
            options={
                'indexes': [models.Index(fields=['chapter', 'lang_code', 'dialect_code'], name='chapter_loc_comp_pkey')],
                'unique_together': {('chapter', 'lang_code', 'dialect_code')},
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('is_primary', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'lang_code', 'dialect_code'], name='language_comp_pkey')],
                'unique_together': {('user', 'lang_code', 'dialect_code')},
            },
        ),
        migrations.AddIndex(
            model_name='question_loc',
            index=models.Index(fields=['question', 'lang_code', 'dialect_code'], name='question_loc_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='question_loc',
            unique_together={('question', 'lang_code', 'dialect_code')},
        ),
        migrations.AddIndex(
            model_name='question_attachment',
            index=models.Index(fields=['question', 'filename', 'lang_code', 'dialect_code'], name='question_attachment_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='question_attachment',
            unique_together={('question', 'filename', 'lang_code', 'dialect_code')},
        ),
        migrations.AddIndex(
            model_name='quiz_question',
            index=models.Index(fields=['quiz', 'question'], name='quiz_question_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='quiz_question',
            unique_together={('quiz', 'question')},
        ),
        migrations.AddIndex(
            model_name='quiz_support',
            index=models.Index(fields=['quiz', 'support'], name='quiz_support_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='quiz_support',
            unique_together={('quiz', 'support')},
        ),
        migrations.AddIndex(
            model_name='support_loc',
            index=models.Index(fields=['support', 'lang_code', 'dialect_code'], name='support_loc_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='support_loc',
            unique_together={('support', 'lang_code', 'dialect_code')},
        ),
        migrations.AddIndex(
            model_name='support_attachment',
            index=models.Index(fields=['support', 'lang_code', 'dialect_code', 'blob_key'], name='support_attachment_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='support_attachment',
            unique_together={('support', 'lang_code', 'dialect_code', 'blob_key')},
        ),
        migrations.AddIndex(
            model_name='verification',
            index=models.Index(fields=['verifier', 'verified'], name='verification_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='verification',
            unique_together={('verifier', 'verified')},
        ),
    ]
