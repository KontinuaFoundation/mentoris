# Generated by Django 4.2.5 on 2023-11-30 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blob',
            fields=[
                ('blob_key', models.BinaryField(default=b'', primary_key=True, serialize=False)),
                ('binary_data', models.BinaryField()),
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
            name='Question',
            fields=[
                ('question_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('conceptual_difficulty', models.FloatField(default=0)),
                ('time_required_mins', models.FloatField(default=0)),
                ('point_value', models.FloatField(default=0)),
                ('pages_required', models.FloatField(default=0)),
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
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_chapter_loc', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_chapter_loc', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.question')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('conceptual_difficulty', models.FloatField()),
                ('time_required_mins', models.IntegerField()),
                ('calculator_allowed', models.BooleanField(default=False)),
                ('computer_allowed', models.BooleanField(default=False)),
                ('internet_allowed', models.BooleanField(default=False)),
                ('book_allowed', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('site_id', models.CharField(default='site', max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(default='028eb885-3b10-46c6-8a99-f280ff5f2203', editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(default='new_user', max_length=50)),
                ('password_hash', models.CharField(default='password', max_length=128)),
                ('org_name', models.CharField(default='org', max_length=50)),
                ('country_code', models.CharField(default='code', max_length=10)),
                ('latitude', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('primary_lang_code', models.CharField(default='EN', max_length=20)),
                ('primary_dialect_code', models.CharField(default='US', max_length=20)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_quizmaker', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('volume_id', models.AutoField(default=0, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('support_id', models.AutoField(default=0, editable=False, primary_key=True, serialize=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.chapter')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.user')),
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
            name='Quiz_Rendering',
            fields=[
                ('rendering_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('lang_code', models.CharField(default='EN', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('paper_size', models.CharField(default='8x11', max_length=50)),
                ('blob_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.quiz')),
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
            name='Quiz_Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_completed', models.DateField(default=django.utils.timezone.now)),
                ('date_viewed', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=300, null=True)),
                ('creator_id', models.CharField(max_length=50, null=True)),
                ('viewer_id', models.CharField(max_length=50, null=True)),
                ('challenge_rating', models.IntegerField(default=0)),
                ('time_rating', models.IntegerField(default=0)),
                ('comments_text', models.TextField(null=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.quiz_rendering')),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='volume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.volume'),
        ),
        migrations.CreateModel(
            name='Question_Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('filename', models.FileField(upload_to='question_attachments/')),
                ('blob_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.question_loc')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('is_primary', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Handle',
            fields=[
                ('handle_id', models.CharField(default='handle', max_length=100, primary_key=True, serialize=False)),
                ('handle', models.CharField(default='handle', max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.site')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('email_address', models.CharField(default='email', max_length=100, primary_key=True, serialize=False)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.user')),
            ],
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
        ),
        migrations.CreateModel(
            name='Chapter_Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=300, null=True)),
                ('creator_comment', models.CharField(max_length=300, null=True)),
                ('viewer_comment', models.CharField(max_length=300, null=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.chapter')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_chapter_feedback', to='mentapp.user')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='viewed_chapter_feedback', to='mentapp.user')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='volume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentapp.volume'),
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateTimeField(blank=True, null=True)),
                ('date_granted', models.DateTimeField(blank=True, null=True)),
                ('verified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verified_user', to='mentapp.user')),
                ('verifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verifier_user', to='mentapp.user')),
            ],
            options={
                'indexes': [models.Index(fields=['verifier', 'verified'], name='verification_comp_pkey')],
                'unique_together': {('verifier', 'verified')},
            },
        ),
        migrations.CreateModel(
            name='Support_Loc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(default='ENG', max_length=5)),
                ('dialect_code', models.CharField(default='US', max_length=5)),
                ('title_latex', models.CharField(max_length=100, null=True)),
                ('content_latex', models.CharField(max_length=500, null=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_support_loc', to='mentapp.user')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_support_loc', to='mentapp.user')),
                ('support', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.support')),
            ],
            options={
                'indexes': [models.Index(fields=['support', 'lang_code', 'dialect_code'], name='support_loc_comp_pkey')],
                'unique_together': {('support', 'lang_code', 'dialect_code')},
            },
        ),
        migrations.CreateModel(
            name='Support_Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_code', models.CharField(max_length=5)),
                ('dialect_code', models.CharField(max_length=5)),
                ('filename', models.FileField(upload_to='support_attachments/')),
                ('blob_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentapp.question_loc')),
            ],
            options={
                'indexes': [models.Index(fields=['question', 'lang_code', 'dialect_code'], name='support_attachment_comp_pkey')],
                'unique_together': {('question', 'lang_code', 'dialect_code')},
            },
        ),
        migrations.AddIndex(
            model_name='quiz_rendering',
            index=models.Index(fields=['quiz', 'lang_code', 'dialect_code'], name='quiz_rendering_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='quiz_rendering',
            unique_together={('quiz', 'lang_code', 'dialect_code')},
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
            model_name='quiz_feedback',
            index=models.Index(fields=['quiz', 'lang_code', 'dialect_code'], name='quiz_feedback_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='quiz_feedback',
            unique_together={('quiz', 'lang_code', 'dialect_code')},
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
            index=models.Index(fields=['question', 'lang_code', 'dialect_code'], name='question_attachment_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='question_attachment',
            unique_together={('question', 'lang_code', 'dialect_code')},
        ),
        migrations.AddIndex(
            model_name='language',
            index=models.Index(fields=['user', 'lang_code', 'dialect_code'], name='language_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='language',
            unique_together={('user', 'lang_code', 'dialect_code')},
        ),
        migrations.AddIndex(
            model_name='chapter_loc',
            index=models.Index(fields=['chapter', 'lang_code', 'dialect_code'], name='chapter_loc_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='chapter_loc',
            unique_together={('chapter', 'lang_code', 'dialect_code')},
        ),
        migrations.AddIndex(
            model_name='chapter_feedback',
            index=models.Index(fields=['chapter', 'lang_code', 'dialect_code'], name='chapter_feedback_comp_pkey'),
        ),
        migrations.AlterUniqueTogether(
            name='chapter_feedback',
            unique_together={('chapter', 'lang_code', 'dialect_code')},
        ),
    ]
