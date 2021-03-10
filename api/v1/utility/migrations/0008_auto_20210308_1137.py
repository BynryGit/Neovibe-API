# Generated by Django 3.0.3 on 2021-03-08 06:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0007_auto_20210308_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitycurrency',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 273815), null=True),
        ),
        migrations.AlterField(
            model_name='utilitycurrency',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 273815), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmentsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 285785), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmentsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 285785), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 284786), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 284786), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydocumenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 671028), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydocumenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 671028), null=True),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 283789), null=True),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 11, 37, 25, 283789)),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 283789), null=True),
        ),
        migrations.AlterField(
            model_name='utilityleavetype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 282796), null=True),
        ),
        migrations.AlterField(
            model_name='utilityleavetype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 282796), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymandetoryfields',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 272822), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymandetoryfields',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 272822), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 662052), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymodule',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 768780), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymodule',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 768780), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentchannel',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 747823), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentchannel',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 747823), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentmode',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 281796), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentmode',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 281796), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 280800), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 280800), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 279800), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 279800), null=True),
        ),
        migrations.AlterField(
            model_name='utilityproduct',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 732863), null=True),
        ),
        migrations.AlterField(
            model_name='utilityregion',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 667039), null=True),
        ),
        migrations.AlterField(
            model_name='utilityregion',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 667039), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 785721), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 785721), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 785721), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 785721), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontracttemplate',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 274812), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontracttemplate',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 274812), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicemaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 275809), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicemaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 275809), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicenumberformat',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 945631), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 276780), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 276780), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 276780), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 276780), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplanrate',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 277776), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplanrate',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 277776), null=True),
        ),
        migrations.AlterField(
            model_name='utilitystatus',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 278773), null=True),
        ),
        migrations.AlterField(
            model_name='utilitystatus',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 278773), null=True),
        ),
        migrations.AlterField(
            model_name='utilitysubmodule',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 781732), null=True),
        ),
        migrations.AlterField(
            model_name='utilitysubmodule',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 22, 781732), null=True),
        ),
        migrations.AlterField(
            model_name='utilityusagesummary',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 278773), null=True),
        ),
        migrations.AlterField(
            model_name='utilityusagesummary',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 278773), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkinghours',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 286782), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkinghours',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 286782), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordersubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 261847), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordersubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 261847), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordertype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 260848), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordertype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 37, 25, 260848), null=True),
        ),
    ]
