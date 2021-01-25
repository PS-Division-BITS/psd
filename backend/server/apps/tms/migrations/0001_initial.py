# Generated by Django 3.1 on 2021-01-25 10:50

from django.db import migrations, models
import django.db.models.deletion
import server.constants


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=13)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('campus', models.IntegerField(blank=True, choices=[(0, 'Goa'), (1, 'Hyderabad'), (2, 'Pilani')], null=True)),
                ('contact', models.CharField(blank=True, help_text='Enter 10 digit contact number', max_length=20, null=True)),
                ('user_type', models.IntegerField(blank=True, choices=[(0, 'Student'), (1, 'Supervisor'), (2, 'Head of Department'), (3, 'Associate Dean'), (4, 'PS-Division')], null=True)),
                ('cgpa', models.CharField(default='NA', max_length=6)),
                ('is_active_tms', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeadlineModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline_PS2TS', models.DateTimeField(blank=True, null=True)),
                ('deadline_TS2PS', models.DateTimeField(blank=True, null=True)),
                ('is_active_PS2TS', models.BooleanField(default=False)),
                ('is_active_TS2PS', models.BooleanField(default=False)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PS2TSTransfer',
            fields=[
                ('applicant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tms.activeuserprofile')),
                ('supervisor_email', models.EmailField(max_length=254)),
                ('hod_email', models.EmailField(max_length=254)),
                ('sub_type', models.IntegerField(choices=[(0, 'PS to TS (Single Degree)'), (1, 'PS-PS to PS-TS (Dual Degree)'), (2, 'PS-PS to TS-PS (Dual Degree)'), (3, 'TS-PS to TS-TS (Dual Degree)')])),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=6)),
                ('thesis_locale', models.IntegerField(choices=[(0, 'On Campus'), (1, 'Off Campus (India)'), (2, 'Off Campus (Abroad)'), (3, 'Off Campus (Industry)')])),
                ('thesis_subject', models.CharField(help_text='Broad area/Title of Thesis', max_length=150)),
                ('name_of_org', models.CharField(help_text='Name of BITS Campus or Organization where thesis will be carried', max_length=100)),
                ('expected_deliverables', models.TextField(help_text='Expected outcome of thesis')),
                ('is_supervisor_approved', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')], default=0)),
                ('is_hod_approved', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')], default=0)),
                ('is_ad_approved', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')], default=0)),
                ('comments_from_supervisor', models.TextField(blank=True, null=True)),
                ('comments_from_hod', models.TextField(blank=True, null=True)),
                ('comments_from_ad', models.TextField(blank=True, null=True)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'PS to TS Application',
                'verbose_name_plural': 'PS to TS Applications',
            },
        ),
        migrations.CreateModel(
            name='TS2PSTransfer',
            fields=[
                ('applicant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tms.activeuserprofile')),
                ('hod_email', models.EmailField(max_length=254)),
                ('sub_type', models.IntegerField(choices=[(server.constants.TransferType['TS2PS'], 'TS to PS (Single Degree)'), (server.constants.TransferType['PSTS2PSPS'], 'PS-TS to PS-PS (Dual Degree)'), (server.constants.TransferType['TSTS2TSPS'], 'TS-TS to TS-PS (Dual Degree)')])),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=6)),
                ('reason_for_transfer', models.TextField()),
                ('name_of_org', models.CharField(help_text='Name of BITS Campus or Organization where thesis was being carried', max_length=100)),
                ('is_hod_approved', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')], default=0)),
                ('is_ad_approved', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')], default=0)),
                ('comments_from_hod', models.TextField(blank=True, null=True)),
                ('comments_from_ad', models.TextField(blank=True, null=True)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'TS to PS Application',
                'verbose_name_plural': 'TS to PS Applications',
            },
        ),
    ]
