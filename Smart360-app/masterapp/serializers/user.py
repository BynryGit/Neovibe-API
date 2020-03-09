from rest_framework import serializers

#
# class PrivilegeSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(max_length=50, required=True)
#     last_name = serializers.CharField(max_length=50, required=True)
#     email = serializers.CharField(max_length=50, required=True)
#     contact_no = serializers.CharField(max_length=15, required=True)
#     address_line_1 = serializers.CharField(max_length=500, required=True)
#     city = serializers.CharField(max_length=500, required=True)
#
#     class Meta:
#         model = UserProfile
#         fields = ('first_name', 'last_name', 'email', 'contact_no', 'address_line_1', 'city')
#
#     def update_profile(self, validated_data, user, userprofileimage=None):
#         city_obj = get_object_or_404(City, city=validated_data['city'], is_deleted=False)
#
#         user.first_name = validated_data['first_name']
#         user.last_name = validated_data['last_name']
#         user.email = validated_data['email']
#         user.contact_no = validated_data['contact_no']
#         user.address_line_1 = validated_data['address_line_1']
#         user.city = city_obj
#
#         try:
#             user.profile_image = str(settings.MEDIA_URL) #+ str(userprofileimage.user_profile_image)
#         except Exception:
#             pass
#
#         user.userprofile.save()
#         return user.userprofile