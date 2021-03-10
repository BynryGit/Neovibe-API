# Generated by Django 3.0.3 on 2021-03-08 05:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0003_auto_20210308_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitycurrency',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 549480), null=True),
        ),
        migrations.AlterField(
            model_name='utilitycurrency',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 549480), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmentsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 561823), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmentsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 561823), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 560820), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 560820), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydocumenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 58, 950379), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydocumenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 58, 950379), null=True),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 558795), null=True),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 11, 29, 1, 558795)),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 558795), null=True),
        ),
        migrations.AlterField(
            model_name='utilityleavetype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 558795), null=True),
        ),
        migrations.AlterField(
            model_name='utilityleavetype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 558795), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymandetoryfields',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 548482), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymandetoryfields',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 548482), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 58, 940534), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymodule',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 51112), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymodule',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 51112), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentchannel',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 30168), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentchannel',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 30168), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentmode',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 557459), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentmode',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 557459), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 556461), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 556461), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 555464), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 555464), null=True),
        ),
        migrations.AlterField(
            model_name='utilityproduct',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 16206), null=True),
        ),
        migrations.AlterField(
            model_name='utilityregion',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 58, 946550), null=True),
        ),
        migrations.AlterField(
            model_name='utilityregion',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 58, 946550), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 68067), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 68067), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 68067), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 68067), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontracttemplate',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 550477), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontracttemplate',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 550477), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicemaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 551475), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicemaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 551475), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicenumberformat',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 211347), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 552472), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 552472), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 552472), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 552472), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplanrate',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 552472), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplanrate',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 552472), null=True),
        ),
        migrations.AlterField(
            model_name='utilitystatus',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 553469), null=True),
        ),
        migrations.AlterField(
            model_name='utilitystatus',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 553469), null=True),
        ),
        migrations.AlterField(
            model_name='utilitysubmodule',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 65075), null=True),
        ),
        migrations.AlterField(
            model_name='utilitysubmodule',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 28, 59, 65075), null=True),
        ),
        migrations.AlterField(
            model_name='utilityusagesummary',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 554466), null=True),
        ),
        migrations.AlterField(
            model_name='utilityusagesummary',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 554466), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkinghours',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 562816), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkinghours',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 562816), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordersubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 537510), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordersubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 537510), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordertype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 536358), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordertype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 29, 1, 536358), null=True),
        ),
    ]
