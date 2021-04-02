from v1.billing.models.invoice_bill import get_consumer_invoice_bill_by_month, get_previous_consumer_bill, InvoiceBill
from v1.consumer.models.consumer_category import get_consumer_category_by_id_string,get_consumer_category_by_id
from v1.consumer.models.consumer_master import ConsumerMaster, get_consumer_by_consumer_no
from v1.consumer.models.consumer_scheme_master import ConsumerSchemeMaster
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id_string, get_consumer_sub_category_by_id
from v1.meter_data_management.models.meter_reading import MeterReading
from v1.meter_data_management.models.meter import get_meter_by_id
from v1.payment.models.payment import Payment
from v1.utility.models.utility_service_plan import get_utility_service_plans_by_dates, UtilityServicePlan
from v1.utility.models.utility_service_plan_rate import get_utility_service_plans_rates, UtilityServicePlanRate
from datetime import datetime, timedelta
from api.messages import *
from rest_framework import status
from v1.commonapp.models.global_lookup import get_global_lookup_by_id_string,get_global_lookup_by_id
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_master import get_utility_by_id_string
from v1.tenant.models.tenant_master import get_tenant_by_id_string
from v1.commonapp.models.city import get_city_by_id_string
from v1.commonapp.models.zone import get_zone_by_id_string
from v1.commonapp.models.area import get_area_by_id_string
from v1.commonapp.models.sub_area import get_sub_area_by_id_string
from v1.commonapp.models.division import get_division_by_id_string
from v1.utility.models.utility_product import get_utility_product_by_id_string,get_utility_product_by_id
from master.models import get_user_by_id_string
from  v1.billing.models.bill_cycle import get_bill_cycle_by_id_string

from django.db import transaction
from v1.billing.models.bill_schedule import get_schedule_bill_by_id_string
from v1.billing.models.bill_cycle import get_bill_cycle_by_id
from v1.meter_data_management.models.route import get_route_by_id_string
from v1.consumer.models.consumer_service_contract_details import get_consumer_service_contract_detail_by_premise_id,get_consumer_service_contract_detail_by_id,\
     ConsumerServiceContractDetail,get_consumer_service_contract_detail_by_consumer_id
from v1.billing.models.bill_schedule_log import get_schedule_bill_log_by_schedule_id
from v1.billing.models.bill_consumer_detail import get_bill_consumer_detail_by_schedule_log_id
from v1.meter_data_management.models.meter import Meter
from v1.consumer.models.consumer_master import get_consumer_by_id
from v1.utility.models.utility_service_contract_master import get_utility_service_contract_master_by_id
from v1.commonapp.models.premises import get_premise_by_id_string
from v1.billing.models.rate import Rate as RateTbl, get_rate_by_category_sub_category_wise
from v1.billing.models.bill_schedule import ScheduleBill
from v1.billing.models.bill import Bill as BillTbl
from v1.payment.models.payment import Payment as PaymentTbl
from v1.billing.models.fixed_charges import get_fixed_charges_by_id_meter_no

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


# def save_outstanding(consumer, bill_month):
#     try:
#         bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
#         if bill.bill_count == 1:
#             bill.outstanding = 0.0
#             bill.save()
#         else:
#             prvious_bill = get_previous_consumer_bill(consumer)
#             if prvious_bill.bill_status_id == 'PAID':#TODO:Replace with Id
#                 if Payment.objects.filter(penalty=True, identification_id=prvious_bill.id, is_active=True).exists():
#                     bill.outstanding = prvious_bill.after_due_date_amount
#                     bill.save()
#                 else:
#                     bill.outstanding = prvious_bill.before_due_date_amount
#                     bill.save()
#             if prvious_bill.bill_status_id == "PARTIAL":#TODO:Replace with Id
#                 if Payment.objects.filter(penalty=True, identification_id=prvious_bill.id, is_active=True).exists():
#                     bill.outstanding = prvious_bill.after_due_date_amount
#                     bill.save()
#                 else:
#                     bill.outstanding = prvious_bill.before_due_date_amount
#                     bill.save()
#             if prvious_bill.bill_status_id == "UNPAID":#TODO:Replace with Id
#                 bill.outstanding = prvious_bill.after_due_date_amount
#                 bill.save()
#     except:
#         pass


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

