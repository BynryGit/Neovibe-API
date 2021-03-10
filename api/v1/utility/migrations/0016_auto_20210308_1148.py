# Generated by Django 3.0.3 on 2021-03-08 06:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0015_auto_20210308_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilitycurrency',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 941046), null=True),
        ),
        migrations.AlterField(
            model_name='utilitycurrency',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 941046), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmentsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 954011), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmentsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 954011), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 953014), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydepartmenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 953014), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydocumenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 323312), null=True),
        ),
        migrations.AlterField(
            model_name='utilitydocumenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 323312), null=True),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 951019), null=True),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 11, 48, 55, 951019)),
        ),
        migrations.AlterField(
            model_name='utilityholidaycalendar',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 951019), null=True),
        ),
        migrations.AlterField(
            model_name='utilityleavetype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 951019), null=True),
        ),
        migrations.AlterField(
            model_name='utilityleavetype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 951019), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymandetoryfields',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 940049), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymandetoryfields',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 940049), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 313339), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymodule',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 431053), null=True),
        ),
        migrations.AlterField(
            model_name='utilitymodule',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 431053), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentchannel',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 407089), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentchannel',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 407089), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentmode',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 949025), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentmode',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 949025), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentsubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 948027), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymentsubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 948027), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymenttype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 947030), null=True),
        ),
        migrations.AlterField(
            model_name='utilitypaymenttype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 947030), null=True),
        ),
        migrations.AlterField(
            model_name='utilityproduct',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 389137), null=True),
        ),
        migrations.AlterField(
            model_name='utilityregion',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 319323), null=True),
        ),
        migrations.AlterField(
            model_name='utilityregion',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 319323), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 450972), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 450972), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 450972), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 450972), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontracttemplate',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 942043), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontracttemplate',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 942043), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicemaster',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 943059), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicemaster',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 943059), null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicenumberformat',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 600767), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 944038), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 944038), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 944038), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplan',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 944038), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplanrate',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 945035), null=True),
        ),
        migrations.AlterField(
            model_name='utilityserviceplanrate',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 945035), null=True),
        ),
        migrations.AlterField(
            model_name='utilitystatus',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 946033), null=True),
        ),
        migrations.AlterField(
            model_name='utilitystatus',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 946033), null=True),
        ),
        migrations.AlterField(
            model_name='utilitysubmodule',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 447980), null=True),
        ),
        migrations.AlterField(
            model_name='utilitysubmodule',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 53, 447980), null=True),
        ),
        migrations.AlterField(
            model_name='utilityusagesummary',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 946033), null=True),
        ),
        migrations.AlterField(
            model_name='utilityusagesummary',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 946033), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkinghours',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 955008), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkinghours',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 955008), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordersubtype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 929078), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordersubtype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 929078), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordertype',
            name='created_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 928081), null=True),
        ),
        migrations.AlterField(
            model_name='utilityworkordertype',
            name='updated_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 48, 55, 928081), null=True),
        ),
    ]
