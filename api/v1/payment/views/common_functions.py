def set_validated_data(validated_data):
    if "payment_type" in validated_data:
        area = get_area_by_id_string(validated_data["area_id"])
        validated_data["area_id"] = area.id
    if "status_id" in validated_data:
        registration_status = get_registration_status_by_id_string(validated_data["status_id"])
        validated_data["status_id"] = registration_status.id
    if "registration_type_id" in validated_data:
        registration_type = get_registration_type_by_id_string(validated_data["registration_type_id"])
        validated_data["registration_type_id"] = registration_type.id
    if "country_id" in validated_data:
        country = get_country_by_id_string(validated_data["country_id"])
        validated_data["country_id"] = country.id
    if "state_id" in validated_data:
        state = get_state_by_id_string(validated_data["state_id"])
        validated_data["state_id"] = state.id
    if "city_id" in validated_data:
        city = get_city_by_id_string(validated_data["city_id"])
        validated_data["city_id"] = city.id
    if "scheme_id" in validated_data:
        scheme = get_scheme_by_id_string(validated_data["scheme_id"])
        validated_data["scheme_id"] = scheme.id
    if "sub_area_id" in validated_data:
        sub_area = get_sub_area_by_id_string(validated_data["sub_area_id"])
        validated_data["area_id"] = sub_area.id
    if "payment_id" in validated_data:
        payment = get_payment_by_id_string(validated_data["payment_id"])
        validated_data["payment_id"] = payment.id
    if "ownership_id" in validated_data:
        ownership = get_consumer_ownership_by_id_string(validated_data["ownership_id"])
        validated_data["ownership_id"] = ownership.id
    if "consumer_category_id" in validated_data:
        consumer_category = get_consumer_category_by_id_string(validated_data["consumer_category_id"])
        validated_data["consumer_category_id"] = consumer_category.id
    if "sub_category_id" in validated_data:
        sub_category = get_consumer_sub_category_by_id_string(validated_data["sub_category_id"])
        validated_data["sub_category_id"] = sub_category.id
    if "source_id" in validated_data:
        source = get_source_type_by_id_string(validated_data["source_id"])
        validated_data["source_id"] = source.id
    return validated_data