# Function for get rate
# def get_rate(schedule):
#     bill_shedule_obj = get_schedule_bill_by_id_string(schedule.id_string)
#     bill_cycle_obj = get_bill_cycle_by_id(bill_shedule_obj.bill_cycle_id)
#     for route in bill_cycle_obj.route_json:
#         route_obj = get_route_by_id_string(route['id_string'])
#         for premise in route_obj.premises_json:
#             premise_obj = get_premise_by_id_string(premise['id_string'])
#             consumer_meter_obj = get_consumer_service_contract_detail_by_premise_id(premise_obj.id)
#             contract_obj = get_utility_service_contract_master_by_id(consumer_meter_obj.service_contract_id)
#     rate_obj = get_rate_by_category_sub_category_wise(bill_shedule_obj.utility,bill_shedule_obj.utility_product_id,contract_obj.consumer_category_id,contract_obj.consumer_sub_category_id)
#     return rate_obj.rate

# # Function for generate current charges
# def generate_current_charges(meter, bill_month, schedule):
#     consumption = meter.current_reading - meter.previous_reading
#     rate = get_rate(schedule)
#     current_charge = consumption * rate
#     return current_charge

# Function for save readings and consumption
def save_meter_data(consumer, bill_month):
    try:
        consumption = 0.0
        current_reading = 0.0
        readings = MeterReading.objects.filter(month=bill_month, consumer_no=consumer)
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        for reading in readings:
            current_reading += reading.current_reading
            consumption += reading.consumption
        bill.meter_reading = {"current_reading":current_reading, "consumption":consumption}
        bill.save()
    except:
        pass

# Function for save outstanding
def save_outstanding(consumer, bill_month):
    try:
        bill = get_consumer_invoice_bill_by_month(consumer, bill_month)
        
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



