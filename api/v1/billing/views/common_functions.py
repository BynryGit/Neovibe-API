from v1.billing.models.invoice_bill import get_consumer_invoice_bill_by_month, get_previous_consumer_bill, InvoiceBill
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string
from v1.consumer.models.consumer_master import ConsumerMaster, get_consumer_by_consumer_no
from v1.consumer.models.consumer_scheme_master import ConsumerSchemeMaster
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string
from v1.meter_reading.models.meter_reading import get_consumer_meter_reading_by_bill_month, MeterReading
# from v1.meter_reading.models.temp_consumer_master import TempConsumerMaster
from v1.payment.models.consumer_payment import Payment
from v1.utility.models.utility_service_plan import get_utility_service_plans_by_dates, UtilityServicePlan
from v1.utility.models.utility_service_plan_rate import get_utility_service_plans_rates, UtilityServicePlanRate


def set_validated_data(validated_data):
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        validated_data["consumer_category_id"] = consumer_category.id
    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        validated_data["sub_category_id"] = sub_category.id
    return validated_data


def run_bill(consumer, bill_month, due_date, schedule):
    try:
        generate_consumer_bill(consumer, bill_month, due_date, schedule)
    except:
        pass


def generate_consumer_bill(consumer, bill_month, due_date, schedule):
    try:
        consumer_obj = TempConsumerMaster.objects.get(consumer_no = consumer, bill_month = bill_month)
        if InvoiceBill.objects.filter(consumer_no = consumer, bill_month = bill_month).exists():
            pass
        else:
            bill = InvoiceBill()
            bill.tenant = schedule.tenent
            bill.utility = schedule.utility
            bill.consumer_no = consumer
            bill.bill_month = bill_month
            bill.due_date = due_date
            bill.address = consumer_obj.address_line_1
            bill.contact = consumer_obj.phone_mobile
            bill.route_id = consumer_obj.route
            bill.cycle_id = consumer_obj.bill_cycle
            if InvoiceBill.objects.filter(consumer_no = consumer).exists():
                bill.bill_count = InvoiceBill.objects.filter(consumer_no = consumer).count() + 1
            else:
                bill.bill_count = 1
            bill.save()
    except:
        pass


def save_outstanding(consumer, bill_month):
    try:
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        if bill.bill_count == 1:
            bill.outstanding = 0.0
            bill.save()
        else:
            prvious_bill = get_previous_consumer_bill(consumer)
            if prvious_bill.bill_status_id == 'PAID':#TODO:Replace with Id
                if Payment.objects.filter(penalty=True, identification_id=prvious_bill.id, is_active=True).exists():
                    bill.outstanding = prvious_bill.after_due_date_amount
                    bill.save()
                else:
                    bill.outstanding = prvious_bill.before_due_date_amount
                    bill.save()
            if prvious_bill.bill_status_id == "PARTIAL":#TODO:Replace with Id
                if Payment.objects.filter(penalty=True, identification_id=prvious_bill.id, is_active=True).exists():
                    bill.outstanding = prvious_bill.after_due_date_amount
                    bill.save()
                else:
                    bill.outstanding = prvious_bill.before_due_date_amount
                    bill.save()
            if prvious_bill.bill_status_id == "UNPAID":#TODO:Replace with Id
                bill.outstanding = prvious_bill.after_due_date_amount
                bill.save()
    except:
        pass


def save_payment(consumer, bill_month):
    try:
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        if bill.bill_count == 1:
            bill.payment = 0.0
            bill.save()
        else:
            prvious_bill = get_previous_consumer_bill(consumer)
            payment = 0.0
            if Payment.objects.filter(identification_id=prvious_bill.id, is_active=True).exists():
                for payment in Payment.objects.filter(identification_id=prvious_bill.id, is_active=True):
                    payment += payment.transaction_amount
                bill.payment = payment
                bill.save()
            else:
                bill.payment = payment
                bill.save()
    except:
        pass


def save_emi(consumer, bill_month):
    try:
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        emi = 0.0
        if ConsumerMaster.objects.filter(consumer_no=consumer).exists():
            consumer = ConsumerMaster.objects.filter(consumer_no=consumer)
            scheme = ConsumerSchemeMaster.objects.filter(id=consumer.scheme_id)
            if consumer.deposit_amt - consumer.collected_amt <= 0:
                consumer.collected_amt = consumer.collected_amt + scheme.monthly_emi
                bill.current_emi_amt = scheme.monthly_emi
                consumer.save()
                bill.save()
            else:
                bill.current_emi_amt = emi
                bill.save()
        else:
            bill.current_emi_amt = emi
            bill.save()
    except:
        pass


def save_meter_data(consumer, bill_month):
    try:
        consumption = 0.0
        current_reading = 0.0
        readings = MeterReading.objects.filter(month=bill_month, consumer_no=consumer)
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        for reading in readings:
            current_reading += reading.current_reading
            consumption += reading.consumption
        bill.current_reading = current_reading
        bill.consumption = consumption
        bill.save()
    except:
        pass


def save_bill_rates(consumer, bill_month, schedule):
    try:
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        consumption_charges = 0.0
        if schedule.reading_frequency == "HOURLY":
            readings = MeterReading.objects.filter(month=bill_month, consumer_no=consumer)
            for reading in readings:
                plan = UtilityServicePlan.objects.get(utility=schedule.utility,
                                                      start_date__hour=reading.reading_date.hour)
                rate = UtilityServicePlanRate.objects.get(utility_service_plan_id=plan.id)
                if rate.is_taxable == True:
                    consumption_charges += (rate.base_rate + ((rate.taxrate/100) * rate.base_rate)) * reading.consumption
                else:
                    consumption_charges += rate.base_rate * reading.consumption
            bill.consumption_charges = consumption_charges
            bill.save()

        if schedule.reading_frequency == "MONTHLY":
            reading = MeterReading.objects.filter(month=bill_month, consumer_no=consumer).last()
            plans = UtilityServicePlan.objects.filter(utility=schedule.utility,
                                                      start_date__lte=bill.previous_reading_date,
                                                      end_date__gte=bill.current_reading_date).oder_by("start_date")
            rates = UtilityServicePlanRate.objects.filter(utility_service_plan_id__in=[plan.id for plan in plans])
            days = (bill.current_reading_date - bill.previous_reading_date).days
            per_day_consumption = bill.consumption/days
            if rates.len == 1:
                if rates[0].is_taxable == True:
                    consumption_charges += (rates[0].base_rate +
                                            ((rates[0].taxrate / 100) * rates[0].base_rate)) * reading.consumption
                else:
                    consumption_charges += rates[0].base_rate * reading.consumption
            else:
                previous_reading_date = bill.previous_reading_date
                for rate in rates:
                    days = (rate.end_date - previous_reading_date).days
                    if rates.last() == rate:
                        days = (bill.current_reading_date - previous_reading_date).days
                    if rate.is_taxable == True:
                        consumption_charges += (rate.base_rate + (
                                (rate.taxrate / 100) * rate.base_rate)) * per_day_consumption * days
                        previous_reading_date = rate.end_date
                    else:
                        consumption_charges += rate.base_rate * per_day_consumption * days
                        previous_reading_date = rate.end_date
            bill.consumption_charges = consumption_charges
            bill.save()

        if schedule.reading_frequency == "DAILY":
            pass
    except:
        pass
