class GetAllTenants(TestCase):
    # Test Module to get all tenants API

    def set_up_tenants(self):
        TenantMaster.objects.create(
            short_name="111", name="tenant1", phone_no="9999999999",
            email_id="ten.tenant@gmail.com", region_id=1, counrty_id=1,
            state_id=1, status_id=2, is_active=True, created_by=2,
            updated_by=3, created_date="28 - 04 - 2020", updated_date="28 - 04 - 2020")
        TenantMaster.objects.create(
            short_name="222", name="tenant2", phone_no="8888888888",
            email_id="tenant22@gmail.com", region_id=4, counrty_id=5,
            state_id=5, status_id=2, is_active=True, created_by=2,
            updated_by=3, created_date="28 - 04 - 2020", updated_date="28 - 04 - 2020")
        TenantMaster.objects.create(
            short_name="333", name="tenant3", phone_no="7777777777",
            email_id="tenant33@gmail.com", region_id=4, counrty_id=5,
            state_id=5, status_id=2, is_active=True, created_by=2,
            updated_by=3, created_date="28 - 04 - 2020", updated_date="28 - 04 - 2020")

    def test_get_all_tenants(self):
        # get API response
        response = reverse('get/tenants')
        # get data from db

        tenants = TenantMaster.objects.all()
        serializer = TenantSerializer(tenants)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