# Function for validate data at time of add add bill schedule
def set_schedule_bill_validated_data(validated_data):
    if "utility_id" in validated_data:
        utility = get_utility_by_id_string(validated_data["utility_id"])
        if utility:
            validated_data["utility_id"] = utility.id
        else:
            raise CustomAPIException(UTILITY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "recurring_id" in validated_data:
        recurring = get_global_lookup_by_id_string(validated_data["recurring_id"])
        if recurring:
            validated_data["recurring_id"] = recurring.id
        else:
            raise CustomAPIException(IS_RECCURING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "bill_cycle_id" in validated_data:
        read_cycle = get_bill_cycle_by_id_string(validated_data["bill_cycle_id"])
        if read_cycle:
            validated_data["bill_cycle_id"] = read_cycle.id
        else:
            raise CustomAPIException(READ_CYCLE_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "frequency_id" in validated_data:
        frequency = get_global_lookup_by_id_string(validated_data["frequency_id"])
        if frequency:
            validated_data["frequency_id"] = frequency.id
        else:
            raise CustomAPIException(FREQUENCY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    else:
        validated_data["frequency_id"] = None

    if "repeat_every_id" in validated_data:
        repeat_every = get_global_lookup_by_id_string(validated_data["repeat_every_id"])
        if repeat_every:
            validated_data["repeat_every_id"] = repeat_every.id
        else:
            raise CustomAPIException(REPEAT_FREQUENCY_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    else:
        validated_data["repeat_every_id"] = None

    if "utility_product_id" in validated_data:
        utility_product = get_utility_product_by_id_string(validated_data["utility_product_id"])
        if utility_product:
            validated_data["utility_product_id"] = utility_product.id
        else:
            raise CustomAPIException(UTILITY_PRODUCT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

    if "occurs_on" in validated_data:
        pass
    else:
        validated_data["occurs_on"] = []

    if "end_date" in validated_data:
        pass
    else:
        validated_data["end_date"] = None

    if "cron_expression" in validated_data:
        pass
    else:
        validated_data["cron_expression"] = None

    return validated_data


# Function for get consumer count it used before runbill
def get_consumer_count(schedule_id):
    try:
        consumer = {}
        schedule_log_id = get_schedule_bill_log_by_schedule_id(schedule_id)
        if schedule_log_id:
            bill_consumer_obj = get_bill_consumer_detail_by_schedule_log_id(schedule_log_id.id).count()
            consumer['consumer'] = bill_consumer_obj
        else:
            consumer['consumer'] = "----"
        return consumer['consumer'] 
    except Exception as e:
        print('-get_consumer_count-----',e)
        pass

# Function for get reading count it used before runbill
def get_reading_count(schedule_obj):
    try:
        meters_no_list = []
        schedule = get_schedule_bill_by_id_string(schedule_obj.id_string)
        if schedule:
            frequency = get_global_lookup_by_id(schedule.frequency_id)
            schedule_log_id = get_schedule_bill_log_by_schedule_id(schedule.id)
            if schedule_log_id:
                bill_consumer_obj = get_bill_consumer_detail_by_schedule_log_id(schedule_log_id.id)
                for meter in bill_consumer_obj:
                    meter_id = get_meter_by_id(meter.meter_id)
                    meters_no_list.append(meter_id.meter_no)
                if frequency.key == 'daily':
                    meter_reading_obj = MeterReading.objects.filter(created_date__date=schedule.start_date.date(),meter_no__in=meters_no_list).count()
                elif frequency.key == 'monthly':
                    meter_reading_obj = MeterReading.objects.filter(created_date__month=schedule.start_date.month,meter_no__in=meters_no_list).count()
                return meter_reading_obj
            else:
                return '----'
        else:
            return '----'
    except Exception as e:
        print('======get_reading_count========',e)
        pass
    

# Function for get rate it used before runbill
def get_rate(schedule_bill_obj): 
    try: 
        electricity = []
        schedule_bill_obj = get_schedule_bill_by_id_string(schedule_bill_obj.id_string)
        bill_cycle_obj = get_bill_cycle_by_id(schedule_bill_obj.bill_cycle_id)
        if bill_cycle_obj:
            for route in bill_cycle_obj.route_json:
                route_obj = get_route_by_id_string(route['id_string'])
                for premise in route_obj.premises_json:
                    premise_obj = get_premise_by_id_string(premise['id_string'])
                    consumer_meter_obj = get_consumer_service_contract_detail_by_premise_id(premise_obj.id)
                    contract_obj = get_utility_service_contract_master_by_id(consumer_meter_obj.service_contract_id)
            rate_obj = get_rate_by_category_sub_category_wise(schedule_bill_obj.utility,schedule_bill_obj.utility_product_id,contract_obj.consumer_category_id,contract_obj.consumer_sub_category_id)
            for electricity_rate in rate_obj:
                rate = {}
                # rate['id_string'] = electricity_rate.id_string
                rate['unit'] = electricity_rate.unit
                rate['rate'] = electricity_rate.rate
                rate['product']= get_utility_product_by_id(electricity_rate.utility_product_id).name
                electricity.append(rate)
            return electricity
        else:
            return False
    except Exception as e:
        print('-get_rate-----',e)
        pass

# Function for getting additional charge count it used before runbill
def get_additional_charges_amount(schedule_bill_obj):
    try:
        outstanding_amount = 0
        adjustment_amount = 0
        refund_amount = 0
        credit_amount = 0
        penalty_amount = 0
        paid_amount = 0
        normal_meter = 0
        rcnt_meter = 0
        faulty_meter = 0

        schedule_obj = ScheduleBill.objects.filter(utility_product_id=schedule_bill_obj.utility_product_id, bill_cycle_id = schedule_bill_obj.bill_cycle_id,end_date__lte=schedule_bill_obj.start_date.date(), is_active=True)
        if schedule_obj:
            schedule_obj = schedule_obj.filter().order_by('-bill_cycle_id')[0]
            schedule_log_id = get_schedule_bill_log_by_schedule_id(schedule_bill_obj.id)
            consumer_list = []
            additional_charges = {}
            data = {}
            meter_status = {}
            outstanding = {}
            if schedule_log_id:
                bill_consumer_obj = get_bill_consumer_detail_by_schedule_log_id(schedule_log_id.id)
                for consumer in bill_consumer_obj:
                    consumer_list.append(consumer)

            consumer_contract = ConsumerServiceContractDetail.objects.filter(consumer_no__in = [consumer.consumer_no for consumer in consumer_list])

            bill_obj = BillTbl.objects.filter(bill_date__range=[schedule_obj.end_date.date(),schedule_bill_obj.start_date.date()],
            consumer_service_contract_detail_id__in = [con_contract.id for con_contract in consumer_contract] )

            for bill in bill_obj:
                if "outstanding" in bill.rate_details:
                    outstanding_amount += bill.rate_details['outstanding']
                if "adjustment" in bill.additional_charges:
                    adjustment_amount += bill.additional_charges['adjustment']
                if "refund" in bill.additional_charges:
                    refund_amount += bill.additional_charges['refund']
                if "credit_amount" in bill.additional_charges:
                    credit_amount += bill.additional_charges['credit_amount']
                if "penalty" in bill.additional_charges:
                    penalty_amount += bill.additional_charges['penalty']


            meter_obj = Meter.objects.filter(id__in=[con_contract.meter_id for con_contract in consumer_contract])
            for meter in meter_obj:

                if meter.meter_status == 0:
                    normal_meter += 1
                if meter.meter_status == 1:
                    faulty_meter += 1
                if meter.meter_status == 2:
                    rcnt_meter += 1
            
            payment_obj = Payment.objects.filter(transaction_date__range=[schedule_obj.end_date.date(),schedule_bill_obj.start_date.date()],
            consumer_no__in = [consumer.consumer_no for consumer in consumer_list])

            for payment in payment_obj:
                if payment.transaction_amount and payment.transaction_charges:
                    paid_amount += payment.transaction_amount + payment.transaction_charges
                else:
                    paid_amount += payment.transaction_amount

            meter_status['normal_meter'] = normal_meter
            meter_status['faulty_meter'] = faulty_meter
            meter_status['rcnt_meter'] = rcnt_meter
            outstanding['outstanding_amount'] = outstanding_amount
            additional_charges['adjustment_amount'] = adjustment_amount
            additional_charges['refund_amount'] = refund_amount
            additional_charges['credit_amount'] = credit_amount
            additional_charges['penalty_amount'] = penalty_amount
            additional_charges['paid_amount'] = paid_amount

            data = {"meter_status":meter_status,"outstanding":outstanding,"additional_charges":additional_charges }
            return data
        else:
            meter_status = {}
            outstanding = {}
            additional_charges = {}
            meter_status['normal_meter'] = 0
            meter_status['faulty_meter'] = 0
            meter_status['rcnt_meter'] = 0
            outstanding['outstanding_amount'] = 0
            additional_charges['adjustment_amount'] = 0
            additional_charges['refund_amount'] = 0
            additional_charges['credit_amount'] = 0
            additional_charges['penalty_amount'] = 0
            additional_charges['paid_amount'] = 0

            data = {"meter_status":meter_status,"outstanding":outstanding,"additional_charges":additional_charges }
            return data
    except Exception as e:
        print('=====get_additional_charges_amount====',e)
        pass

# Calculate bill current charges
def calculate_current_all_charges(data):
    try:
        # get bill schedule object
        schedule_bill_obj = get_schedule_bill_by_id_string(data['schedule_bill_id_string'])
        frequency = get_global_lookup_by_id(schedule_bill_obj.frequency_id)
        rate = data['rate_obj']
        # get bill schedule log object by schedule
        schedule_log_id = get_schedule_bill_log_by_schedule_id(schedule_bill_obj.id)
        if schedule_log_id:

            # get Consumers according to bill schedule log
            bill_consumer_obj = get_bill_consumer_detail_by_schedule_log_id(schedule_log_id.id)
            for consumer in bill_consumer_obj:
                # getting consumer service contract by consumer Id
                service_contract_obj = get_consumer_service_contract_detail_by_consumer_id(consumer.consumer_id)
                if service_contract_obj:

                    # get bill objects according to consumer service contract
                    bill_obj = BillTbl.objects.filter(consumer_service_contract_detail_id = service_contract_obj.id, is_active=True).last() 
                    if bill_obj:
                        if frequency.key == 'daily':
                            meter_reading = MeterReading.objects.get(created_date__date=schedule_bill_obj.start_date.date(),consumer_no=consumer.consumer_no, meter_no=consumer.meter_no)
                            bill_date_val = (datetime.now() + timedelta(days=7))
                            bill_period_val = "7 Days"
                        elif frequency.key == 'monthly':
                            meter_reading = MeterReading.objects.get(created_date__month=schedule_bill_obj.start_date.month,consumer_no=consumer.consumer_no, meter_no=consumer.meter_no)
                            bill_date_val = (meter_reading.created_date + timedelta(days=30))
                            bill_period_val = "30 Days"
                        privious_meter_reading = bill_obj.meter_reading['current_meter_reading']
                        
                        # calculate current charge
                        current_charge = calculate_current_charges(privious_meter_reading,meter_reading.current_meter_reading,rate)
                        fixed_charges = get_fixed_charges_by_id_meter_no(consumer.meter_no)

                        # calculate outstanding amount
                        outstanding_amt = get_outstanding_amount(consumer,bill_obj)

                        # calculate opening balance
                        if int(bill_obj.opening_balance) > 0:
                            opening_balance = int(current_charge) + int(outstanding_amt) + int(fixed_charges)

                        meter_data = {
                            "privious_meter_reading" : privious_meter_reading,
                            "current_meter_reading" : meter_reading.current_meter_reading,
                            "previous_meter_reading_date" : str((bill_obj.bill_date).date()),
                            "current_meter_reading_date" : str((meter_reading.created_date).date()), 
                            "consumption" : int(meter_reading.current_meter_reading) - int(privious_meter_reading),
                            "amount_before_due_date" : int(opening_balance),
                            "amount_after_due_date" : int(opening_balance) + 50,
                            "fixed_charges": fixed_charges,
                        }

                        
                        rate_details = [{"rate":rate, "outstanding" : outstanding_amt,"consumption_charges":current_charge}]
                    else:
                        if frequency.key == 'daily':
                            meter_reading = MeterReading.objects.get(created_date__date=schedule_bill_obj.start_date.date(),consumer_no=consumer.consumer_no, meter_no=consumer.meter_no)
                            bill_date_val = (datetime.now() + timedelta(days=7))
                            bill_period_val = "7 Days"
                        elif frequency.key == 'monthly':
                            meter_reading = MeterReading.objects.get(created_date__month=schedule_bill_obj.start_date.month,consumer_no=consumer.consumer_no, meter_no=consumer.meter_no)
                            bill_date_val = (meter_reading.created_date + timedelta(days=30))
                            bill_period_val = "30 Days"

                        privious_meter_reading = 0
                        current_charge = calculate_current_charges(privious_meter_reading,meter_reading.current_meter_reading,rate)
                        opening_balance = int(current_charge) + int(fixed_charges)
                        meter_data = {
                            "privious_meter_reading" : privious_meter_reading,
                            "current_meter_reading" : meter_reading.current_meter_reading,
                            "previous_meter_reading_date" : "",
                            "current_meter_reading_date" : str((meter_reading.created_date).date()),
                            "consumption" : int(meter_reading.current_meter_reading) - int(privious_meter_reading),
                            "amount_before_due_date" : int(opening_balance),
                            "amount_after_due_date" : int(opening_balance) + 50,
                            "fixed_charges": fixed_charges,
                        }
                        rate_details = [{"unit":rate['unit'],"rate":rate['rate'], "outstanding" : 0,"consumption_charges":current_charge}]

                    # save bill data
                    if BillTbl.objects.filter(consumer_service_contract_detail_id = service_contract_obj.id,bill_cycle_id = schedule_bill_obj.bill_cycle_id,current_charges = current_charge,is_active=True).exists():
                        print('EXISTS')
                    else:
                        with transaction.atomic():    
                            bill_val = BillTbl(
                                tenant = schedule_bill_obj.tenant,
                                utility = schedule_bill_obj.utility,
                                consumer_service_contract_detail_id = service_contract_obj.id,
                                consumer_no = service_contract_obj.consumer_no,
                                bill_cycle_id = schedule_bill_obj.bill_cycle_id,
                                meter_reading = meter_data,
                                bill_month = (meter_reading.created_date).strftime("%B"),
                                rate_details = rate_details,
                                bill_date = bill_date_val,
                                bill_period = bill_period_val,
                                opening_balance = opening_balance,
                                current_charges = current_charge,
                                is_active = True                        
                            ).save()

            # return bill_val

    except Exception as ex:
        print('********',ex)
        pass


# geberate current charges function
def calculate_current_charges(privious_meter_reading,current_meter_reading,rate):
    try:
        unit_list = []
        rate_list = []
        finalunitrate = []
        current_charge = (int(current_meter_reading) - int(privious_meter_reading))
        item = []
        if rate[0]['product'] == 'Gas':
            current_charge = current_charge * int(rate[0]['rate'])
            return current_charge
        elif rate[0]['product'] == 'Power':
            for rate_val in rate:
                unit_list.append(rate_val['unit'])
                rate_list.append(rate_val['rate'])
            # creating length of list (e.g. current_charge is 250 )
            for a in range(len(unit_list)):
                if str(unit_list[a].split('-')[0]) != str('>') and int(current_charge) > int(unit_list[a].split('-')[0]):
                    item.append(unit_list[a])
                
            if int(current_charge) > int(unit_list[len(unit_list)-1].split('-')[1]): # it check last element value
                for a in range(len(unit_list)): # if current_charge are greater than all unit range then loop iterate len wise
                    if int(current_charge) > int(unit_list[a].split('-')[1]) or int(current_charge) == int(unit_list[a].split('-')[1]):
                        if str(unit_list[a].split('-')[0]) != '>':                        
                            finalunitrate.append((int(unit_list[a].split('-')[1])-(int(unit_list[a].split('-')[0])-1))*int(rate_list[a]))
                        else:
                            finalunitrate.append((int(current_charge) - int(unit_list[a].split('-')[1])) * int(rate_list[a]))
                    else:
                        finalunitrate.append((int(unit_list[a].split('-')[1])-int(current_charge))*int(rate_list[a])) # not needed
            else:
                for a in range(len(item)):
                    if int(current_charge) > int(unit_list[a].split('-')[1]) or int(current_charge) == int(unit_list[a].split('-')[1]):
                        if str(unit_list[a].split('-')[0]) != '>':                        
                            finalunitrate.append((int(unit_list[a].split('-')[1])-(int(unit_list[a].split('-')[0])-1))*int(rate_list[a]))
                        else:
                            finalunitrate.append((int(current_charge) - int(unit_list[a].split('-')[1])) * int(rate_list[a]))
                    else:
                        finalunitrate.append((int(current_charge) - (int(unit_list[a-1].split('-')[1])))*int(rate_list[a]))

            return sum(finalunitrate)
    except Exception as ex:
        print('=========Excepion====>',ex)



# geberate Outstanding amount function
def get_outstanding_amount(consumer,bill_obj):
    if PaymentTbl.objects.filter(consumer_no=consumer.consumer_no, state=1,transaction_date__lte=bill_obj.bill_date.date()).exists():
        return bill_obj.meter_reading['amount_before_due_date']
    elif PaymentTbl.objects.filter(consumer_no=consumer.consumer_no, state=1,transaction_date__gte=bill_obj.bill_date.date()).exists():
        return bill_obj.meter_reading['amount_after_due_date']
    else:
        return bill_obj.meter_reading['amount_after_due_date']